from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.make_file_dfs import make_ships_df
import pandas as pd
import plotly.graph_objects as go
from vis_utils.remove_translation import remove_translation
#import plotly.express as px
#from plotly.subplots import make_subplots

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
    ).groupby("fandom").count().rename(columns={"slash_ship":"no_of_ships"})
    ship_columns_df = ship_columns_df.join(
        other=ships_per_fandom_df, on="fandom", 
        rsuffix="_right", lsuffix="_left"
    )

    # join members info 
    full_character_df = join_character_info_to_df(ship_columns_df)

    # drop duplicate "fandom" column
    full_character_df.pop("fandom_right")

    # remove any none value rows from 3 & 4 if you haven't yet 
    full_character_df = full_character_df.rename(
        columns={"fandom_left": "fandom"}
    ).sort_values(by="fandom")

    return full_character_df

def make_hottest_char_df(full_character_df):
    """
    takes output dataframe of make_full_chars_df

    returns a new df with the top hottest characters (characters who are in 3 or more ships) by fandom
    """

    # we need: 
    hottest_df = full_character_df.copy().where(
        cond=full_character_df["no_of_ships"] > 1 # there needs to be multiple ships
    ).get(["fandom", "full_name", "slash_ship", "gender", "race"])

    # renaming & setting gender as ambig where relevant for the doctor & gender diff player 
    #   characters as they are the same character & we want to count them as one here
    # setting genders
    hottest_df["gender"] = hottest_df["gender"].mask(
        cond=(
            (hottest_df["full_name"].str.contains("Female", na=False)
            ) | (hottest_df["full_name"].str.contains("Male", na=False)
            ) | (hottest_df["full_name"].str.contains(" Doctor", na=False))
            ),
        other="Ambig"
    )
    # making renaming dict
    renaming_dict = {}
    for doctor in [
        "The Eleventh Doctor",
        "The Ninth Doctor",
        "The Tenth Doctor",
        "The Thirteenth Doctor",
        "The Twelfth Doctor",
    ]:
        renaming_dict[doctor] = "The Doctor"
    for pc in [
        "Hawke (Female) | Player Character",
        "Inquisitor (Female) | Player Character",
        "Warden (Female) | Player Character",
        "Shepard (Female) | Player Character",
        "Shepard (Male) | Player Character",
    ]:
        if "Hawke" in pc:
            renaming_dict[pc] = "Hawke | Player Character"
        elif "Inquisitor" in pc:
            renaming_dict[pc] = "Inquisitor | Player Character"
        elif "Warden" in pc:
            renaming_dict[pc] = "Warden | Player Character"
        elif "Shepard" in pc:
            renaming_dict[pc] = "Shepard | Player Character"
    # renaming
    hottest_df["full_name"] = hottest_df["full_name"].replace(to_replace=renaming_dict)

    # group by fandom, by characters, count characters
    hottest_df = hottest_df.groupby(["fandom", "full_name", "gender", "race"]).count().rename(
        columns={"slash_ship":"no_of_ships_they_in"}
    ).reset_index().sort_values(by=["fandom", "no_of_ships_they_in"], ascending=False)

    # # figuring out which fandoms' characters are all tied for ship numbers
    # unique_fandoms = hottest_df["fandom"].unique()
    # tied_fandoms = []
    # for fandom in unique_fandoms:
    #     fandom_group = hottest_df.where(
    #         cond=hottest_df["fandom"] == fandom
    #     ).sort_values(by="no_of_ships_they_in").dropna()
    #     if fandom_group["no_of_ships_they_in"].max() == fandom_group["no_of_ships_they_in"].min() and \
    #     fandom_group.shape[0] > 1 and fandom_group["no_of_ships_they_in"].max() > 1:
    #         tied_fandoms.append(fandom)
    # print(tied_fandoms) # -> only ['Carmilla', 'Amphibia']

    # removing all chars that are in less than 3 ships, and any fandoms where all chars are tied
    hottest_df = hottest_df.where(
        cond=(hottest_df["no_of_ships_they_in"] > 2) & (
        hottest_df["fandom"] != 'Carmilla') & (
        hottest_df["fandom"] != 'Amphibia')
    ).dropna()

    # ordering/grouping by fandom & number of ships
    unique_fandoms = hottest_df["fandom"].unique()
    hottest_chars_by_ship_no_dict = {}
    for fandom in unique_fandoms: # for each fandom
        if " | " in fandom:
            # couldn't figure out a way to render kana/kanji with kaleido, so getting rid of em
            hottest_chars_by_ship_no_dict[remove_translation(fandom)] = {}
        else: hottest_chars_by_ship_no_dict[fandom] = {}
        fandom_group = hottest_df.where( # making group of only this fandom's values
            cond=hottest_df["fandom"] == fandom
        ).sort_values(by="no_of_ships_they_in").dropna() # sorting by number of ships
        for num in [3,4,5,6,7,8]: # range of ships they can be in
            char_rank_list = list(fandom_group["full_name"].where( # characters in that num of ships
                fandom_group["no_of_ships_they_in"] == num
            ).dropna())
            if len(char_rank_list) > 0: # if there are characters with that num of ships
                if " | " in fandom:
                    hottest_chars_by_ship_no_dict[remove_translation(fandom)][num] = char_rank_list
                else: hottest_chars_by_ship_no_dict[fandom][num] = char_rank_list

    # making dataframe where every row is one number of ships (index)
    # and contains chars of that number by fandom (columns)
    hottest_chars_by_ship_no = pd.DataFrame(hottest_chars_by_ship_no_dict).sort_index(ascending=False)

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
            names_str = names_list[0] # getting first name

            if len(names_list) > 1: # if there are more names
                for name in names_list[1:]:
                    names_str += " & " + name # add every name
                names_str += " (tied)" # then tag them as tied

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

def visualise_hottest_characters(hottest_rank_df):
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
            columnwidth=[0.5,0.15,1,0.1] # setting column width ratios
        )
    ])

    return fig

# running file writing code
if __name__ == "__main__":

    full_character_df = make_full_chars_df()
    hottest_rank_df = make_hottest_char_df(full_character_df)
    hottest_rank_fig = visualise_hottest_characters(hottest_rank_df)

    hottest_rank_fig.write_image(
        "visualisation/all_ao3_data_vis_charts/all_ao3_hottest_characters_ranking_2013_2023.png", 
        width=800, 
        height=1400, 
        scale=2
    )
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