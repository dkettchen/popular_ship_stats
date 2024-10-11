from visualisation.vis_utils.df_utils.hottest_char_utils import unify_doctors_and_PCs
import pandas as pd
import pytest

# mock df with "gender" & "full_name" columns
@pytest.fixture
def test_df():
    """
    makes a df with dummy data
    """
    df = pd.DataFrame(
        columns=["full_name", "gender"],
        data={
            "full_name": [
                "Stephen Strange | Doctor Strange", 
                "The Tenth Doctor", 
                "Warden (Female) | Player Character", 
                "Shepard (Male) | Player Character",
                "Amamiya Ren | Player Character",
                "Traveler | Player Character",
                "The Doctor",
                "Venom (Symbiote)",
                "Pearl"
            ],
            "gender": [
                "M",
                "M", 
                "F",
                "M",
                "M",
                "Ambig",
                "M",
                "Other",
                "F | Other"
            ]
        }
    )

    return df


def test_returns_dataframe(test_df):
    result = unify_doctors_and_PCs(test_df)
    assert type(result) == pd.DataFrame

def test_returns_new_dataframe(test_df):
    result = unify_doctors_and_PCs(test_df)
    assert result is not test_df

def test_does_not_mutate_input(test_df):
    copy_df = test_df.copy()
    unify_doctors_and_PCs(test_df)
    assert type(test_df) == type(copy_df)
    assert test_df.shape == copy_df.shape
    assert list(test_df.columns) == list(copy_df.columns)
    assert list(test_df["full_name"]) == list(copy_df["full_name"])
    assert list(test_df["gender"]) == list(copy_df["gender"])

def test_returns_dataframe_of_same_shape(test_df):
    result = unify_doctors_and_PCs(test_df)
    assert result.shape == test_df.shape


def test_leaves_other_doctors_names_unchanged(test_df):
    result = unify_doctors_and_PCs(test_df)
    assert "Stephen Strange | Doctor Strange" in list(result["full_name"])

def test_leaves_other_characters_names_unchanged(test_df):
    result = unify_doctors_and_PCs(test_df)
    assert "Venom (Symbiote)" in list(result["full_name"])
    assert "Pearl" in list(result["full_name"])
    assert "Amamiya Ren | Player Character" in list(result["full_name"])
    assert "Traveler | Player Character" in list(result["full_name"])

def test_leaves_other_player_chars_gender_unchanged(test_df):
    result = unify_doctors_and_PCs(test_df)
    result = result.set_index("full_name")
    assert result.loc["Amamiya Ren | Player Character", "gender"] == "M"
    assert result.loc["Traveler | Player Character", "gender"] == "Ambig"

def test_leaves_other_characters_gender_unchanged(test_df):
    result = unify_doctors_and_PCs(test_df)
    result = result.set_index("full_name")
    assert result.loc["Stephen Strange | Doctor Strange", "gender"] == "M"
    assert result.loc["Venom (Symbiote)", "gender"] == "Other"
    assert result.loc["Pearl", "gender"] == "F | Other"


def test_changes_player_chars_names_to_remove_gender(test_df):
    result = unify_doctors_and_PCs(test_df)
    assert "Warden (Female) | Player Character" not in list(result["full_name"])
    assert "Shepard (Male) | Player Character" not in list(result["full_name"])
    assert "Warden | Player Character" in list(result["full_name"])
    assert "Shepard | Player Character" in list(result["full_name"])

def test_removes_number_from_doctor_whos(test_df):
    result = unify_doctors_and_PCs(test_df)
    assert "The Doctor" in list(result["full_name"])
    assert "The Tenth Doctor" not in list(result["full_name"])

def test_changes_relevant_chars_gender_to_ambig(test_df):
    result = unify_doctors_and_PCs(test_df)
    changed_genders = result.where(
        (result["full_name"] == "The Doctor") | (
        result["full_name"] == "Warden | Player Character") | (
        result["full_name"] == "Shepard | Player Character")
    ).dropna()
    gender_list = list(changed_genders["gender"].unique())
    assert len(gender_list) == 1
    assert gender_list == ["Ambig"]
        
