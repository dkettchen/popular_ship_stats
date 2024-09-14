from visualisation.vis_utils.read_csv_to_df import df_from_csv
import pandas as pd
import plotly.graph_objects as go
#import plotly.express as px
#from plotly.subplots import make_subplots

def make_full_chars_df(characters_df, ships_df):
    """
    takes input dataframes as read from our characters.csv & ships.csv (currently stage 5 versions)

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

    # getting only columns we need (for now)
    character_columns_df = characters_df.copy().get(['full_name','fandom', 'gender', 'race'])
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

    # add a column to char df with concat tag!
    character_columns_df["name_tag"] = character_columns_df["fandom"] + " - " \
        + character_columns_df["full_name"]
    character_columns_df = character_columns_df.set_index(character_columns_df["name_tag"])

    # make temp df for each member position
    member_1_df = ship_columns_df.join(
        other=character_columns_df, on="member_1", 
        rsuffix="_right", lsuffix="_left"
    )
    member_2_df = ship_columns_df.join(
        other=character_columns_df, on="member_2", 
        rsuffix="_right", lsuffix="_left"
    )
    member_3_df = ship_columns_df.join(
        other=character_columns_df, on="member_3", 
        rsuffix="_right", lsuffix="_left"
    )
    member_4_df = ship_columns_df.join(
        other=character_columns_df, on="member_4", 
        rsuffix="_right", lsuffix="_left"
    )

    # -> combine all rows into one big df 
    full_character_df = pd.concat([member_1_df, member_2_df, member_3_df, member_4_df])

    # drop "member" columns now that they're joined
    full_character_df.pop("member_1")
    full_character_df.pop("member_2")
    full_character_df.pop("member_3")
    full_character_df.pop("member_4")
    # drop duplicate "fandom" column
    full_character_df.pop("fandom_right")

    # remove any none value rows from 3 & 4 if you haven't yet 
    full_character_df = full_character_df.dropna().rename(
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


if __name__ == "__main__":
    # read from ships file make a df
    characters_df = df_from_csv("data/fifth_clean_up_data/stage_5_characters.csv")
    ships_df = df_from_csv("data/fifth_clean_up_data/stage_5_ships.csv")

    full_character_df = make_full_chars_df(characters_df, ships_df)
    hottest_rank_df = make_hottest_char_df(full_character_df)
    hottest_rank_fig = visualise_hottest_characters(hottest_rank_df)

    hottest_rank_fig.write_image(
        "visualisation/all_ao3_data_vis_charts/hottest_characters_ranking.png", 
        width=800, 
        height=1400, 
        scale=2
    )
    # available formats:  .png .jpeg .webp .svg .pdf 
    # gotta specify dimensions you want to make sure it prints it at the size you want

    # TODO: will need to look into kaleido smh 
        # -figure out work flow & test w this file ✅
        # (-make util for saving the image files)
        # -then put other notebook files into python files too & set up their work flows
        # -store old notebook files in vis folder once they've been successfully 
        #  transferred to python files
    # currently kaleido can't do non-latin characters yet rip
        # https://github.com/plotly/Kaleido/issues/157 
        # possible workaround is to install language packages on the ubuntu
        # in this case language code would be ja for japanese
        # but there's others you can find at https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes 