import pandas as pd
from visualisation.input_data_code.make_top_ships import top_ships, most_popular_ships

def make_by_gender_combo(ship_info_df:pd.DataFrame, data_case:str, ranking:str):
    """
    takes ship info df and ranking string

    returns a dictionary with "mlm", "wlw", "hets" keys with values containing only data relating to 
    ships of that type

    - if data_case="most_popular" the values are dataframes of the all-time most popular ships 
    in that ranking
    - if data_case="top_ships" the values are dictionaries with year keys with dataframes of the 
    top 10 of that year
    """

    type_dict = {}
    for label in ["mlm", "wlw", "hets"]:
        top_ships_dict = top_ships(ship_info_df, ranking, label)
        if data_case == "most_popular":
            concat_list = [top_ships_dict[year] for year in top_ships_dict]
            top_ships_df = pd.concat(concat_list)

            most_popular = most_popular_ships(top_ships_df, ranking)

            type_dict[label] = most_popular # df values
        elif data_case == "top_ships":
            type_dict[label] = top_ships_dict # dict values

    return type_dict


    
    