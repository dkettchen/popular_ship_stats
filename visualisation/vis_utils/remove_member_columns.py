import pandas as pd

def remove_members_from_df(input_df):
    """
    takes a df with "member_1" through "member_4" columns (+ any other columns)

    returns a new df with the member columns removed
    """
    new_df = input_df.copy()
    new_df.pop("member_1")
    new_df.pop("member_2")
    new_df.pop("member_3")
    new_df.pop("member_4")
    return new_df