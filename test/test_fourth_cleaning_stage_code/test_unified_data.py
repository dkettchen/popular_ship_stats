from src.fourth_stage_fixing_values_code.separate_names_into_parts import gather_all_raw_characters, remove_brackets, separate_name_parts
from src.fourth_stage_fixing_values_code.categorise_character_names import group_split_names_by_fandom, categorise_names
from src.fourth_stage_fixing_values_code.complete_character_names import make_unique_characters, complete_character_names
import pytest

@pytest.fixture(scope="class") # only running this mess once for this whole test suite bc heck
def complete_chars():
    all_raw_chars = gather_all_raw_characters()
    no_brackets = remove_brackets(all_raw_chars)
    separated_chars = separate_name_parts(no_brackets)
    grouped_chars = group_split_names_by_fandom(separated_chars)
    categorised_chars = categorise_names(grouped_chars)
    unique_chars = make_unique_characters(categorised_chars)
    complete_chars = complete_character_names(unique_chars)

    return complete_chars

@pytest.fixture(scope="class")
def rpf_fic(complete_chars):
    rpf = complete_chars["RPF"]
    fic = complete_chars["fictional"]
    return (rpf, fic)


@pytest.mark.skip
def test_does_not_mutate_inputs():
    all_raw_chars = gather_all_raw_characters()
    no_brackets = remove_brackets(all_raw_chars)
    separated_chars = separate_name_parts(no_brackets)
    grouped_chars = group_split_names_by_fandom(separated_chars)
    categorised_chars = categorise_names(grouped_chars)
    unique_chars = make_unique_characters(categorised_chars)

    assert all_raw_chars == gather_all_raw_characters()
    assert no_brackets == remove_brackets(all_raw_chars)
    assert separated_chars == separate_name_parts(no_brackets)
    assert grouped_chars == group_split_names_by_fandom(separated_chars)
    assert categorised_chars == categorise_names(grouped_chars)
    assert unique_chars == make_unique_characters(categorised_chars)

class TestOutputDict:

    def test_at_least_one_name_part_is_populated(self, rpf_fic):
        rpf_dict, fic_dict = rpf_fic
        name_parts = [
            "given_name", 
            "middle_name", 
            "maiden_name", 
            "surname", 
            "alias", 
            "nickname", 
            "title (prefix)", 
            "title (suffix)"
        ]
        for category in [rpf_dict, fic_dict]:
            for fandom in category:
                for character in category[fandom]:
                    has_name = False
                    for key in name_parts:
                        if category[fandom][character][key]:
                            has_name = True
                    assert has_name

    def test_full_name_string_is_present_and_not_empty(self, rpf_fic):
        rpf_dict, fic_dict = rpf_fic
        for category in [rpf_dict, fic_dict]:
            for fandom in category:
                for character in category[fandom]:
                    full_name = category[fandom][character]["full_name"]
                    assert type(full_name) == str
                    assert len(full_name) > 0

    def test_no_brackets_left_in_name(self, rpf_fic):
        rpf_dict, fic_dict = rpf_fic
        for category in [rpf_dict, fic_dict]:
            for fandom in category:
                for character in category[fandom]:
                    full_name = category[fandom][character]["full_name"]
                    if full_name not in [
                        "Connor (RK800)",
                        "Connor (RK900)",
                        "Venom (Symbiote)"
                    ]:
                        assert "(" not in full_name and ")" not in full_name

    def test_no_obvious_double_names_left(self, rpf_fic):
        rpf_dict, fic_dict = rpf_fic
        for category in [rpf_dict, fic_dict]:
            for fandom in category:
                key_list = list(category[fandom].keys())
                key_set = set(key_list)
                assert len(key_list) == len(key_set)

    def test_collects_unique_original_versions(self, rpf_fic):
        rpf_dict, fic_dict = rpf_fic
        for category in [rpf_dict, fic_dict]:
            for fandom in category:
                for character in category[fandom]:
                    op_versions = category[fandom][character]["op_versions"]
                    assert type(op_versions) == list
                    assert len(op_versions) >= 1
                    assert len(op_versions) == len(set(op_versions))


# format of final dict? just to make sure
# we didn't lose any fandoms (check against clean fandoms list)
# we didn't lose any characters (check against old versions I guess)




# boo boring, no, later maybe:

# test output data rather than individual functions leading to it
# get data from files to test

#main data:
# correct output format
# maintained length of ranking data, we didn't lose any data
# all names of fandoms have been replaced with new clean ones
# all character names have been replaced with new clean ones
# RPF is tagged as such
# items in row are expected format
# replaced names are expected format (eg no brackets etc)

#additional data in helper files:
    # fandoms
# correct output format (keys etc)
# all fandoms are present (check all ranking data against op versions??)
# items in row are expected format
# row contains additional fandom info
    # characters
# correct output format (keys etc)
# all characters are present
    # check fandoms against fandoms w characters against characters files
    # ->  if we've determined the correct length of fandoms list
            # fandoms w characters should have same length
        # if we've removed all duplicate characters
        # and no fandoms are like obviously missing their characters
            # fandoms should have their correct amount of characters
            # and therefore the total number of those characters
            # should be the amount of characters in character file
# all characters are associated with the correct fandoms
# items in row are expected format
# row contains additional character info
# added info is up to date