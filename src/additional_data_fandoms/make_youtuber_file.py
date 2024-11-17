from visualisation.input_data_code.make_file_dfs import make_characters_df
from src.util_functions.write_csv_file import make_csv_file

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
    prepped_list = [["full_name", "country_of_origin"]]
    for youtuber in country_dict:
        prepped_list.append([youtuber, country_dict[youtuber]])

    # write to csv file
    csv_fandom_filepath = "data/reference_and_test_files/additional_data/additional_youtuber_data.csv"
    make_csv_file(prepped_list, csv_fandom_filepath)

#def replace_youtuber_countries(input_df:pd.DataFrame, data_case:str):
    # retrieve make youtuber countries' output
    # replace youtuber countries w respective ones
        # individual if char df
        # pairing combo if ships df

if __name__ == "__main__":
    make_youtuber_countries()