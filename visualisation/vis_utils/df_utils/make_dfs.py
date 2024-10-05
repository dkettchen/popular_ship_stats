import pandas as pd

# get year df (where year == year)
def get_year_df(df:pd.DataFrame, year:int|float):
    """
    takes a dataframe (must (at least) contain a "year" column), and a year number

    returns a new dataframe that only contains the rows with the given year in their "year" column
    """
    
    year_df = df.copy().where(
        df["year"] == year
    ).dropna()

    return year_df

# sort df ascending
def sort_df(df:pd.DataFrame, column_name:str=None, asc:bool=False):
    """
    takes a dataframe, and optional arguments column_name (str) and asc (bool)

    if a column name string is given, the dataframe will be sorted by that column's values, 
    otherwise it'll be sorted by index

    if asc is True, it will be sorted in ascending order, otherwise it'll be sorted in descending order
    """

    if type(column_name) == str:
        new_df = df.sort_values(by=column_name, ascending=asc)
    else:
        new_df = df.sort_index(ascending=asc)

    return new_df

# make items into df or series (for consistency)