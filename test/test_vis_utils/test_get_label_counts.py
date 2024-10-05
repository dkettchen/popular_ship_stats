from visualisation.vis_utils.df_utils.retrieve_numbers import get_label_counts, find_full_column, get_unique_values_list
import pandas as pd
import pytest

@pytest.fixture
def test_df():
    """
    makes a df with dummy data

    "year" has a mix of floats and ints
    "strings" has strings
    "other_values" contains some none values
    """
    df = pd.DataFrame(
        columns=["year", "strings", "other_values", "another_full_column"],
        data={
            "year": [2015.0, 2018, 2020.0, 2013, 2015, 2020, 2007],
            "strings": ["white", "black", "e asian", "white", "s asian", "e asian", "white"],
            "other_values": [2,3,4,5,None,2,None],
            "another_full_column": ["a", "b", "c", "d", "e", "f", "g"]
        }
    )

    return df


class TestFullColumn:
    def test_returns_string(self, test_df):
        result = find_full_column(test_df, "strings")
        assert type(result) == str
    
    def test_does_not_mutate_input(self, test_df):
        copy_df = test_df.copy()
        find_full_column(test_df, "strings")
        assert copy_df.shape == test_df.shape
        assert list(copy_df.columns) == list(test_df.columns)
        assert list(copy_df.year) == list(test_df.year)
        assert list(copy_df["strings"]) == list(test_df["strings"])
        assert list(copy_df["other_values"].dropna()) == list(test_df["other_values"].dropna()) # it was 
        # throwing an error cause it thought nan != nan and I'm like- that's literally the same thing??

    def test_returns_column_name_from_given_df(self, test_df):
        result = find_full_column(test_df, "strings")
        assert result in test_df.columns
    
    def test_returns_column_name_other_than_column_name(self, test_df):
        result = find_full_column(test_df, "strings")
        assert result != "strings"

    def test_returns_column_name_without_null_values(self, test_df):
        result = find_full_column(test_df, "strings")
        assert result != "other_values"

    def test_returns_none_if_there_is_no_other_full_column(self, test_df):
        new_df = test_df.copy()
        new_df.pop("year")
        new_df.pop("another_full_column")
        result = find_full_column(new_df, "strings")
        assert result == None

    def test_raises_keyerror_if_passed_key_not_in_df(self, test_df):
        with pytest.raises(KeyError):
            assert find_full_column(test_df, "who?")

class TestLabelCounts:
    def test_returns_series(self, test_df):
        result = get_label_counts(test_df, "strings")
        assert type(result) == pd.Series

    def test_does_not_mutate_input(self, test_df):
        copy_df = test_df.copy()
        get_label_counts(test_df, "strings")
        assert copy_df.shape == test_df.shape
        assert list(copy_df.columns) == list(test_df.columns)
        assert list(copy_df.year) == list(test_df.year)
        assert list(copy_df["strings"]) == list(test_df["strings"])
        assert list(copy_df["other_values"].dropna()) == list(test_df["other_values"].dropna())

    def test_returns_index_of_unique_labels_from_given_column(self, test_df):
        result = get_label_counts(test_df, "strings")
        assert sorted(list(result.index)) == sorted(get_unique_values_list(test_df, "strings"))

    def test_returns_numerical_values(self, test_df):
        result = get_label_counts(test_df, "strings")
        assert result.dtype == "int64"
    
    def test_counts_each_label(self, test_df):
        result = get_label_counts(test_df, "strings")
        count_series = pd.Series(
            index=["black", "e asian", "s asian", "white"],
            data={"black":1, "e asian":2, "s asian":1, "white":3}
        )
        assert list(result.index) == list(count_series.index)
        assert list(result.values) == list(count_series.values)
    
    def test_works_with_given_count_column(self, test_df):
        result = get_label_counts(test_df, "strings")
        result_2 = get_label_counts(test_df, "strings", "another_full_column")
        result_3 = get_label_counts(test_df, "strings", "year")
        assert list(result.index) == list(result_2.index)
        assert list(result.values) == list(result_2.values)
        assert list(result.index) == list(result_3.index)
        assert list(result.values) == list(result_3.values)
    
    def test_finds_different_column_if_given_count_column_contains_null_values(self, test_df):
        result = get_label_counts(test_df, "strings")
        result_2 = get_label_counts(test_df, "strings", "other_values")
        assert list(result.index) == list(result_2.index)
        assert list(result.values) == list(result_2.values)

    def test_returns_accurate_counts_even_if_no_full_columns_outside_of_given_column(self, test_df):
        result = get_label_counts(test_df, "strings")

        new_df = test_df.copy()
        new_df.pop("year")
        new_df.pop("another_full_column")
        result_2  = get_label_counts(new_df, "strings")

        assert type(result) == type(result_2)
        assert list(result.index) == list(result_2.index)
        assert list(result.values) == list(result_2.values)
    
    def test_raises_keyerror_if_passed_key_not_in_df(self, test_df):
        with pytest.raises(KeyError):
            assert get_label_counts(test_df, "who?")
    
    