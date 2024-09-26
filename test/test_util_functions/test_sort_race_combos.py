from visualisation.vis_utils.sort_race_combos import sort_race_combos

def test_returns_dict():
    test_input = ["White", "S Asian / Black", "MENA / White", "White / E Asian (multi)"]
    result = sort_race_combos(test_input)
    assert type(result) == dict

def test_does_not_mutate_input():
    test_input = ["S Asian / Black", "White / E Asian (multi)"]
    sort_race_combos(test_input)
    assert test_input == ["S Asian / Black", "White / E Asian (multi)"]

def test_returns_empty_dict_for_no_changes():
    test_input = ["White", "MENA / White"]
    result = sort_race_combos(test_input)
    assert result == {}

def test_returns_correctly_reconcated_string_value_for_unordered_keys():
    test_input = ["S Asian / Black"]
    result = sort_race_combos(test_input)
    assert result["S Asian / Black"] == "Black / S Asian"

def test_returns_alphabetically_ordered_values_for_unordered_keys():
    test_input = ["S Asian / Black", "White / E Asian (multi)"]
    result = sort_race_combos(test_input)
    assert list(result.keys()) == ["S Asian / Black", "White / E Asian (multi)"]
    assert list(result.values()) == ["Black / S Asian", "E Asian (multi) / White"]

def test_returns_appropriate_dict_entries_for_mixed_case_input():
    test_input = ["S Asian / Black", "White", "MENA / White", "White / E Asian (multi)"]
    result = sort_race_combos(test_input)
    assert list(result.keys()) == ["S Asian / Black", "White / E Asian (multi)"]
    assert list(result.values()) == ["Black / S Asian", "E Asian (multi) / White"]
