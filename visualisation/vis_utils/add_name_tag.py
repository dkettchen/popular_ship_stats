import pandas as pd

def add_name_tag(input_df:pd.DataFrame):
    """
    input df must have "fandom" and "full_name" columns

    adds a "name_tag" column to df with "{fandom} - {full_name}" values
    """
    new_df = input_df.copy()

    new_df["name_tag"] = new_df["fandom"] + " - " \
        + new_df["full_name"]
    
    new_df = new_df.set_index(new_df["name_tag"])

    return new_df
