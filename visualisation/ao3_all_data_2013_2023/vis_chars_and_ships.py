from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.make_file_dfs import make_ships_df
from visualisation.vis_utils.make_name_string import make_name_string
from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df
from visualisation.vis_utils.df_utils.hottest_char_utils import unify_doctors_and_PCs, find_tied_fandoms
import pandas as pd
import plotly.graph_objects as go

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

# possibly also refactor this mess
def make_hottest_char_df(full_character_df:pd.DataFrame):
    """
    takes output dataframe of make_full_chars_df

    returns a new df with the top hottest characters (characters who are in 3 or more ships) by fandom
    """

    # we need: 
    hottest_df = full_character_df.copy().where(
        cond=full_character_df["count"] > 1 # there needs to be multiple ships
    ).get(["fandom", "full_name", "slash_ship", "gender", "race"]).dropna()

    hottest_df = unify_doctors_and_PCs(hottest_df) # unifying doctor whos & player characters

    hottest_df["fandom"] = clean_fandoms(hottest_df["fandom"]) # removing translations

    # group by fandom, by characters, count characters
    hottest_df = get_label_counts(hottest_df, ["fandom", "full_name", "gender", "race"], "slash_ship")
    hottest_df = hottest_df.rename(
        columns={"count":"no_of_ships_they_in"}
    ).reset_index()
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
    unique_fandoms = get_unique_values_list(hottest_df, "fandom")
    hottest_chars_by_ship_no_dict = {}
    for fandom in unique_fandoms: # for each fandom
        hottest_chars_by_ship_no_dict[fandom] = {}

        fandom_group = hottest_df.where( # making group of only this fandom's values
            cond=hottest_df["fandom"] == fandom
        ).sort_values(by="no_of_ships_they_in").dropna() # sorting by number of ships

        for num in [3,4,5,6,7,8]: # range of ships they can be in
            char_rank_list = list(fandom_group["full_name"].where( # characters in that num of ships
                fandom_group["no_of_ships_they_in"] == num
            ).dropna())

            if len(char_rank_list) > 0: # if there are characters with that num of ships
                hottest_chars_by_ship_no_dict[fandom][num] = char_rank_list

    # making dataframe where every row is one number of ships (index)
    # and contains chars of that number by fandom (columns)
    hottest_chars_by_ship_no = pd.DataFrame(hottest_chars_by_ship_no_dict)
    hottest_chars_by_ship_no = sort_df(hottest_chars_by_ship_no)

    # making a new dict for ranking order
    hottest_chars_dict = {}
    rank_lookup_dict = {
        1: "1st",
        2: "2nd",
        3: "3rd",
        4: "4th",
    }
    for fandom in hottest_chars_by_ship_no.columns:
        all_chars = hottest_chars_by_ship_no[fandom].dropna() # getting all characters in fandom
        hottest_chars_dict[fandom] = {}
        count = 1
        for index in all_chars.index:
            names_list = sorted(all_chars.loc[index]) # sorting names alphabetically
            no_of_ships = index # retrieving number of ships
            names_str = make_name_string(names_list)

            rank_no = rank_lookup_dict[count] # getting rank string
            hottest_chars_dict[fandom][rank_no] = {
                "no_of_ships": no_of_ships,
                "names": names_str,
            }
            count += 1

    # prepping columns & values for dataframe
    rankings_columns = ["fandom", "rank", "names", "no"]
    rankings_list = [] 
    for fandom in hottest_chars_dict:
        for rank in hottest_chars_dict[fandom]:
            temp_list = [
                fandom, 
                rank,
                hottest_chars_dict[fandom][rank]["names"],
                hottest_chars_dict[fandom][rank]["no_of_ships"]
            ]
            rankings_list.append(temp_list)

    hottest_rank_df = pd.DataFrame(
        data=rankings_list, 
        columns=rankings_columns
    ).sort_values(by=["fandom", "rank"]) # ordering by fandom & rank therein

    return hottest_rank_df

def visualise_hottest_characters(hottest_rank_df:pd.DataFrame):
    """
    takes output dataframe of make_hottest_char_df

    returns a plotly table figure of it
    """

    line_colour = 'slategrey'
    header_fill_colour = 'skyblue'
    body_fill_colour = 'aliceblue'

    fig = go.Figure(data=[
        go.Table(
            header=dict(
                values=list(hottest_rank_df.columns),
                align='left',
                line_color=line_colour,
                fill_color=header_fill_colour,
            ),
            cells=dict(
                values=[
                    hottest_rank_df["fandom"], 
                    hottest_rank_df["rank"], 
                    hottest_rank_df["names"], 
                    hottest_rank_df["no"],
                ],
                align='left',
                line_color=line_colour,
                fill_color=body_fill_colour,
            ),
            columnwidth=[0.3,0.1,1.4,0.07] # setting column width ratios
        )
    ])

    return fig


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