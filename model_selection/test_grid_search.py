from model_selection import grid_search
from xgboost.sklearn import XGBClassifier


def test_grid_search_generator():
    # check if generating the right number of grids
    grids = {'max_depth': [2, 3], 'min_child_weight': [1, 2]}
    gen = grid_search.grid_search_generator(XGBClassifier, grids)
    count = 0
    for clf in gen:
        count += 1
    assert count == 4
