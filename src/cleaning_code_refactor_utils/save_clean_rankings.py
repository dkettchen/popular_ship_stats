from data.reference_and_test_files.refactor_helper_files.folder_lookup import  CLEAN_FOLDER
import os

def make_clean_rankings_csvs(final_rankings:dict):
    """
    prints finished clean AO3 rankings to csv files

    creates sub folders for each year if they don't exist yet
    """

    for year in final_rankings:
        FOLDER_PATH = f"{CLEAN_FOLDER}/AO3_{year}"
        # make sub folder if it doesn't exist yet
        if not os.path.exists(FOLDER_PATH):
            os.mkdir(FOLDER_PATH)
        # make a file for each ranking
        for ranking in final_rankings[year]:
            filepath = f"{FOLDER_PATH}/AO3_{year}_{ranking}.csv"
            df = final_rankings[year][ranking]
            df.to_csv(filepath, index=False)

