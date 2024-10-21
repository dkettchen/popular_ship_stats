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
def get_label_counts(df:pd.DataFrame, column_name:str | list, count_column:str=None, dropna:bool=False):
    """
    takes a dataframe, column name, and optionally a count column that must not contain null values

    if the latter is not provided it will use the first column that does not contain null values instead

    it can also take an argument to drop null values, which defaults to false

    returns a dataframe that contains the number of items for each unique label in that column in each
    column, including one column named "count" (either newly added by default or count_column renamed)
    """

    counted_df = df.copy()

    if not count_column or len(df[count_column]) != len(df[count_column].dropna()):
        if column_name == "index":
            count_column == None
        else: 
            count_column = find_full_column(df, column_name)

    if not count_column: # if there was no other full column
        counted_df["count"] = 1 # we make one
    else: # if there is a count_column now
        counted_df = counted_df.rename(
            columns={count_column: "count"} # we rename it to count
        )
    
    if column_name == "index":
        counted_df = counted_df.groupby(by=df.index, dropna=dropna).count()
    else:
        counted_df = counted_df.groupby(by=column_name, dropna=dropna).count()

    return counted_df

# sum x labels (ie combine a few labels)
def sum_label_nums(df:pd.DataFrame, label_column:str, sum_column:str=None):
    """
    takes a dataframe and column name by which to group the sums

    returns a new dataframe that contains the sum of the numbers in any numerical columns grouped by the 
    unique labels in the given column

    if a sum_column was provided it will return a df containing only this column, renamed as "sum"
    """

    if label_column == "index":
        summed_df = df.copy().groupby(df.index).agg("sum") # TODO: test
    else:
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

# get average per each label
def get_average_num(df:pd.DataFrame):
    """
    takes a dataframe with columns containing numbers to take the average of

    returns a new dataframe that contains one row, with the average of each column's numbers, 
    rounded to two decimal numbers
    """

    new_df = df.copy().mean(0).round(2)

    return new_df


# make list of unique values in column
def get_unique_values_list(input_item:pd.DataFrame|dict, column_name:str=None):
    """
    takes a dataframe and column name

    returns a list of all unique items in that column
    """

    if type(input_item) == pd.DataFrame:
        values_list = list(input_item[column_name].unique())
    elif type(input_item) == dict:
        values_list = []
        for year in input_item:
            year_srs = input_item[year].copy()
            values_list.extend(list(year_srs.index))
        values_list = sorted(set(values_list))

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
    
# make y/n columns
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

