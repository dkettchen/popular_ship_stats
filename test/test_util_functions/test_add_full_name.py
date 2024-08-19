from src.util_functions.add_full_name import add_full_name
import pytest

@pytest.fixture
def character_dicts():
    falin_touden = {
        "given_name": "Falin",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Touden",
        "alias": None,
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": "W",
        "full_name": None,
        "fandom": "Delicious in Dungeon | ダンジョン飯",
        "op_versions": ["Falin (Dungeon Meshi)"]
    }
    wonder_woman = {
        "given_name": "Diana",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Prince",
        "alias": "Wonder Woman",
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": "W",
        "full_name": None,
        "fandom": "DC",
        "op_versions": ["Diana Prince"]
    }
    l_death_note = {
        "given_name": None,
        "middle_name": None,
        "maiden_name": None,
        "surname": None,
        "alias": "L",
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": None,
        "full_name": None,
        "fandom": "Death Note | デスノート",
        "op_versions": ["L (Death Note)"]
    }
    uzui_tengen = {
        "given_name": "Tengen",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Uzui",
        "alias": "Sound Hashira",
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": "E",
        "full_name": None,
        "fandom": "Demon Slayer | 鬼滅の刃",
        "op_versions": ["Tengen"]
    }
    spock = {
        "given_name": None,
        "middle_name": None,
        "maiden_name": None,
        "surname": None,
        "alias": None,
        "nickname": "Spock",
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": None,
        "full_name": None,
        "fandom": "Star Trek",
        "op_versions": [
            "Spock"
        ]
    }
    kylo_ren ={
        "given_name": "Ben",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Solo",
        "alias": "Kylo",
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": "Ren",
        "name_order": "W",
        "full_name": None,
        "fandom": "Star Wars",
        "op_versions": [
            "Ben Solo | Kylo Ren",
            "Kylo Ren"
        ]
    }
    darth_vader = {
        "given_name": "Anakin",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Skywalker",
        "alias": "Vader",
        "nickname": None,
        "title (prefix)": "Darth",
        "title (suffix)": None,
        "name_order": "W",
        "full_name": None,
        "fandom": "Star Wars",
        "op_versions": [
            "Anakin Skywalker | Darth Vader"
        ]
    }
    zoro = {
        "given_name": "Zoro",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Roronoa",
        "alias": "Pirate Hunter",
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": "E",
        "full_name": None,
        "fandom": "One Piece | \u30ef\u30f3\u30d4\u30fc\u30b9",
        "op_versions": [
            "Roronoa Zoro"
        ]
    }
    sanji = {
        "given_name": "Sanji",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Vinsmoke",
        "alias": "Black-Leg",
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": "W",
        "full_name": None,
        "fandom": "One Piece | \u30ef\u30f3\u30d4\u30fc\u30b9",
        "op_versions": [
            "Vinsmoke Sanji"
        ]
    }
    kate_bridgerton = {
        "given_name": "Kate",
        "middle_name": None,
        "maiden_name": "Sheffield/Sharma",
        "surname": "Bridgerton",
        "alias": None,
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": "W",
        "full_name": None,
        "fandom": "Bridgerton",
        "op_versions": [
            "Kate Sheffield | Kate Sharma"
        ]
    }
    capt_hook = {
        "given_name": "Killian",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Jones",
        "alias": "Hook",
        "nickname": None,
        "title (prefix)": "Captain",
        "title (suffix)": None,
        "name_order": "W",
        "full_name": None,
        "fandom": "Once Upon a Time",
        "op_versions": [
            "Captain Hook | Killian Jones"
        ]
    }
    mccoy = {
        "given_name": "Leonard",
        "middle_name": None,
        "maiden_name": None,
        "surname": "McCoy",
        "alias": None,
        "nickname": "'Bones'",
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": "W",
        "full_name": None,
        "fandom": "Star Trek",
        "op_versions": [
            "Leonard 'Bones' McCoy",
            "Leonard McCoy"
        ]
    }

    look_up = {
        "Falin Touden" : falin_touden,
        "Diana Prince | Wonder Woman" : wonder_woman,
        "L" : l_death_note,
        "Uzui Tengen | Sound Hashira" : uzui_tengen,
        "Spock" : spock,
        "Ben Solo | Kylo Ren" : kylo_ren,
        "Anakin Skywalker | Darth Vader" : darth_vader,
        "Roronoa Zoro | Pirate Hunter Zoro" : zoro,
        "Sanji Vinsmoke | Black-Leg Sanji" : sanji,
        "Kate Bridgerton, née Sheffield/Sharma" : kate_bridgerton,
        "Killian Jones | Captain Hook" : capt_hook,
        "Leonard 'Bones' McCoy" : mccoy,
    }
    return look_up


