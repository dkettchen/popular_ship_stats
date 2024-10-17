from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.make_file_dfs import make_ships_df
from visualisation.vis_utils.make_name_string import make_name_string
from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df
from visualisation.vis_utils.df_utils.hottest_char_utils import unify_doctors_and_PCs
import visualisation.vis_utils.diagram_utils.ranks as ranks
import pandas as pd

def make_full_chars_df():
    """
    combines ships & characters file data

    returns a dataframe where all the members of the ships have had their full name, gender and race 
    columns joined to their ships, and arranged so every member has their own row per ship
    (ie essentially going from:
        row 1: ship | member_1 | member_2 | member_3 | member_4
    to
        row 1: ship | member_1,
        row 2: ship | member_2,
        row 3: ship | member_3,
        row 4: ship | member_4
    )
    """
    ships_df = make_ships_df()

    # getting only columns we need (for now)
    ship_columns_df = ships_df.copy().get([
            'slash_ship', 'members_no', 'fandom', 'rpf_or_fic', 'gender_combo', 'race_combo', 
            'member_1', 'member_2', 'member_3', 'member_4'
    ])

    # adding count of ships per fandom before joining characters
    ships_per_fandom_df = ship_columns_df.copy().get(
        ['fandom', 'slash_ship',]
    )
    ships_per_fandom_df = get_label_counts(ships_per_fandom_df, "fandom", "slash_ship")

    ship_columns_df = ship_columns_df.join(
        other=ships_per_fandom_df, on="fandom", 
        rsuffix="_right", lsuffix="_left"
    )

    # join members info 
    full_character_df = join_character_info_to_df(ship_columns_df)

    # drop duplicate "fandom" column
    full_character_df.pop("char_fandom")

    # remove any none value rows from 3 & 4 if you haven't yet 
    full_character_df = full_character_df.rename(
        columns={"fandom_left": "fandom"}
    ).sort_values(by="fandom")

    return full_character_df

def make_hottest_char_df(full_character_df:pd.DataFrame):
    """
    takes output dataframe of make_full_chars_df

    returns a new df with the top hottest characters (characters who are in 3 or more ships) by fandom
    """
    # we need: 
    hottest_df = full_character_df.copy()
    
    # getting columns & rows with multiple ships
    hottest_df = hottest_df.where(
        cond=full_character_df["count"] > 1 # there needs to be multiple ships
    ).get([
        "fandom", 
        "full_name",
        "slash_ship", 
        "gender", 
        # "race"
    ]).dropna()

    hottest_df = unify_doctors_and_PCs(hottest_df) # unifying doctor whos & player characters
    hottest_df["fandom"] = clean_fandoms(hottest_df["fandom"]) # removing translations

    # group by fandom, by characters, count characters
    hottest_df = get_label_counts(hottest_df, [
        "fandom", 
        "full_name", 
        "gender", 
        # "race"
    ], "slash_ship")
    hottest_df = hottest_df.rename(columns={"count":"no_of_ships_they_in"}).reset_index()
    hottest_df = sort_df(hottest_df, ["fandom", "no_of_ships_they_in"])
    
    # # figuring out which fandoms' characters are all tied for ship numbers
    # tied_fandoms = find_tied_fandoms(hottest_df)
    # print(tied_fandoms) # -> should be only ['Carmilla', 'Amphibia']

    # removing all chars that are in less than 3 ships, and any fandoms where all chars are tied
    hottest_df = hottest_df.where(
        cond=(hottest_df["no_of_ships_they_in"] > 2) & (
        hottest_df["fandom"] != 'Carmilla') & (
        hottest_df["fandom"] != 'Amphibia')
    ).dropna()

    # ordering/grouping by fandom & number of ships

    unique_fandoms = sorted(get_unique_values_list(hottest_df, "fandom"))
    num_dict = {}
    rankings_columns = ["fandom", "rank", "names", "no"]
    rankings_list = [] 
    for fandom in unique_fandoms: # for each fandom (in alphabetical order)
        fandom_group = hottest_df.where( # making group of only this fandom's values
            cond=hottest_df["fandom"] == fandom
        ).sort_values(by="no_of_ships_they_in").dropna() # sorting by number of ships

        num_dict[fandom] = []
        for num in [8,7,6,5,4,3]: # range of ships they can be in

            # characters in that num of ships
            char_rank_list = list(
                fandom_group["full_name"].where(fandom_group["no_of_ships_they_in"] == num).dropna()
            )
            # if any
            if len(char_rank_list) > 0: 
                # concat into str
                names_list = sorted(char_rank_list) # sorting names alphabetically
                names_str = make_name_string(names_list)
                temp_dict = {
                    "no_of_ships":num, 
                    "names":names_str
                }
                num_dict[fandom].append(temp_dict)

        counter = 0
        for rank in num_dict[fandom]: # adding rank numbers
            temp_list = [
                fandom, 
                ranks.top_10_list[counter],
                rank["names"],
                rank["no_of_ships"]
            ]
            rankings_list.append(temp_list)

            counter += 1

    hottest_rank_df = pd.DataFrame(
        data=rankings_list, 
        columns=rankings_columns
    )#.sort_values(by=["fandom", "rank"]) # ordering by fandom & rank therein

    return hottest_rank_df


#notes:
# available formats:  .png .jpeg .webp .svg .pdf 
# gotta specify dimensions you want to make sure it prints it at the size you want

# look into kaleido smh 
    # -figure out work flow & test w this file ✅
    # (-make util for saving the image files)
    # -TODO:then put other notebook files into python files too & set up their work flows
    # -store old notebook files in vis folder once they've been successfully 
    #  transferred to python files

# currently kaleido can't do non-latin characters yet rip
    # https://github.com/plotly/Kaleido/issues/157 
    # possible workaround is to install language packages on the ubuntu
    # in this case language code would be ja for japanese
    # but there's others you can find at https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes 
# -> jupyter notebook version managed to do foreign characters tho!
    # -> how about we put the code in py files & then import into a notebook to actually export?
    # => try and see if the dimension specification works in notebook
# update: didn't solve the issue rip 
    # -jupyter renders the characters but doesn't change size w specified dimensions 
    # -image/bytes version changes size but still uses kaleido & doesn't render the characters
    # -installing japanese language pack & fonts also didn't fix it for the latter
    # -trying to export only the jupyter bit with the characters to try and manually 
    # photoshop em together also didn't work, it defaults to only exporting the top bit
    # -tried finding a way to make jupyter output bigger, but also not yet implemented 
    # for non-text outputs smh