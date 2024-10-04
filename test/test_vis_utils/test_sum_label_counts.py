from visualisation.df_making_functions.retrieve_numbers import sum_label_nums
import pandas as pd
import pytest

@pytest.fixture
def test_df():
    """
    makes a df with dummy data
    """
    df = pd.DataFrame(
        columns=["rank", "labels", "no_of_works", "type"],
        data={
            "rank": [99,80,75,60,54,35,20,10.0],
            "labels": ["white", "white", "black", "e asian", "white", "s asian", "e asian", "white"],
            "no_of_works": [30, 25, 23, 20, 10, 5, 2, 3],
            "type": ["M/M", "F/F", "M/F", "M/M", "M/M", "M | Other/M", "M/M", "F/M"]
        }
    )

    return df


def test_returns_dataframe(test_df):
    result = sum_label_nums(test_df, "labels")
    assert type(result) == pd.DataFrame

def test_returns_new_df(test_df):
    result = sum_label_nums(test_df, "labels")
    assert result is not test_df

def test_does_not_mutate_input(test_df):
    copy_df = test_df.copy()
    sum_label_nums(test_df, "labels")
    assert copy_df.shape == test_df.shape
    assert list(copy_df.columns) == list(test_df.columns)
    assert list(copy_df["rank"]) == list(test_df["rank"])
    assert list(copy_df["labels"]) == list(test_df["labels"])

def test_raises_error_when_given_invalid_label_column(test_df):
    with pytest.raises(KeyError):
        assert sum_label_nums(test_df, "who?")

def test_raises_error_when_given_invalid_sum_column(test_df):
    with pytest.raises(KeyError):
        assert sum_label_nums(test_df, "labels", "who?")

def test_returns_all_columns_summed_by_default(test_df):
    result = sum_label_nums(test_df, "labels")
    assert "rank" in list(result.columns)
    assert "no_of_works" in list(result.columns)
    assert list(result["rank"]) == [75, 80, 35, 243]
    assert list(result["no_of_works"]) == [23, 22, 5, 68]

def test_returns_only_given_column_summed_and_renamed_as_sum_if_provided(test_df):
    result = sum_label_nums(test_df, "labels", "rank")
    assert "no_of_works" not in list(result.columns)
    assert "sum" in list(result.columns)
    assert list(result["sum"]) == [75, 80, 35, 243]

def test_removes_non_numerical_columns(test_df):
    result = sum_label_nums(test_df, "labels")
    assert "type" not in list(result.columns)
