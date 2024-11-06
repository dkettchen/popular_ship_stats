from src.util_functions.retrieve_data_from_csv import read_data_from_csv
import pandas as pd

def df_from_csv(filepath:str):
    """
    reads from filepath (must be csv file) (using read_data_from_csv util function)

    returns a df with the data contained, using the first row as its column titles
    """
    csv_data = read_data_from_csv(filepath)
    df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
    return df