def test_does_not_mutate_input(character_dicts):
    expected = {
        "given_name": "Falin",
        "middle_name": None,
        "maiden_name": None,
        "surname": "Touden",
        "alias": None,
        "nickname": None,
        "title (prefix)": None,
        "title (suffix)": None,
        "name_order": "W",
        "full_name": None,
        "fandom": "Delicious in Dungeon | ダンジョン飯",
        "op_versions": ["Falin (Dungeon Meshi)"]
    }
    add_full_name(character_dicts["Falin Touden"])
    assert character_dicts["Falin Touden"] == expected

def test_returns_same_amount_of_keys_as_input(character_dicts):
    for char in character_dicts:
        result = add_full_name(character_dicts[char])
        assert len(result.keys()) == len(character_dicts[char].keys())

def test_returns_same_key_names_as_input(character_dicts):
    for char in character_dicts:
        result = add_full_name(character_dicts[char])
        assert result.keys() == character_dicts[char].keys()

def test_returns_unused_keys_unchanged(character_dicts):
    for char in character_dicts:
        result = add_full_name(character_dicts[char])
        for key in result:
            if key not in [
                "given_name", 
                "middle_name", 
                "maiden_name", 
                "surname", 
                "alias", 
                "nickname", 
                "title (prefix)", 
                "title (suffix)", 
                "name_order", 
                "full_name", 
                "fandom"
            ]:
                assert result[key] == character_dicts[char][key]

def test_returns_used_keys_except_nick_and_full_unchanged(character_dicts):
    for char in character_dicts:
        result = add_full_name(character_dicts[char])
        for key in result:
            if key not in ["full_name", "nickname"]:
                assert result[key] == character_dicts[char][key]

def test_removes_quotes_from_nick_where_present(character_dicts):
    result = add_full_name(character_dicts["Leonard 'Bones' McCoy"])
    assert character_dicts["Leonard 'Bones' McCoy"]["nickname"] == "'Bones'"
    assert result["nickname"] == "Bones"

def test_does_not_change_quoteless_nicks(character_dicts):
    clean_nick = character_dicts["Spock"]
    result = add_full_name(clean_nick)
    assert result["nickname"] == "Spock"
    assert result["nickname"] == clean_nick["nickname"]

def test_returns_single_nicks_and_aliases_without_other_characters(character_dicts):
    spock = add_full_name(character_dicts["Spock"])
    assert "'" not in spock["full_name"]
    assert spock["full_name"] == "Spock"

    eru = add_full_name(character_dicts["L"])
    assert "|" not in eru["full_name"]
    assert eru["full_name"] == "L"

def test_overwrites_full_name_value_with_string(character_dicts):
    for char in character_dicts:
        assert character_dicts[char]["full_name"] == None
        result = add_full_name(character_dicts[char])
        assert result["full_name"] != None
        assert type(result["full_name"]) == str
    
    character_dicts["L"]["full_name"] = "'Laurence or something probably' - Kira"
    take_the_L_kira = add_full_name(character_dicts["L"])
    assert take_the_L_kira["full_name"] != "'Laurence or something probably' - Kira"
    assert take_the_L_kira["full_name"] == "L"

def test_returns_full_name_in_correct_order(character_dicts):
    for char in character_dicts:
        if char not in [
            "Ben Solo | Kylo Ren",
            "Anakin Skywalker | Darth Vader",
            "Roronoa Zoro | Pirate Hunter Zoro",
            "Sanji Vinsmoke | Black-Leg Sanji",
            "Killian Jones | Captain Hook"
        ]:
            assert character_dicts[char]["full_name"] == None
            result = add_full_name(character_dicts[char])
            assert result["full_name"] == char

def test_returns_exceptions_formatted_correctly(character_dicts):
    for char in character_dicts:
        if char in [
            "Ben Solo | Kylo Ren",
            "Anakin Skywalker | Darth Vader",
            "Roronoa Zoro | Pirate Hunter Zoro",
            "Sanji Vinsmoke | Black-Leg Sanji",
            "Killian Jones | Captain Hook"
        ]:
            assert character_dicts[char]["full_name"] == None
            result = add_full_name(character_dicts[char])
            assert result["full_name"] == char

