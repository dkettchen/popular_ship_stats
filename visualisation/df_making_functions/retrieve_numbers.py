import pandas as pd

# total items(rows) in df (ie characters or ships)
def get_total_items(df:pd.DataFrame, column_name:str):
    """
    takes a dataframe and column name

    returns the number of unique items in that column
    """

    column_list = get_unique_values_list(df, column_name)
    number_of_items = len(column_list)

    return number_of_items

# count x labels (ie gender, race, combos, rpf, etc)
def get_label_counts(df:pd.DataFrame, column_name:str, count_column:str=None):
    """
    takes a dataframe, column name, and optionally a count column that must not contain null values

    if the latter is not provided it will use the first column that does not contain null values instead

    returns a series that contains the number of items for each unique label in that column
    """

    counted_df = df.copy().groupby(column_name).count()

    if not count_column:
        count_column = find_full_column(df, column_name)

    counted_df = counted_df.rename(
        columns={count_column: "count"}
    )

    return counted_df[count_column]

# sum x labels (ie combine a few labels)
def sum_label_nums(df:pd.DataFrame, label_column:str, sum_column:str=None):
    """
    takes a dataframe and column name by which to group the sums

    returns a new dataframe that contains the sum of the numbers in any numerical columns grouped by the 
    unique labels in the given column

    if a sum_column was provided it will return a df containing only this column, renamed as "sum"
    """

    summed_df = df.copy().groupby(label_column).agg("sum")

    if sum_column: 
        summed_df = summed_df.rename(
            columns={sum_column: "sum"}
        ).get([sum_column])

    return summed_df



# make list of unique values in column
def get_unique_values_list(df:pd.DataFrame, column_name:str):
    """
    takes a dataframe and column name

    returns a list of all unique items in that column
    """

    values_list = list(df[column_name].unique)

    return values_list

# finding a column without null values
def find_full_column(df:pd.DataFrame, column_name:str):
    """
    takes a dataframe and column name

    returns a different column name that does not contain null values
    """

    temp_df = df.copy()
    temp_df.pop(column_name)
    columns = list(temp_df.columns)

    for column in columns:
        if len(temp_df[column].dropna()) == len(temp_df[column]): # if there are no null values
            return column
    
