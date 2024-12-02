from visualisation.input_data_code.make_file_dfs import make_characters_df
from src.util_functions.write_csv_file import make_csv_file
import pandas as pd
from visualisation.vis_utils.read_csv_to_df import df_from_csv
import visualisation.vis_utils.diagram_utils.labels as lbls # to get continents

real_human_americans = [
    'Patrick Kane', # american
    'Alexander | Technoblade',
    'Clay | Dream', # american
    'Darryl Noveschosch | BadBoyHalo', # american
    'Karl Jacobs', # american
    'Kristin Watson, née Rosales', # american
    'Mark Fischbach | Markiplier', # american
    'Michael Jones', # american
    'Nicholas Armstrong | Sapnap', # american
    'Ranboo', # american
    'Ryan | GoodTimesWithScar', # american
    'Zak Ahmed | Skeppy', # american
]
real_human_brits = [
    'Charles | Grian', # UK
    'Dan Howell | danisnotonfire', # UK
    'Gavin Free', # UK
    'George Davidson | GeorgeNotFound', # UK
    'Phil Lester | AmazingPhil', # UK
    'Phil Watson | Philza', # UK
    'Thomas Michael Simons | TommyInnit', # UK
    'Toby Smith | Tubbo', # UK
    'William Patrick Spencer Gold | Wilbur Soot', # UK
]
other_real_humans = {
    'Boyang Jin': "China", # chinese
    'Yuzuru Hanyu': "Japan", # japanese
    'Jonathan Toews': "Canada", # canadian
    'Sean McLoughlin | Jacksepticeye': "Ireland", # irish
    "Alexis 'Alex' Maldonado | Quackity": "Mexico", # mexican
}

def make_rpf_countries():
    """
    adds countries of origin to real humans from multi-national fandoms 
    (because they cause problems otherwise)

    prints full names and country of origin to data/reference_and_test_files/
    additional_data/additional_rpf_data.csv
    """
    # read from char file
    char_df = make_characters_df()

    # get only relevant humans
    human_df = char_df.where(
        (char_df["fandom"] == "Youtube") | (
        char_df["fandom"] == "Figure Skating") | (
        char_df["fandom"] == "Hockey")
    ).dropna(how="all")
    all_humans = list(human_df["full_name"])

    country_dict = {}
    # add countries to them
    for human in all_humans:
        if human in real_human_americans:
            country_dict[human] = "USA"
        elif human in real_human_brits:
            country_dict[human] = "UK"
        elif human in other_real_humans:
            country_dict[human] = other_real_humans[human]
        else: print(human)
    
    # prep for csv
    prepped_list = [["full_name", "country_of_origin", "continent"]]
    for human in country_dict:
        country_of_origin = country_dict[human]
        if country_of_origin in lbls.continents["North America"]:
            continent = "North America"
        if country_of_origin in lbls.continents["Europe"]:
            continent = "Europe"
        if country_of_origin in lbls.continents["Asia"]:
            continent = "Asia"

        prepped_list.append([human, country_of_origin, continent])

    # write to csv file
    csv_fandom_filepath = "data/reference_and_test_files/additional_data/additional_rpf_data.csv"
    make_csv_file(prepped_list, csv_fandom_filepath)

def replace_rpf_countries(input_df:pd.DataFrame, data_case:str):
    
    # retrieve make human countries' output
    filepath = "data/reference_and_test_files/additional_data/additional_rpf_data.csv"
    humans_countries = df_from_csv(filepath)
    
    new_df = input_df.copy()

    # replace human countries w respective ones
    if data_case == "char_df":
        # individual if char df
        for human in humans_countries["full_name"]:
            new_df["country_of_origin"] = new_df['country_of_origin'].mask(
                new_df["full_name"] == human, 
                other=humans_countries.set_index("full_name").loc[human, "country_of_origin"]
            )
            new_df["continent"] = new_df['continent'].mask(
                new_df["full_name"] == human, 
                other=humans_countries.set_index("full_name").loc[human, "continent"]
            )
        
    elif data_case == "ships_df":
        # pairing combo if ships df
        if "slash_ship" in new_df.columns:
            ship_name = "slash_ship"
        else: ship_name = "ship"
        
        # find relevant ships
        all_humans_ships = sorted(list(set(
            new_df.where(
                (new_df["fandom"] == "Youtube") | (
                new_df["fandom"] == "Figure Skating") | (
                new_df["fandom"] == "Hockey")
            ).dropna(how="all")[ship_name]
        )))

        # who is in those ships
        for ship in all_humans_ships:
            ship_countries = set()
            ship_continents = set()

            # add their countries & continents to a set resp
            for human in humans_countries["full_name"]:
                if human in ship:
                    ship_countries.add(
                        humans_countries.set_index("full_name").loc[human, "country_of_origin"]
                    )
                    ship_continents.add(
                        humans_countries.set_index("full_name").loc[human, "continent"]
                    )

            # sort & concat them
            ship_countries = sorted(list(ship_countries))
            ship_country_str = ship_countries[0] # adding first one
            # if there are multiple:
            for item in ship_countries[1:]:
                ship_country_str += f" / {item}"

            ship_continents = sorted(list(ship_continents))    
            ship_continent_str = ship_continents[0]
            for item in ship_continents[1:]:
                ship_continent_str += f" / {item}"

            # replace w those
            new_df["country_of_origin"] = new_df['country_of_origin'].mask(
                new_df[ship_name] == ship, 
                other=ship_country_str
            )
            new_df["continent"] = new_df['continent'].mask(
                new_df[ship_name] == ship, 
                other=ship_continent_str
            )

    return new_df

if __name__ == "__main__":
    make_rpf_countries()