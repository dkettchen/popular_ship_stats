from visualisation.vis_utils.df_utils.make_dfs import get_year_df
import pandas as pd
import pytest

@pytest.fixture
def test_df():
    """
    makes a df with dummy data, containing a year & data column

    the year column contains ints as well as floats (and has been tested with only ints first)
    """
    df = pd.DataFrame(
        columns=["year", "data"],
        data={
            "year": [2015.0, 2018, 2020.0, 2013, 2004, 2023, 2024, 2010, 2020, 2013, 2006, 2020, 2015, 2013],
            "data": [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        }
    )

    return df


def test_returns_dataframe(test_df):
    result = get_year_df(test_df, 2020)
    assert type(result) == pd.DataFrame

def test_returns_new_df(test_df):
    result = get_year_df(test_df, 2020)
    assert result is not test_df

def test_does_not_mutate_input(test_df):
    copy_df = test_df.copy()
    get_year_df(test_df, 2020)
    assert copy_df.shape == test_df.shape
    assert list(copy_df.columns) == list(test_df.columns)
    assert list(copy_df.year) == list(test_df.year)
    assert list(copy_df["data"]) == list(test_df["data"])

def test_returns_empty_df_if_year_not_in_df(test_df):
    result = get_year_df(test_df, 2030)
    assert len(result) == 0
    assert type(result) == pd.DataFrame

def test_returns_df_with_only_one_year_value(test_df):
    result = get_year_df(test_df, 2020)
    assert len(result["year"].unique()) == 1

def test_returns_df_with_only_requested_year_values(test_df):
    result = get_year_df(test_df, 2020)
    assert set(result["year"]) == {2020}

def test_returns_df_with_corresponding_data_from_other_columns(test_df):
    result = get_year_df(test_df, 2020)
    assert list(result["data"]) == [3, 9, 12]

def test_works_with_floats_too(test_df):
    result = get_year_df(test_df, 2020.0)
    assert int(list(set(result["year"]))[0]) == 2020
    assert list(result["data"]) == [3, 9, 12]