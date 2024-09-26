from visualisation.vis_utils.make_name_string import make_name_string

def test_returns_string():
    test_list = ["Mario", "Princess Peach", "Bowser", "Toad"]
    result = make_name_string(test_list)
    assert type(result) == str

def test_does_not_mutate_input():
    test_list = ["Mario", "Princess Peach", "Bowser", "Toad"]
    make_name_string(test_list)
    assert test_list == ["Mario", "Princess Peach", "Bowser", "Toad"]

def test_returns_empty_string_for_empty_list():
    result = make_name_string([])
    assert result == ""

def test_returns_single_name_as_is():
    test_list = ["Mario"]
    result = make_name_string(test_list)
    assert result == "Mario"

def test_returns_string_containing_given_names():
    test_list = ["Mario", "Princess Peach", "Bowser", "Toad"]
    result = make_name_string(test_list)
    for name in test_list:
        assert name in result

def test_returns_string_containing_ampercent():
    test_list = ["Mario", "Princess Peach", "Bowser", "Toad"]
    result = make_name_string(test_list)
    assert " & " in result

def test_returns_string_ending_in_tied():
    test_list = ["Mario", "Princess Peach", "Bowser", "Toad"]
    result = make_name_string(test_list)
    assert result[-7:] == " (tied)"

def test_returns_names_concated_string():
    test_list = ["Mario", "Princess Peach", "Bowser", "Toad"]
    result = make_name_string(test_list)
    assert result == "Mario & Princess Peach & Bowser & Toad (tied)"