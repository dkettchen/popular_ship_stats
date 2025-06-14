from src.vis_code_refactor_utils.join_reference_data import join_ranking_and_ref
from src.vis_code_refactor_utils.drop_duplicate_characters import unique_chars

def make_joined_data(rankings:dict, reference_dict:dict):
    """
    takes dicts of all the read-in rankings and reference data

    runs joining code to join on additional fandoms, ship and character data to each yearly ranking

    returns a nested dict with a dict for every ranking of every year with the following keys/values:
    - "clean" - the original ranking df
    - "characters" - joined on character data (incl ranks & ships n stuff, 
    duplicate characters if in multiple ships)
    - "unique_characters" - character data (without ranks, ships, etc) for each 
    unique character that made the ranking that year
    - "ships" - joined on ship data
    """

    joined_data = {}
    for year in rankings:
        joined_data[year] = {}
        for ranking in rankings[year]:
            ranking_df = rankings[year][ranking]
            joined_char_df = join_ranking_and_ref(ranking_df, reference_dict, "characters")
            unique_char_df = unique_chars(joined_char_df)
            joined_ship_df = join_ranking_and_ref(ranking_df, reference_dict, "ships")
            all_dfs = {
                "clean": ranking_df,
                "characters": joined_char_df,
                "unique_characters": unique_char_df,
                "ships": joined_ship_df,
            }
            joined_data[year][ranking] = all_dfs
    return joined_data