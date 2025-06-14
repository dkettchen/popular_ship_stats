import pandas as pd

def unique_chars(df:pd.DataFrame):
    """
    retrieve all unique characters in the given df

    only keeps character specific columns and drops any duplicates 
    (ie if same char was in multiple ships)

    returns new df
    """
    # only char specific data
    get_columns = [
        'Fandom', 'Name', 'Fandom_Name',
        'char_year_joined', 'char_latest_year', 'char_total_years', 
        'gender', 'race', 'orientation',
    ]
    # get relevant columns & drop duplicate rows!
    new_df = df.copy().get(get_columns).drop_duplicates()

    return new_df
