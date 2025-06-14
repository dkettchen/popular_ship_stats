from src.vis_code_refactor_utils.read_ranking_files import read_rankings
from src.vis_code_refactor_utils.join_dfs import make_joined_data

def get_data_from_files(reference_dict:dict):
    """
    reads in, and joins reference data onto, rankings data

    returns a nested dict with various resulting data for each year/ranking

    prints updates as it goes

    you can change which data range you want in this function's file!
    """
    # which data we want
    START_YEAR = 2013
    END_YEAR = 2024
    WHICH_RANKING = "all"
    WEBSITE = "AO3"

    # retrieve ranking data
    print(f"Reading in {WHICH_RANKING} {WEBSITE} ranking data from {START_YEAR} to {END_YEAR}...")
    all_rankings = read_rankings(END_YEAR, START_YEAR, WHICH_RANKING, WEBSITE)
    print("Ranking files have been read.")

    # make a ship & char joined df for each year
    print("Joining ship and character data onto rankings...")
    joined_data = make_joined_data(all_rankings, reference_dict)
    print("Ship and character data has been added to rankings.")

    return joined_data
