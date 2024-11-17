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
    # sean will go here cause he irish
    'Boyang Jin': "China", # chinese
    'Yuzuru Hanyu': "Japan", # japanese
    'Jonathan Toews': "Canada", # canadian
    'Sean McLoughlin | Jacksepticeye': "Ireland", # irish
    "Alexis 'Alex' Maldonado | Quackity": "Mexico", # mexican
}

def make_youtuber_countries():
    """
    adds countries of origin to youtubers (because they are numerous enough to cause problems otherwise)

    prints full names and country of origin to data/reference_and_test_files/
    additional_data/additional_youtuber_data.csv
    """
    # read from char file
    char_df = make_characters_df()

    # get only youtubers
    youtuber_df = char_df.where(
        char_df["fandom"] == "Youtube"
    ).dropna(how="all")
    all_youtubers = list(youtuber_df["full_name"])

    country_dict = {}
    # add countries to them
    for youtuber in all_youtubers:
        if youtuber in real_human_americans:
            country_dict[youtuber] = "USA"
        elif youtuber in real_human_brits:
            country_dict[youtuber] = "UK"
        elif youtuber in other_real_humans:
            country_dict[youtuber] = other_real_humans[youtuber]
        else: print(youtuber)
    
    # prep for csv
    prepped_list = [["full_name", "country_of_origin", "continent"]]
    for youtuber in country_dict:
        country_of_origin = country_dict[youtuber]
        if country_of_origin in lbls.continents["America"]:
            continent = "America"
        if country_of_origin in lbls.continents["Europe"]:
            continent = "Europe"

        prepped_list.append([youtuber, country_of_origin, continent])

    # write to csv file
    csv_fandom_filepath = "data/reference_and_test_files/additional_data/additional_youtuber_data.csv"
    make_csv_file(prepped_list, csv_fandom_filepath)

def replace_youtuber_countries(input_df:pd.DataFrame, data_case:str):
    
    # retrieve make youtuber countries' output
    filepath = "data/reference_and_test_files/additional_data/additional_youtuber_data.csv"
    youtuber_countries = df_from_csv(filepath)
    
    new_df = input_df.copy()

    # replace youtuber countries w respective ones
    if data_case == "char_df":
        # individual if char df
        for youtuber in youtuber_countries["full_name"]:
            new_df["country_of_origin"] = new_df['country_of_origin'].mask(
                new_df["full_name"] == youtuber, 
                other=youtuber_countries.set_index("full_name").loc[youtuber, "country_of_origin"]
            )
            new_df["continent"] = new_df['continent'].mask(
                new_df["full_name"] == youtuber, 
                other=youtuber_countries.set_index("full_name").loc[youtuber, "continent"]
            )
        print(new_df.where(new_df["fandom"] == "Youtube").dropna(how="all").get(
            ["full_name","country_of_origin", "continent"]
        ))
    # elif data_case == "ships_df":
    #     # pairing combo if ships df
    #     pass

    return new_df

if __name__ == "__main__":
    make_youtuber_countries()