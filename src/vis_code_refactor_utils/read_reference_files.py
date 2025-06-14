from data.reference_and_test_files.refactor_helper_files.folder_lookup import TOTAL_DATA_FOLDER
import pandas as pd

def read_reference_file(which):
    """
    reads requested reference data csv file

    which="fandoms"|"characters"|"ships"
    """
    filepath = f"{TOTAL_DATA_FOLDER}/{which[:-1]}_data.csv"
    df = pd.read_csv(filepath, index_col=0)
    return df
