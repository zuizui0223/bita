import math
import numpy as np

from scripts.analyze_route_retention_extended_mle import (
    maximal_transport_face, fit_extended, joint_category_rank,
)


def test_boundary_forced_cell_not_conflated_with_nonrecorded_edge():
    # w1-b has an available opportunity but its row/column count margins
    # force its fitted intensity to zero.
    r=np.array([0,0,1],dtype=np.int32)
    c=np.array([0,1,1],dtype=np.int32)
    y=np.array([1.,0.,1.])
    face=maximal_transport_face(r,c,y,2,2)
    assert face.tolist()==[True,False,True]


def test_all_positive_edges_available_in_simple_transportation_matrix():
    r=np.array([0,0,1,1],dtype=np.int32)
    c=np.array([0,1,0,1],dtype=np.int32)
    y=np.ones(4)
    assert maximal_transport_face(r,c,y,2,2).all()


def test_extended_fit_identifiable_and_recovers_unit_category_ratios():
    cats=[[0,1,2],[2,0,1],[1,2,0]]
    records=[
        (f"w{i}",f"bird{j}@@site1",cats[i][j],1,f"plant{i}")
        for i in range(3) for j in range(3)
    ]
    rank=joint_category_rank(records)
    assert rank["joint_contrast_rank"]==2
    fit=fit_extended(records)
    assert fit["status"]=="FIT"
    assert fit["forced_zero_cells"]==0
    assert fit["max_margin_error"]<1e-9
    assert math.isclose(fit["rate_ratios"]["moderate_accessible"],1.,rel_tol=1e-7)
    assert math.isclose(fit["rate_ratios"]["severe_accessible"],1.,rel_tol=1e-7)
