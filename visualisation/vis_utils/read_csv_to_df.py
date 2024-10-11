from src.util_functions.retrieve_data_from_csv import read_data_from_csv
import pandas as pd

def df_from_csv(filepath:str):
    csv_data = read_data_from_csv(filepath)
    df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
    return df