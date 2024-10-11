from visualisation.vis_utils.df_utils.hottest_char_utils import find_tied_fandoms
import pandas as pd
import pytest

# mock df with "fandom" & "no_of_ships_they_in" columns
@pytest.fixture
def test_df():
    """
    makes a df with dummy data
    """
    df = pd.DataFrame(
        columns=["full_name", "fandom", "no_of_ships_they_in"],
        data={
            "full_name": [
                "Tony Stark", "Steve Rogers", 
                "Princess Peach", "Princess Daisy", "Bowser", "Mario", 
                "Calder", "Callie", "Sol",
                "Superman", "Batman",
            ],
            "fandom": [
                "Marvel", "Marvel",
                "Mario", "Mario", "Mario", "Mario", 
                "NADDpod", "NADDpod", "NADDpod", 
                "DC", "DC",
            ], 
            "no_of_ships_they_in": [
                7, 3,
                2, 4, 5, 2,
                3, 3, 3,
                1, 1,
            ]
        }
    )

    return df


def test_returns_list(test_df):
    result = find_tied_fandoms(test_df)
    assert type(result) == list

def test_does_not_mutate_input(test_df):
    copy_df = test_df.copy()
    find_tied_fandoms(test_df)
    assert type(test_df) == type(copy_df)
    assert test_df.shape == copy_df.shape
    assert list(test_df.columns) == list(copy_df.columns)
    assert list(test_df["full_name"]) == list(copy_df["full_name"])
    assert list(test_df["fandom"]) == list(copy_df["fandom"])
    assert list(test_df["no_of_ships_they_in"]) == list(copy_df["no_of_ships_they_in"])


def test_list_does_not_contain_non_tied_fandoms(test_df):
    result = find_tied_fandoms(test_df)
    assert "Marvel" not in result
    assert "Mario" not in result

def test_list_does_not_contain_fandoms_with_only_one_ship(test_df):
    result = find_tied_fandoms(test_df)
    assert "DC" not in result

def test_list_contains_tied_fandoms(test_df):
    result = find_tied_fandoms(test_df)
    assert "NADDpod" in result
    assert len(result) == 1