from visualisation.vis_utils.df_utils.make_dfs import sort_df
import pandas as pd
import pytest

@pytest.fixture
def test_df():
    """
    makes a df with dummy data

    "year" has a mix of floats and ints
    "ints" has integers
    "strings" has strings
    """
    df = pd.DataFrame(
        columns=["year", "ints", "strings"],
        data={
            "year": [2015.0, 2018, 2020.0, 2013, 2015, 2020],
            "ints": [7,8,2,6,9,14],
            "strings": ["why", "hello", "there", "champ", "how's it", "going"]
        }
    )

    return df


def test_returns_dataframe(test_df):
    result = sort_df(test_df, "year")
    assert type(result) == pd.DataFrame

def test_returns_new_df(test_df):
    result = sort_df(test_df, "year")
    assert result is not test_df

def test_does_not_mutate_input(test_df):
    copy_df = test_df.copy()
    sort_df(test_df, "year")
    assert copy_df.shape == test_df.shape
    assert list(copy_df.columns) == list(test_df.columns)
    assert list(copy_df.year) == list(test_df.year)
    assert list(copy_df["ints"]) == list(test_df["ints"])
    assert list(copy_df["strings"]) == list(test_df["strings"])

def test_returns_df_of_same_shape(test_df):
    result = sort_df(test_df, "year")
    assert result.shape == test_df.shape

def test_returns_df_with_values_of_given_column_sorted(test_df):
    result = sort_df(test_df, "year", asc=True)
    assert list(result["year"]) == sorted(list(result["year"]))

def test_sorts_descending_by_default(test_df):
    result = sort_df(test_df, "year")
    assert list(result["year"]) == sorted(list(result["year"]), reverse=True)

def test_sorts_index_by_default(test_df):
    test_df = test_df.set_index("ints")
    assert list(test_df.index) == [7,8,2,6,9,14]
    result = sort_df(test_df)
    assert list(result.index) == sorted([7,8,2,6,9,14], reverse=True)

def test_raises_key_error_if_column_not_in_df(test_df):
    with pytest.raises(KeyError):
        assert sort_df(test_df, "who?")
