from visualisation.vis_utils.df_utils.retrieve_numbers import add_true_false_column, get_unique_values_list
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
    result = add_true_false_column(test_df, "rank", ">", 0)
    assert type(result) == pd.DataFrame

def test_returns_new_df(test_df):
    result = add_true_false_column(test_df, "rank", ">", 0)
    assert result is not test_df

def test_does_not_mutate_input(test_df):
    copy_df = test_df.copy()
    add_true_false_column(test_df, "rank", ">", 0)
    assert copy_df.shape == test_df.shape
    assert list(copy_df.columns) == list(test_df.columns)
    assert list(copy_df["rank"]) == list(test_df["rank"])
    assert list(copy_df["labels"]) == list(test_df["labels"])

def test_raises_error_when_given_invalid_column_name(test_df):
    with pytest.raises(KeyError):
        assert add_true_false_column(test_df, "who?", ">", 0)

def test_raises_error_when_given_invalid_operator(test_df):
    with pytest.raises(KeyError):
        assert add_true_false_column(test_df, "rank", "??", 0)


def test_returns_original_columns_unchanged(test_df):
    result = add_true_false_column(test_df, "rank", ">", 0)
    for column in test_df.columns:
        assert column in result.columns
    assert list(result["rank"]) == list(test_df["rank"])
    assert list(result["labels"]) == list(test_df["labels"])
    assert list(result["no_of_works"]) == list(test_df["no_of_works"])
    assert list(result["type"]) == list(test_df["type"])

def test_adds_a_single_new_column(test_df):
    result = add_true_false_column(test_df, "rank", ">", 0)
    assert len(result.columns) == len(test_df.columns) + 1

def test_new_column_is_named_new_column_by_default(test_df):
    result = add_true_false_column(test_df, "rank", ">", 0)
    assert "new_column" in result.columns

def test_new_column_is_named_given_name_if_provided(test_df):
    result = add_true_false_column(test_df, "rank", ">", 0, "positive_rank")
    assert "positive_rank" in result.columns
    assert len(result.columns) == len(test_df.columns) + 1
    for column in test_df.columns:
        assert column in result.columns


def test_returns_column_w_all_null_values_if_no_values_in_column_pass_cond(test_df):
    result = add_true_false_column(test_df, "rank", "<", 0)
    assert len(result["new_column"].dropna()) == 0

def test_returns_column_w_all_true_values_if_all_values_in_column_pass_cond(test_df):
    result = add_true_false_column(test_df, "rank", ">", 0)
    unique_values = get_unique_values_list(result, "new_column")
    assert unique_values == [True]

def test_returns_column_w_mix_of_true_and_null_values_if_only_some_values_pass_cond(test_df):
    result = add_true_false_column(test_df, "labels", "==", "white")
    assert len(result["new_column"].dropna()) < len(result["labels"].dropna())
    assert len(result["new_column"].dropna()) > 0

def test_returns_column_w_true_values_only_for_rows_that_pass_cond(test_df):
    result = add_true_false_column(test_df, "labels", "!=", "white")
    result = result.sort_values(by="labels") # white rows should be last
    assert list(result["new_column"].head(4)) == [True, True, True, True]
    assert len(result["new_column"].tail(4).dropna()) == 0
