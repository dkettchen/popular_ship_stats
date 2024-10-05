import pandas as pd

# total items(rows) in df (ie characters or ships) - tested
def get_total_items(df:pd.DataFrame, column_name:str):
    """
    takes a dataframe and column name

    returns the number of unique items in that column
    """

    column_list = get_unique_values_list(df, column_name)
    number_of_items = len(column_list)

    return number_of_items

# count x labels (ie gender, race, combos, rpf, etc) - tested
def get_label_counts(df:pd.DataFrame, column_name:str, count_column:str=None):
    """
    takes a dataframe, column name, and optionally a count column that must not contain null values

    if the latter is not provided it will use the first column that does not contain null values instead

    returns a series that contains the number of items for each unique label in that column
    """

    counted_df = df.copy()

    if not count_column or len(df[count_column]) != len(df[count_column].dropna()):
        count_column = find_full_column(df, column_name)

    if not count_column: # if there was no other full column
        counted_df["count"] = 1 # we make one
    else: # if there is a count_column now
        counted_df = counted_df.rename(
            columns={count_column: "count"} # we rename it to count
        )

    counted_df = counted_df.groupby(column_name).count()

    return counted_df["count"]

# sum x labels (ie combine a few labels) - tested
def sum_label_nums(df:pd.DataFrame, label_column:str, sum_column:str=None):
    """
    takes a dataframe and column name by which to group the sums

    returns a new dataframe that contains the sum of the numbers in any numerical columns grouped by the 
    unique labels in the given column

    if a sum_column was provided it will return a df containing only this column, renamed as "sum"
    """

    summed_df = df.copy().groupby(label_column).agg("sum")

    if sum_column: 
        if sum_column not in summed_df.columns:
            raise KeyError
        
        summed_df = summed_df.rename(
            columns={sum_column: "sum"}
        ).get(["sum"])
    
    for column in summed_df.columns:
        if summed_df[column].dtype != "int64" and summed_df[column].dtype != "float64":
            # removing non-numerical columns
            summed_df.pop(column)

    return summed_df

#TODO get average per each label
def get_average_num(df:pd.DataFrame, column_name:str, labels_list:str=None):
    
    pass



# make list of unique values in column - tested
def get_unique_values_list(df:pd.DataFrame, column_name:str):
    """
    takes a dataframe and column name

    returns a list of all unique items in that column
    """

    values_list = list(df[column_name].unique())

    return values_list

# finding a column without null values - tested
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
    
# make y/n columns TODO: test
def add_true_false_column(
        df:pd.DataFrame, 
        column_name:str, operator:str, value_label, 
        new_column_name:str="new_column"
    ):
    """
    takes a dataframe, the column to check, one of the following operators: 
    ["==", "!=", "<", "<=", ">", ">="], 
    and a value or label to check the values in the column against, 
    as well as an optional name for the new column

    returns a new dataframe that's a copy of the given one with an added new column of retained values 
    where the condition was true, and null values where it was false
    """

    new_df = df.copy()

    #conditions are formatted as <column> <operator> <value/label>
    if operator == "==":
        new_df[new_column_name] = new_df[column_name].where(new_df[column_name] == value_label)
    elif operator == "!=":
        new_df[new_column_name] = new_df[column_name].where(new_df[column_name] != value_label)
    elif operator == "<":
        new_df[new_column_name] = new_df[column_name].where(new_df[column_name] < value_label)
    elif operator == "<=":
        new_df[new_column_name] = new_df[column_name].where(new_df[column_name] <= value_label)
    elif operator == ">":
        new_df[new_column_name] = new_df[column_name].where(new_df[column_name] > value_label)
    elif operator == ">=":
        new_df[new_column_name] = new_df[column_name].where(new_df[column_name] >= value_label)
    else: raise KeyError

    with pd.option_context('future.no_silent_downcasting', True): 
        # why is there warnings I need to work around ToT
        new_df[new_column_name] = new_df[new_column_name].mask(
            cond=pd.notna(new_df[new_column_name]), other=True
        )

    # we want the output to be the same df, but with added column w true/false values based on condition
    return new_df

#TODO combine y/n column info (WIP)
def combine_true_false_column_info(
        df:pd.DataFrame, operator:str, 
        true_columns:list=[], false_columns:list=[]
    ):

    is_or = False
    is_and = False
    if operator.lower() == "or" or operator == "|":
        is_or = True
    elif operator.lower() == "and" or operator == "&":
        is_and = True

    # if I can't figure out a way to make it work for more than 2 items, lists may only be 0-2 items long