from pathlib import Path

path = Path('manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md')
text = path.read_text(encoding='utf-8')
old = '**Open Research statement:** Analysis code, source-adjudication products, and generated readouts are maintained in the public project repository. The exact immutable release, repository licence, and archival DOI for the submitted version are author-controlled release fields and will be inserted before submission.'
new = '**Open Research statement:** Analysis code, source-adjudication products, and generated readouts are maintained in the public project repository for peer review. Repository/software/data licence details are author-controlled submission fields where applicable. A permanent versioned archive of the accepted exact data/code release and its archival citation/DOI will be created at the acceptance stage.'
if text.count(old) != 1:
    raise SystemExit(f'expected exactly one Open Research statement target; found {text.count(old)}')
path.write_text(text.replace(old, new, 1), encoding='utf-8')
print('synchronized canonical Open Research statement')
