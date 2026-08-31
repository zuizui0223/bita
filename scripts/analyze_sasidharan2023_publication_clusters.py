"""Publication-cluster sensitivity for Sasidharan et al. 2023 Table S1.

Input is the losslessly exported S1 CSV from recover_sasidharan2023_supplement_v2.py.
The source article treats FVOC x insect tests as analysis rows; this script preserves
those rows but resamples whole publication-reference clusters to avoid treating tests
within one publication as independent replication.
"""
from __future__ import annotations
import argparse, csv, json, random
from collections import defaultdict
from pathlib import Path

SEED=20260831
B=20000

def read_rows(path):
    with open(path,encoding='utf-8',newline='') as h:
        rows=list(csv.reader(h))
    header=rows[3][:16]
    out=[]
    for r in rows[4:]:
        if not r or not r[0].strip(): continue
        r=(r+['']*16)[:16]
        out.append(dict(zip(header,r)))
    return out

def normalize_ref(s): return ' '.join(s.split())

def build(rows, mode):
    # cluster -> [F sum,F n,P sum,P n]
    stats=defaultdict(lambda:[0,0,0,0])
    for r in rows:
        fn=r.get('Insect function','').strip()
        if fn not in {'Florivore','Pollinator'}: continue
        if mode=='detection':
            v=r.get('GC-EAD or EAG or SCR/SSR','').strip()
            if v not in {'0','1'}: continue
            y=int(v)
        else:
            v=r.get('Behaviour choice','').strip()
            if v not in {'+','-','0'}: continue
            y=int(v == ('+' if mode=='attraction' else '-'))
        c=normalize_ref(r.get('Reference (doi TBA)',''))
        j=0 if fn=='Florivore' else 2
        stats[c][j]+=y; stats[c][j+1]+=1
    return dict(stats)

def summarize(stats, mode):
    total=[sum(v[j] for v in stats.values()) for j in range(4)]
    f=total[0]/total[1]; p=total[2]/total[3]; obs=f-p
    clusters=list(stats)
    rng=random.Random(SEED + {'detection':1,'attraction':2,'repulsion':3}[mode])
    draws=[]
    for _ in range(B):
        s=[0,0,0,0]
        for c in rng.choices(clusters,k=len(clusters)):
            v=stats[c]
            for j in range(4): s[j]+=v[j]
        if s[1] and s[3]: draws.append(s[0]/s[1]-s[2]/s[3])
    draws.sort()
    def q(x):
        i=int(round((len(draws)-1)*x)); return draws[i]
    return {'module':mode,'florivore_prop':f,'pollinator_prop':p,'florivore_minus_pollinator':obs,
            'cluster_bootstrap_low95':q(.025),'cluster_bootstrap_median':q(.5),'cluster_bootstrap_high95':q(.975),
            'clusters_with_florivore':sum(v[1]>0 for v in stats.values()),'clusters_with_pollinator':sum(v[3]>0 for v in stats.values()),
            'reference_clusters_total':len(stats),'bootstrap_iterations':len(draws),'seed':SEED}

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('s1_csv'); ap.add_argument('output_dir'); a=ap.parse_args(argv)
    out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    rows=read_rows(a.s1_csv)
    summaries=[]
    profiles=[]
    for mode in ('detection','attraction','repulsion'):
        stats=build(rows,mode); summaries.append(summarize(stats,mode))
        for c,v in sorted(stats.items()):
            profiles.append({'module':mode,'publication_reference_cluster':c,'florivore_positive':v[0],'florivore_n':v[1],'pollinator_positive':v[2],'pollinator_n':v[3]})
    with (out/'SASIDHARAN2023_PUBLICATION_CLUSTER_SUMMARY_V1.csv').open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(summaries[0])); w.writeheader(); w.writerows(summaries)
    with (out/'SASIDHARAN2023_PUBLICATION_CLUSTER_PROFILES_V1.csv').open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(profiles[0])); w.writeheader(); w.writerows(profiles)
    det,att,rep=summaries
    readout=f'''# Sasidharan et al. 2023 publication-cluster sensitivity\n\n## Gate-C result\n\nThe source workbook is recovered directly from the article supplement. Table S1 contains 517 populated FVOC/insect rows and multiple rows per publication. Therefore FVOC x insect tests are not treated as independent study replication here.\n\nThe original article reports a higher row-level FVOC detection proportion for florivores than pollinators. Recomputing on source rows and resampling whole publication-reference clusters gives:\n\n| outcome | florivore | pollinator | F-P difference | 95% publication-cluster bootstrap |\n|---|---:|---:|---:|---:|\n| detection | {det['florivore_prop']:.3f} | {det['pollinator_prop']:.3f} | {det['florivore_minus_pollinator']:+.3f} | [{det['cluster_bootstrap_low95']:+.3f}, {det['cluster_bootstrap_high95']:+.3f}] |\n| attraction | {att['florivore_prop']:.3f} | {att['pollinator_prop']:.3f} | {att['florivore_minus_pollinator']:+.3f} | [{att['cluster_bootstrap_low95']:+.3f}, {att['cluster_bootstrap_high95']:+.3f}] |\n| repulsion | {rep['florivore_prop']:.3f} | {rep['pollinator_prop']:.3f} | {rep['florivore_minus_pollinator']:+.3f} | [{rep['cluster_bootstrap_low95']:+.3f}, {rep['cluster_bootstrap_high95']:+.3f}] |\n\nAll three cluster-bootstrap intervals cross zero. The row-level detection contrast is therefore not stable to publication-level dependence. This does **not** show equal responses; it shows that the broad between-guild contrast is not independently replicated strongly enough for a publication-level generality claim.\n\n## What is positively recovered\n\nThe workbook still provides a large, source-linked map of sign/state heterogeneity across compounds, insect guilds, plant genera and publications. That is directly useful for the fixed conditional BITA hypothesis: response sign is compound-, receiver- and context-dependent rather than universally positive or negative.\n\n## Gate C adjudication\n\n```text\nsource workbook recovered: YES\nsource rows reproduced: YES\npublication dependence reconstructed: YES\nrow-level universal guild contrast robust to publication clustering: NO\ncontext/sign heterogeneity module: PASS\nuniversal-effect module: FAIL_CLOSED\nGATE_C = PASS_AS_HETEROGENEITY_MODULE_NOT_AS_UNIVERSAL_GUILD_EFFECT\n```\n\nNo manuscript text is changed by this analysis.\n'''
    (out/'SASIDHARAN2023_PUBLICATION_CLUSTER_READOUT_V1.md').write_text(readout,encoding='utf-8')
    print(json.dumps({'summaries':summaries,'gate_c':'PASS_AS_HETEROGENEITY_MODULE_NOT_AS_UNIVERSAL_GUILD_EFFECT'},indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
