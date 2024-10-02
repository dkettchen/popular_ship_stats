from visualisation.df_making_functions.retrieve_numbers import get_total_items, get_unique_values_list
import pandas as pd
import pytest

@pytest.fixture
def test_df():
    """
    makes a df with dummy data

    "year" has a mix of floats and ints
    "strings" has strings
    """
    df = pd.DataFrame(
        columns=["year", "strings"],
        data={
            "year": [2015.0, 2018, 2020.0, 2013, 2015, 2020, 2007],
            "strings": ["white", "black", "e asian", "white", "s asian", "e asian", "white"]
        }
    )

    return df


class TestUniqueValuesList:
    def test_returns_list(self, test_df):
        result = get_unique_values_list(test_df, "strings")
        assert type(result) == list

    def test_does_not_mutate_input(self, test_df):
        copy_df = test_df.copy()
        get_unique_values_list(test_df, "strings")
        assert copy_df.shape == test_df.shape
        assert list(copy_df.columns) == list(test_df.columns)
        assert list(copy_df.year) == list(test_df.year)
        assert list(copy_df["strings"]) == list(test_df["strings"])

    def test_list_contains_less_items_than_input(self, test_df):
        result = get_unique_values_list(test_df, "strings")
        assert len(result) < len(test_df["strings"])

    def test_list_contains_unique_items(self, test_df):
        result = get_unique_values_list(test_df, "strings")
        assert len(result) == len(set(result))

    def test_raises_key_error_when_column_not_in_df(self, test_df):
        with pytest.raises(KeyError):
            assert get_unique_values_list(test_df, "who?")

class TestTotalItems:
    def test_returns_int(self, test_df):
        result = get_total_items(test_df, "strings")
        assert type(result) == int
    
    def test_does_not_mutate_input(self, test_df):
        copy_df = test_df.copy()
        get_total_items(test_df, "strings")
        assert copy_df.shape == test_df.shape
        assert list(copy_df.columns) == list(test_df.columns)
        assert list(copy_df.year) == list(test_df.year)
        assert list(copy_df["strings"]) == list(test_df["strings"])
    
    def test_returns_number_of_unique_items_in_given_column(self, test_df):
        result = get_total_items(test_df, "strings")
        assert result == 4

        result_2 = get_total_items(test_df, "year")
        assert result_2 == 5
    
    def test_raises_key_error_when_column_not_in_df(self, test_df):
        with pytest.raises(KeyError):
            assert get_total_items(test_df, "who?")