from src.util_functions.make_ship_tag import make_ship_tag

def test_does_not_mutate_input():
    characters = ["Princess Peach", "Princess Daisy"]
    fic_type = "slash"
    make_ship_tag(characters, fic_type)
    assert characters == ["Princess Peach", "Princess Daisy"]
    assert fic_type == "slash"

def test_returns_string():
    result = make_ship_tag(["Princess Peach", "Princess Daisy"], "slash")
    assert type(result) == str

def test_returns_new_string():
    result = make_ship_tag(["Princess Peach", "Princess Daisy"], "slash")
    assert result != "slash"

def test_returns_list_item_for_single_item_list():
    result = make_ship_tag(["Princess Peach"], "slash")
    assert result == "Princess Peach"

def test_ship_tag_contains_items_from_list():
    characters = ["Princess Peach", "Princess Daisy"]
    result = make_ship_tag(characters, "slash")
    for char in characters:
        assert char in result

def test_ship_tag_is_longer_than_any_list_item_if_more_than_one_item_in_list():
    characters = ["Princess Peach", "Princess Daisy"]
    result = make_ship_tag(characters, "slash")
    length = len(result)
    for char in characters:
        assert length > len(char)

def test_ship_tag_contains_ampercent_for_gen_ships():
    result = make_ship_tag(["Princess Peach", "Princess Daisy"], "gen")
    assert " & " in result

def test_ship_type_is_case_insensitive():
    result = make_ship_tag(["Princess Peach", "Princess Daisy"], "GeN")
    assert " & " in result

def test_ship_tag_contains_x_for_any_other_ship_type():
    result_1 = make_ship_tag(["Princess Peach", "Princess Daisy"], "slash")
    assert " x " in result_1
    result_2 = make_ship_tag(["Princess Peach", "Bowser"], "they're married!")
    assert " x " in result_2

def test_characters_have_been_sorted_alphabetically():
    result = make_ship_tag(["Princess Peach", "Princess Daisy"], "slash")
    assert result == "Princess Daisy x Princess Peach"

def test_appends_characters_with_separator_between_them_for_more_than_2_chars():
    result = make_ship_tag(["Luigi", "Princess Peach", "Mario", "Princess Daisy"], "slash")
    assert result == "Luigi x Mario x Princess Daisy x Princess Peach"
