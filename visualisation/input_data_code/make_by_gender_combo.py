import pandas as pd
from visualisation.input_data_code.make_top_ships import top_ships, most_popular_ships

def make_by_gender_combo(ship_info_df:pd.DataFrame, data_case:str, ranking:str):
    """
    takes ship info df and ranking string

    returns a dictionary 
    
    - if data_case="most_popular" the dict has "mlm", "wlw", "hets" keys with dataframes of the 
    all-time most popular ships of that type in that ranking
    - if data_case="top_ships" the dict has year keys with dictionary values with "mlm", "wlw", 
    "hets" keys with dataframes of the top 10 ships of that year
    """

    type_dict = {}
    for label in ["mlm", "wlw", "hets"]:
        top_ships_dict = top_ships(ship_info_df, ranking, label) 
        # outputs dict with each year's top 10

        if data_case == "most_popular": # returns a concated df for each type
            concat_list = [top_ships_dict[year] for year in top_ships_dict]
            top_ships_df = pd.concat(concat_list)

            most_popular = most_popular_ships(top_ships_df, ranking)

            type_dict[label] = most_popular # df values
    
        elif data_case == "top_ships": # returns a dict with type keys for each year
            for year in top_ships_dict:
                if year not in type_dict.keys():
                    type_dict[year] = {}
                type_dict[year][label] = top_ships_dict[year] # dict values
    
    return type_dict


    
    