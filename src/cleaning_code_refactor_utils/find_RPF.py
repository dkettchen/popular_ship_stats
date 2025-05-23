import pandas as pd

def find_RPF(input_df:pd.DataFrame):
    """
    adds RPF bool column, returns new df
    """

    fandom_df = input_df.copy()

    fandom_df["RPF"] = True
    fandom_df["RPF"] = fandom_df["RPF"].where(
        (fandom_df["Fandom"].str.contains("RPF")) | (
        fandom_df["Fandom"].str.contains("Band\)")) | (
        fandom_df["Fandom"].str.contains("\(Musician\)")) | (
        fandom_df["Fandom"].str.contains("My Chemical Romance")) | (
        fandom_df["Fandom"].str.contains("Panic! at the Disco")) | (
        fandom_df["Fandom"].str.contains("TXT")) | (
        fandom_df["Fandom"].str.contains("Twenty One Pilots")) | (
        fandom_df["Fandom"].str.contains("BTS")) | (
        fandom_df["Fandom"].str.contains("Fall Out Boy")) | (
        fandom_df["Fandom"].str.contains("Minecraft")) | (
        fandom_df["Fandom"].str.contains("Hermit")) | (
        fandom_df["Fandom"].str.contains("Super-Vocal")),
        other=False
    )

    return fandom_df


