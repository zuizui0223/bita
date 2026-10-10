from scripts.diagnose_route_retention_poisson_mle_existence import Cell, positive_margin_lp


def cell(waypoint, bird, value, site="siteA", cat=0):
    return Cell(waypoint=waypoint, bird=bird, site=site,
                plant=waypoint, category=cat,
                robbery=value, legitimate=value)


def test_positive_margin_interior_when_all_supported_cells_used():
    rows = [
        cell("w1","a",1),cell("w1","b",1),
        cell("w2","a",1),cell("w2","b",1),
    ]
    res = positive_margin_lp(rows,route="robbery",bird_site=True,
                             include_category=False)
    assert res["status"] == "STRICTLY_POSITIVE_FEASIBLE"
    assert res["positive_margin_supported_edges"] == 4
    assert res["max_common_positive_mean"] > 0.9


def test_positive_row_and_column_margins_can_still_force_zero_cell():
    # Margins: w2 has only b and contributes 1; bird b's total is 1.
    # Therefore w1-b is forced to expected 0 despite its allowed edge.
    rows = [
        cell("w1","a",1),
        cell("w1","b",0),
        cell("w2","b",1),
    ]
    res = positive_margin_lp(rows,route="robbery",bird_site=True,
                             include_category=False)
    assert res["status"] == "BOUNDARY_SEPARATION"
    assert res["positive_margin_supported_edges"] == 3
    assert abs(res["max_common_positive_mean"]) < 1e-7


def test_category_constraint_can_be_removed_without_changing_fe_support():
    rows = [
        cell("w1","a",1,cat=0),
        cell("w1","b",0,cat=1),
        cell("w2","b",1,cat=2),
    ]
    res = positive_margin_lp(rows,route="legitimate",bird_site=False,
                             include_category=False)
    assert res["status"] == "BOUNDARY_SEPARATION"
