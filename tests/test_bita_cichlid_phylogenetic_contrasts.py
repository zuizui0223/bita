"""Phylogenetic-contrast implementation tests use synthetic tree and traits.

Real 88-species source checks are mandatory in the dedicated GitHub action;
synthetic toy data are never presented as observed biological confirmation.
"""
from __future__ import annotations

import math

import pytest

from scripts import analyze_bita_cichlid_phylogenetic_contrasts as pic


def test_parse_four_species_original_branch_lengths_and_exact_pic():
    root=pic.parse_newick("((A:1,B:1):1,(C:1,D:1):1);")
    traits={"A":[0.0],"B":[2.0],"C":[1.0],"D":[1.0]}
    assert pic.tips(root)==set(traits)
    computed=pic.contrasts(root,traits)
    assert len(computed)==3
    assert computed[0][0]==pytest.approx(-math.sqrt(2))
    assert computed[1][0]==pytest.approx(0)
    assert computed[2][0]==pytest.approx(0)


def test_phylo_restricted_tree_collapses_unsampled_branches_correctly():
    root=pic.parse_newick("((A:1,B:2):3,(C:4,D:5):6);")
    restricted=pic.prune(root,{"A","B","C"})
    assert pic.tips(restricted)=={"A","B","C"}
    assert len(pic.contrasts(restricted,{
        "A":[1.0],"B":[2.0],"C":[3.0]
    }))==2
    root.children[0].children[0].length=99
    assert restricted.children[0].children[0].length==1.0  # independent copy


def test_pic_source_registration_matches_2021_original_author_archive():
    assert pic.SOURCE_COMMIT=="575a148a6c6cb90ee957d4290cf3e2d141ca9c14"
    assert pic.TREE["blob_sha1"]=="23076ac2c895a92aaf36cebfa059124ec1139bd7"
    assert pic.TREE["bytes"]==76749
    assert pic.source_tree_url().endswith("/MacroevolutionSetUp/CichlidTreeNature2020.tre")


@pytest.mark.parametrize("bad",[
    "(A:1,B:1)",
    "(A:1,B:1); stray",
    "(A:1,B:inf);",
    "(A:-1,B:1);",
    "(A:1,A:2);",
    "(A:1,B:broken);",
])
def test_fails_closed_for_bad_newick(bad):
    with pytest.raises(ValueError):
        pic.parse_newick(bad)


def test_missing_species_and_polytomy_fail_closed():
    root=pic.parse_newick("((A:1,B:1):1,C:1);")
    with pytest.raises(ValueError,match="MISSING"):
        pic.prune(root,{"A","B","C","D"})
    multi=pic.parse_newick("(A:1,B:1,C:1);")
    with pytest.raises(ValueError,match="NONBINARY"):
        pic.contrasts(multi,{"A":[1],"B":[2],"C":[3]})


def test_zero_contrast_variance_refused():
    root=pic.parse_newick("(A:0,B:0);")
    with pytest.raises(ValueError,match="DEGENERATE"):
        pic.contrasts(root,{"A":[1],"B":[2]})


def test_RV_uses_whole_module_pic_vectors_and_reproducible_permutation():
    # 8 tips supply 7 contrasts. Identical modules retain RV=1.
    newick="(((A:1,B:1):1,(C:1,D:1):1):1,((E:1,F:1):1,(G:1,H:1):1):1);"
    tree=pic.parse_newick(newick)
    traits={
        chr(65+i):[
            ((i*3+j*5)%(j+7)-2*j)/5+math.sin((i+1)*(j+1)*.35)
            for j in range(5)
        ] for i in range(8)
    }
    contrasts=pic.contrasts(tree,traits)
    assert len(contrasts)==7
    a=pic.permuted_pic_rv(contrasts,contrasts,axes=3,permutations=99)
    b=pic.permuted_pic_rv(contrasts,contrasts,axes=3,permutations=99)
    assert a==b
    assert a["rv_pic"]==pytest.approx(1,abs=1e-10)
    assert a["permutation_p"]>=.01
    assert a["n_independent_contrasts"]==7


def test_no_uninformative_axis_or_inadequate_contrasts():
    with pytest.raises(ValueError,match="NOT_ENOUGH"):
        pic.standardize_rows([[1,2],[2,3]],2)
    with pytest.raises(ValueError,match="UNINFORMATIVE"):
        pic.standardize_rows([[1,0]]*7,2)
    with pytest.raises(ValueError,match="NO_PERMUTATIONS"):
        pic.permuted_pic_rv([[1,2]]*7,[[1,2]]*7,axes=2,permutations=0)


def test_post_open_branch_length_sensitivity_changes_only_tree_model():
    root=pic.parse_newick("((A:1,B:1):3,(C:2,D:2):4);")
    baseline=pic.contrasts(root,{"A":[2.0],"B":[1.0],"C":[0.0],"D":[3.0]})
    equal=pic.alter_branch_model(root,"equal_edge_lengths")
    terminal=pic.alter_branch_model(root,"double_terminal_lengths")
    assert pic.tips(root)==pic.tips(equal)==pic.tips(terminal)
    assert equal.children[0].length==pytest.approx(1)
    assert terminal.children[0].length==pytest.approx(3)
    assert terminal.children[0].children[0].length==pytest.approx(2)
    assert root.children[0].children[0].length==pytest.approx(1)
    assert pic.contrasts(terminal,{"A":[2.0],"B":[1.0],"C":[0.0],"D":[3.0]}) != baseline
    with pytest.raises(ValueError,match="UNREGISTERED"):
        pic.alter_branch_model(root,"pretend_BM_fit")
