from re import sub
import pandas as pd

def remove_asterix(word):
    """
    takes a value, if it's a string and contains any asterixes, removes all asterixes from it

    otherwise returns as is
    """

    if type(word) == str and "*" in word:
        new_word = sub(r"\*", r"", word)
    else: new_word = word

    return new_word

def clean_columns(ship_df:pd.DataFrame):
    """
    removes asterixes from all columns in the input df
    """

    new_df = ship_df.copy()

    for column in new_df.columns:
        new_df[column] = new_df[column].apply(remove_asterix)

    return new_df
