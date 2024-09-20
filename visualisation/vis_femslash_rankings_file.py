from visualisation.vis_utils.make_file_dfs import make_femslash_dfs, make_characters_df, make_ships_df
from visualisation.vis_utils.remove_member_columns import remove_members_from_df
from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.invert_rank import invert_rank
from visualisation.vis_utils.remove_translation import remove_translation

from copy import deepcopy
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def edit_femslash_df_columns(femslash_df_dict):
    """
    takes output dict from make_femslash_dfs

    returns a new dict with new dataframes, where the "new_works", "release_date", 
    and "data_set" columns have been removed, a "year" column has been added, and in the 
    2014 set, the "change" column has been filled with "new" rather than None values
    """

    new_df_dict = {}

    for year in femslash_df_dict:
        new_df = femslash_df_dict[year].copy()

        # drop new works cause it's an overall ranking
        new_df.pop("new_works")

        # and release date cause we're not tracking that yet
        new_df.pop("release_date")

        # and replace data set name column with just year cause it's all femslash here for now
        new_df.pop("data_set")
        new_df["year"] = year

        if year == 2014:
            new_df["change"] = "new" # getting rid of none values

        new_df_dict[year] = new_df

    return new_df_dict
def join_ship_info_to_femslash(femslash_df_dict):
    """
    takes femslash df dict

    combines all femslash dfs into one big femslash ranking df and joins "fandom", 
    "rpf_or_fic", "gender_combo", "race_combo", and the 4 "member_" columns from ships file onto their 
    respective ranked ships
    """
    ships_df = make_ships_df().get([
        "slash_ship",
        "fandom",
        "rpf_or_fic",
        "gender_combo",
        "race_combo",
        "member_1",
        "member_2",
        "member_3",
        "member_4",
    ]).set_index("slash_ship")
    
    femslash_dfs_list = [femslash_df_dict[year] for year in femslash_df_dict]
    full_femslash_df = pd.concat(femslash_dfs_list)

    joined_df = full_femslash_df.join(other=ships_df, on="ship", lsuffix="_left", rsuffix="_right")

    return joined_df


## general stats

# marketshare of fandoms each year
def fandom_market_share_by_year(ship_info_df):
    """
    takes a dataframe that contains (at least) "year", "ship", and "fandom" columns

    returns a dictionary with year keys and dataframe values, of the counted 
    amount of ships per fandom in that year ("year" and "no_of_ships" columns)
    """
    new_df = ship_info_df.copy().get(["year", "ship", "fandom"])

    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).groupby("fandom").count().rename(
            columns={"ship": "no_of_ships"}
        )
        year_df = year_df.where(
            year_df["no_of_ships"] > 1
        ).sort_values(by="no_of_ships", ascending=False).dropna()
        year_df["year"] = year
        year_dict[int(year)] = year_df

    return year_dict
# fandoms with most popular ships (add together rankings!)
def fandoms_popularity_by_year(ship_info_df):
    """
    takes a dataframe that contains (at least) "year", "rank_no", and "fandom" columns

    returns a dictionary with year keys and dataframe values, of the sum of the inverted 
    rank number of all ships in each fandom in that year ("year" and "rank_sum" columns)
    (ex if a ship was 1st in the ranking, it was counted for 99, 
    if it was 90th, it was counted for 10)
    """
    new_df = ship_info_df.copy().get(["year", "rank_no", "fandom"])
    new_df["rank_no"] = new_df["rank_no"].apply(invert_rank)

    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).groupby("fandom").agg("sum").rename(
            columns={"rank_no": "rank_sum"}
        )
        year_df = year_df.head(15).sort_values(by="rank_sum", ascending=False)#.dropna()
        year_df["year"] = year
        year_dict[int(year)] = year_df

    return year_dict
# fandoms with most ships in ranking each year and most popular fandoms
def top_5_fandoms_by_year(market_share, popularity):
    """
    takes outputs from fandom_market_share_by_year and fandoms_popularity_by_year

    returns a dict of dataframes with the top 5 fandoms for each year by number of 
    ships and by popularity
    """
    # make a df with 1st, 2nd, 3rd place as index
    # and top by number of ships and top by popularity as columns
    index = ["1st", "2nd", "3rd", "4th", "5th"]
    columns = ["most_ships", "most_popular"]

    top_5_dict = {}
    for year in market_share:
        market_share_top = market_share[year].head().index
        popularity_top = popularity[year].head().index
        new_df = pd.DataFrame(
            data={columns[0]:market_share_top,columns[1]:popularity_top},
            index=index
        )
        new_df["year"] = year
        top_5_dict[year] = new_df

    return top_5_dict

# how much rpf vs not
def rpf_vs_fic(ship_info_df):
    """
    takes a dataframe that contains (at least) "year", "ship", and "rpf_or_fic" columns

    returns a dictionary with year keys and dataframe values, of the counted 
    amount of rpf or fictional ships in that year ("year" and "no_of_ships" columns)
    """
    new_df = ship_info_df.copy().get(["year", "ship", "rpf_or_fic"])

    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).groupby("rpf_or_fic").count().rename(
            columns={"ship": "no_of_ships"}
        )
        year_df["year"] = year
        year_dict[int(year)] = year_df

    return year_dict

# top 5 wlw ships & their demo each year
def top_5_wlw(ship_info_df):
    """
    takes a dataframe that contains (at least) "year", "ship", "fandom", "race_combo", and "rpf_or_fic" 
    columns and is sorted by ranks already

    returns a dictionary with year keys and dataframe values, of the top 5 ships in that year
    """
    new_df = ship_info_df.copy().get(["year", "ship", "fandom", "race_combo", "rpf_or_fic"])
    # leaving out gender combo cause all of em seem to be F / F

    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).dropna().head()
        year_dict[int(year)] = year_df
    
    return year_dict

def count_appearances(top_5):
    """
    takes output from top_5_wlw

    returns a dataframe with the count of number of appearances of each ship in the top 5
    """
    all_year_dfs = list(top_5.values())
    new_df = pd.concat(all_year_dfs)
    most_appearances = new_df.groupby(
        ["ship", "fandom", "race_combo", "rpf_or_fic"]
    ).count().sort_values(by="year", ascending=False)
    return most_appearances.reset_index().rename(columns={"year": "no_of_appearances"})
def count_streaks(top_5):
    """
    takes output from top_5_wlw

    returns a dataframe with the longest streak of each ship in the top 5
    """
    # set counters for each pairing (to zero)
    all_year_dfs = list(top_5.values())
    all_top_5 = pd.concat(all_year_dfs)
    counter_dict = {
        ship : 0 for ship in sorted(list(set(all_top_5["ship"])))
    }

    # set up streak storage
    streak_storage = deepcopy(counter_dict)
    for ship in streak_storage:
        streak_storage[ship] = []

    # go through years in order
    all_years = sorted(list(top_5.keys()))
    for year in all_years:

        for ship in counter_dict:
            if ship in list(top_5[year]["ship"]):
                counter_dict[ship] += 1 # increase streak
                streak_storage[ship].append(counter_dict[ship]) # add counter to storage
            else: # if ship isn't in top 5 that year
                counter_dict[ship] = 0 # reset counter to zero

    final_ranking = {}
    # get each pairing's longest streak number    
    for ship in streak_storage:
        longest_streak = sorted(streak_storage[ship], reverse=True)[0]
        final_ranking[ship] = longest_streak

    new_df = pd.DataFrame(
        data=final_ranking.values(), 
        index=final_ranking.keys(), 
        columns=["longest_streak"]
    ).sort_values(by="longest_streak", ascending=False)

    return new_df.reset_index().rename(columns={"index": "ship"})
# longest running top 5 femslash ship (longest streak & most appearances)
def longest_running_top_5_ships(appearances, streaks):
    """
    takes the output of count_appearances and count_streaks

    returns a dataframe with the top 5 ships for most appearances and longest streak, 
    including their respective numbers
    """

    top_5_for_appearances = appearances.head()
    top_5_for_streaks = streaks.head()

    ranks = ["1st", "2nd", "3rd", "4th", "5th"]
    rank_dict = {
        "top_ships_by_appearances": top_5_for_appearances["ship"].values,
        "no_of_appearances": top_5_for_appearances["no_of_appearances"].values,
        "top_ships_by_streak": top_5_for_streaks["ship"].values,
        "longest_streak": top_5_for_streaks["longest_streak"].values
    }
    new_df = pd.DataFrame(index=ranks, data=rank_dict)

    return new_df

# no 1 hottest character each year (in most ships)
    # & their highest-ranked ship
def hottest_sapphic(character_info_df):
    """
    takes dataframe that (at least) contains "year", "full_name", "ship", "rank_no", 
    "fandom", "race", "rpf_or_fic" columns

    returns a dict with year keys and dataframe values

    the dataframes contain the numbers of ships each character that year was in,
    ordered from most to least, and which their highest-ranked ship was
    """
    new_df = character_info_df.copy().get(
        ["year", "full_name", "ship", "rank_no", "fandom", "race", "rpf_or_fic"]
    )

    # group by years
    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).dropna()

        # group by characters
        # count
        hottest_df = year_df.groupby(
            ["year", "full_name", "fandom", "race", "rpf_or_fic"]
        ).count().sort_values(by="ship", ascending=False).reset_index()

        # finding highest ranked ship per character per year
        highest_ships_by_char = {}
        for character in list(year_df["full_name"].unique()):
            char_df = year_df.where(
                year_df["full_name"] == character
            ).sort_values(by="rank_no").head(1)

            highest_ships_by_char[character] = list(char_df["ship"])[0]
        
        hottest_df["highest_ship"] = [highest_ships_by_char[name] for name in hottest_df["full_name"]]
        hottest_df.pop("rank_no")

        year_dict[int(year)] = hottest_df
    
    return year_dict
# need to separate out chars we wanna visualise as a lot are tied & it's by year not fandom

# character gender percentages (what gender weirds were in the femslash ranking)
def sapphic_gender_stats(character_info_df):
    """
    takes dataframe that (at least) contains "year" and "gender" columns

    returns a dict with year keys and dataframe values

    the dataframes contain the numbers of characters of each gender tag represented that year
    """
    new_df = character_info_df.copy().get(["year", "gender"])

    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).dropna()
        counted_df = year_df.groupby("gender").count().rename(columns={"year": "count"})
        year_dict[int(year)] = counted_df.sort_values(by="count", ascending=False)

    return year_dict


## race stats:

# character race percentages each year
def total_racial_group_nos_by_year(character_info_df):
    """
    takes dataframe that (at least) contains "year" and "race" columns

    returns a dict with year keys and dataframe values

    the dataframes contain the numbers of characters of each race tag represented that year
    """
    new_df = character_info_df.copy().get(["year", "race"])

    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).dropna()
        counted_df = year_df.groupby("race").count().rename(columns={"year": "count"})
        year_dict[int(year)] = counted_df.sort_values(by="count", ascending=False)

    return year_dict
# how many multiracial characters each year
def total_multi_chars(race_percent):
    """
    takes output dict from total_racial_group_nos_by_year

    returns a dataframe with the total no of multiracial and non-multiracial characters per year
    """
    temp_dict = {}
    for year in race_percent:
        df = race_percent[year].reset_index()
        total = df["count"].sum()
        multi = df.where(
            df["race"].str.contains("(Multi)", regex=False) # regex false suppressed the warning!
        )["count"].sum()
        non_multi = total - multi
        temp_dict[year] = [multi, non_multi]
    new_df = pd.DataFrame(data=temp_dict, index=["multi_chars", "non-multi_chars"])
    return new_df
# how many racial groups each year
def total_racial_groups(race_percent):
    """
    takes output dict from total_racial_group_nos_by_year

    returns a series with the total no of racial groups represented each year
    """
    temp_dict = {}
    for year in race_percent:
        df = race_percent[year].reset_index()
        total = df["count"].count()
        temp_dict[year] = total
    new_df = pd.Series(data=temp_dict)
    return new_df

# ship race combo percentages each year
def total_racial_combo_nos_by_year(ship_info_df):
    """
    takes dataframe that (at least) contains "year" and "race_combo" columns

    returns a dict with year keys and dataframe values

    the dataframes contain the numbers of ships of each race combo represented that year
    """
    new_df = ship_info_df.copy().get(["year", "race_combo"])

    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).dropna()
        counted_df = year_df.groupby("race_combo").count().rename(columns={"year": "count"})
        year_dict[int(year)] = counted_df.sort_values(by="count", ascending=False)

    return year_dict
# of which how many interracial vs same
def total_interracial_ratio(race_combo_percent):
    """
    takes output dict from total_racial_combo_nos_by_year

    returns a dataframe with the total no of interracial and non-interracial ships per year
    """
    temp_dict = {}
    for year in race_combo_percent:
        df = race_combo_percent[year].reset_index()
        total = df["count"].sum()
        inter = df.where(
            df["race_combo"].str.contains("/")
        )["count"].sum()
        non_inter = total - inter
        temp_dict[year] = [inter, non_inter]
    new_df = pd.DataFrame(data=temp_dict, index=["interracial_ships", "non-interracial_ships"])
    return new_df
# of which how many involved multi chars vs non-multi
def total_multi_involved_ratio(race_combo_percent):
    """
    takes output dict from total_racial_combo_nos_by_year

    returns a dataframe with the total no of ships that involve multiracial chars vs not each year
    """
    temp_dict = {}
    for year in race_combo_percent:
        df = race_combo_percent[year].reset_index()
        total = df["count"].sum()
        multi = df.where(
            df["race_combo"].str.contains("(Multi)", regex=False) # regex false suppressed the warning!
        )["count"].sum()
        non_multi = total - multi
        temp_dict[year] = [multi, non_multi]
    new_df = pd.DataFrame(data=temp_dict, index=["with_multi_chars", "without_multi_chars"])
    return new_df

# prep info df with true/false values
def prep_df_for_non_white_ship_comp(ship_info_df):
    """
    takes dataframe that (at least) contains "year", "ship", "fandom", "rank_no", "race_combo" columns

    returns a dict with year keys and dataframe values

    the dataframes contain new columns with true or false/none values based on whether the ship involves
    white, east asian, ambiguous/non-human/unknown characters and whether they're white-involved,
    east asian-involved, non-white, or non-white & non-east asian ships based on that
    """
    new_df = ship_info_df.copy().get(["year", "ship", "fandom", "rank_no", "race_combo"])

    year_dict = {}
    for year in list(new_df["year"].unique()):
        year_df = new_df.where(
            new_df["year"] == year
        ).dropna()
        year_df["contains_white_person"] = year_df["race_combo"].str.contains("White|Eu")
            # I want to catch anna and elsa cause like they are white even if 
            # they're also european-indigenous (they can be both!), 
            # they're not a "non-white/non-ea" pairing, that's silly
        year_df["contains_e_asian_person"] = year_df["race_combo"].str.contains("E Asian")
        year_df["contains_ambig_person"] = year_df["race_combo"].str.contains("Ambig")
        year_df["contains_non_human"] = year_df["race_combo"].str.contains("N.H.")
        year_df["contains_unknown"] = year_df["race_combo"].str.contains("Unknown")

        year_df["true"] = True
        year_df["white_involved_ship"] = year_df["true"].where(
            year_df["contains_white_person"] == True
        )
        year_df["e_asian_involved_ship"] = year_df["true"].where(
            year_df["contains_e_asian_person"] == True
        )
        year_df["non_white_ship"] = year_df["true"].where(
            cond= (year_df["contains_white_person"] == False) & (
                year_df["contains_ambig_person"] == False) & (
                year_df["contains_non_human"] == False) & (
                year_df["contains_unknown"] == False)
        )
        year_df["non_white_or_ea_ship"] = year_df["true"].where(
            cond= (year_df["contains_white_person"] == False) & (
                year_df["contains_e_asian_person"] == False) & (
                year_df["contains_ambig_person"] == False) & (
                year_df["contains_non_human"] == False) & (
                year_df["contains_unknown"] == False)
        )
        year_df.pop("true")

        year_dict[int(year)] = year_df

    return year_dict
# how many ships involving {same racial combos as previously} made the wlw ranking each year
def count_non_white_ships(prepped_dict):
    """
    takes output from prep_df_for_non_white_ship_comp

    returns a df with numbers for how many ships each year involved white people, involved east 
    asian people, did not involve white people, and did not involve white or east asian people
    """
    concat_list = [prepped_dict[year] for year in prepped_dict]
    new_df = pd.concat(concat_list).get([
        "year", 
        "white_involved_ship", 
        "e_asian_involved_ship", 
        "non_white_ship", 
        "non_white_or_ea_ship"
    ])
    
    new_df = new_df.groupby("year").count()

    return new_df

# separate out the diff ship info
def separate_out_non_white_ships_info(prepped_dict): # (util)
    """
    takes output from prep_df_for_non_white_ship_comp

    returns a dict with year keys and dict values

    nested dicts contain "white_involved_ship", "e_asian_involved_ship", "non_white_ship", 
    and "non_white_or_ea_ship" keys with dataframe values with "year", "ship", "fandom", 
    "rank_no", "race_combo" & "ship_type"
    """
    year_dict = {}
    lookup_list = [
        "white_involved_ship",
        "e_asian_involved_ship",
        "non_white_ship",
        "non_white_or_ea_ship"
    ]

    for year in prepped_dict:
        year_dict[year] = {}
        year_df = prepped_dict[year]

        for item in lookup_list:
            temp_df = year_df.copy().get(
                ["year", "ship", "fandom", "rank_no", "race_combo", item]
            ).dropna().rename(columns={item: "ship_type"})
            temp_df["ship_type"] = item

            year_dict[year][item] = temp_df

    return year_dict
# top (1-5) ranked ship(s) of “” racial group combos as above each year
def top_non_white_ships(separated_dict):
    """
    takes output from separate_out_non_white_ships_info

    returns a dict with year keys and dataframe values

    the dataframes compile the top 3 (if 3) ships that year for each ship-type: 
    "white_involved_ship", "e_asian_involved_ship", "non_white_ship", "non_white_or_ea_ship"
    """
    new_dict = {}
    lookup_list = [
        "white_involved_ship",
        "e_asian_involved_ship",
        "non_white_ship",
        "non_white_or_ea_ship"
    ]
    for year in separated_dict:
        year_dict = separated_dict[year]
        concat_list = [year_dict[item].head(3) for item in lookup_list]
        new_df = pd.concat(concat_list)
        new_dict[year] = new_df
    
    return new_dict
# average rank of “” racial group combos as above each year vs average white-only & white-involved rank
def average_non_white_ranking(separated_dict):
    """
    takes output from separate_out_non_white_ships_info

    returns a dict with year keys and dataframe values

    the dataframes compile the average rank number that year for each ship-type: 
    "white_involved_ship", "e_asian_involved_ship", "non_white_ship", "non_white_or_ea_ship"
    """
    new_dict = {}
    lookup_list = [
        "white_involved_ship",
        "e_asian_involved_ship",
        "non_white_ship",
        "non_white_or_ea_ship"
    ]
    for year in separated_dict:
        year_dict = separated_dict[year]
        concat_list = [year_dict[item] for item in lookup_list]
        new_df = pd.concat(concat_list)
        new_df["rank_no"] = new_df["rank_no"].apply(invert_rank)
        new_df = new_df.get(
            ["ship_type", "rank_no"]
        ).groupby("ship_type").aggregate("mean").round(2)
        new_df["rank_no"] = new_df["rank_no"].apply(invert_rank)
        new_df["year"] = year
        new_dict[year] = new_df.sort_values(by="rank_no")
    
    return new_dict


## vis

def visualise_market_share_and_popularity(input_dict, colour_lookup):
    """
    visualise the femslash output from fandom_market_share_by_year 
    or fandoms_popularity_by_year as pie charts
    """
    year_donuts_fig = make_subplots(rows=2, cols=5, specs=[[
        {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}
    ], [
        {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}
    ]],)

    row_count = 1
    col_count = 2

    if "no_of_ships" in input_dict[2023].columns:
        femslash_title = "Fandoms (> 1 ship) by market share by year (AO3 femslash ranking 2013-2023)"
        column_name = "no_of_ships"
    elif "rank_sum" in input_dict[2023].columns:
        femslash_title = "Top 15 fandoms by popularity by year (AO3 femslash ranking 2013-2023)"
        column_name = "rank_sum"

    for year in input_dict:
        year_df = input_dict[year]
        fandoms = []
        for fandom in year_df.index:
            if " | " in fandom:
                new_fandom = remove_translation(fandom) 
                if "Madoka" in new_fandom:
                    new_fandom = "Madoka"
                elif new_fandom == "My Hero Academia":
                    new_fandom = "MHA"
            elif "Universe" in fandom and fandom != "Steven Universe":
                new_fandom = fandom[:-9]
                if "Avatar" in new_fandom:
                    new_fandom = "ATLA"
                elif "Game of Thrones" in new_fandom:
                    new_fandom = "GoT"
            elif "She-Ra" in fandom:
                new_fandom = "She-Ra"
            else: new_fandom = fandom
            fandoms.append(new_fandom)

        ships_no = year_df[column_name]

        colours = list(year_df.reset_index()["fandom"].apply(lambda x: colour_lookup[x]))

        year_donuts_fig.add_trace(go.Pie(
            labels=fandoms, 
            values=ships_no, 
            hole=0.3, # determines hole size
            title=year, # text that goes in the middle of the hole
            sort=False, # if you want to keep it in its original order rather than sorting by size
            titlefont_size=25, # to format title text
            marker_colors=colours,
            automargin=False,
            textposition="inside"
        ), row_count, col_count)

        if col_count == 5:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    year_donuts_fig.update_traces(
        textinfo='label',
        # marker=dict(
        #     #colors=px.colors.qualitative.Bold + px.colors.qualitative.Bold, # to use colours
        #     line=dict(color='#000000', width=2) # to add outline
        # )
    )
    year_donuts_fig.update_layout(
        title=femslash_title, 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        showlegend=False,
        # colorway=list(colour_lookup.values())
        # px.colors.qualitative.Bold + \
        #     px.colors.qualitative.Pastel + \
        #     px.colors.qualitative.Prism + \
        #     px.colors.qualitative.Vivid
    )

    return year_donuts_fig


def visualise_top_5_fandoms(input_dict):
    pass


def make_colour_lookup(input_df):
    """
    takes a df that contains (at least) a "fandom" column

    returns a dictionary with keys of all fandoms from input_df and colour values assigned to each
    """

    all_fandoms = sorted(list(input_df["fandom"].unique()))

    colour_lookup = {}
    colours = px.colors.qualitative.Bold + px.colors.qualitative.Bold + \
        px.colors.qualitative.Bold + px.colors.qualitative.Bold + \
        px.colors.qualitative.Bold + px.colors.qualitative.Bold + \
        px.colors.qualitative.Bold + px.colors.qualitative.Bold + \
        px.colors.qualitative.Bold + px.colors.qualitative.Bold
    
    colour_counter = 0
    for fandom in all_fandoms:
        colour_lookup[fandom] = colours[colour_counter]
        colour_counter += 1
    colour_lookup["Marvel"] = "crimson"
    colour_lookup["DC"] = "dodgerblue"
    colour_lookup["Harry Potter Universe"] = "green"
    colour_lookup["Homestuck"] = "orange"
    colour_lookup["Genshin Impact | 原神"] = "gold"
    colour_lookup["Steven Universe"] = "deeppink"
    colour_lookup["Once Upon a Time"] = "steelblue"
    colour_lookup["Avatar: The last Airbender Universe"] = "tomato"
    colour_lookup["Teen Wolf"] = "darkslateblue"
    colour_lookup["Buffy Universe"] = "goldenrod"
    colour_lookup["RWBY"] = "darkred"
    colour_lookup["Vampire Diaries Universe"] = "darkmagenta"
    colour_lookup["Stranger Things"] = "red"
    colour_lookup["Amphibia"] = "lightgreen"
    colour_lookup["Women's Soccer"] = "black"
    colour_lookup["Doctor Who"] = "blue"
    colour_lookup["Frozen"] = "paleturquoise"
    colour_lookup["Carmilla"] = "red"


    return colour_lookup


if __name__ == "__main__":

    # get data
    femslash_df_dict = make_femslash_dfs()

    # fix columns
    new_femslash_df_dict = edit_femslash_df_columns(femslash_df_dict)
    # combine into one big df
    ship_joined_femslash_df = join_ship_info_to_femslash(new_femslash_df_dict) 

    # make useable dfs
    femslash_ship_info_df = remove_members_from_df(ship_joined_femslash_df)
    femslash_character_info_df = join_character_info_to_df(ship_joined_femslash_df)

    # make fandom colour dict:
    colour_lookup_dict = make_colour_lookup(femslash_ship_info_df)

    # make items to be visualised:

    ## general stuff

    market_share_dict = fandom_market_share_by_year(femslash_ship_info_df) 
    market_share_fig = visualise_market_share_and_popularity(market_share_dict, colour_lookup_dict)
    market_share_fig.write_image(
        "visualisation/femslash_ao3_data_vis_charts/fandom_market_share_2013_2023.png", 
        width=2200, 
        height=1000, 
        scale=2
    )

    popularity_dict = fandoms_popularity_by_year(femslash_ship_info_df) 
    popularity_fig = visualise_market_share_and_popularity(popularity_dict, colour_lookup_dict)
    popularity_fig.write_image(
        "visualisation/femslash_ao3_data_vis_charts/fandom_popularity_2013_2023.png", 
        width=2200, 
        height=1000, 
        scale=2
    )

    top_5_fandoms_dict = top_5_fandoms_by_year(market_share_dict, popularity_dict) 
        # make into tables

    # rpf_or_fic_dict = rpf_vs_fic(femslash_ship_info_df) 
    #     # make into pie charts

    # top_5_ships_dict = top_5_wlw(femslash_ship_info_df)
    #     # either tables or race categories as a diagram
    # appearances_ranking = count_appearances(top_5_ships_dict)
    # streak_ranking = count_streaks(top_5_ships_dict)
    # longest_running_top_5 = longest_running_top_5_ships(appearances_ranking, streak_ranking) 
    #     # make into table

    # hottest_wlw = hottest_sapphic(femslash_character_info_df)
    #     # needs more futzing before vis
    #     # make into tables 
    #     # (rank (all chars of top number or top 2 nums), char name, top ship, per each year)

    # sapphic_genders = sapphic_gender_stats(femslash_character_info_df)

    ## race stats

    # femslash_race_percent = total_racial_group_nos_by_year(femslash_character_info_df)
    # femslash_race_combo_percent = total_racial_combo_nos_by_year(femslash_ship_info_df)

    # total_multi = total_multi_chars(femslash_race_percent)
    # total_groups = total_racial_groups(femslash_race_percent)

    # total_interracial = total_interracial_ratio(femslash_race_combo_percent)
    # total_multi_involved = total_multi_involved_ratio(femslash_race_combo_percent)

    # femslash_prepped_dict = prep_df_for_non_white_ship_comp(femslash_ship_info_df)
    # non_white_counts = count_non_white_ships(femslash_prepped_dict)

    # femslash_separated_dict = separate_out_non_white_ships_info(femslash_prepped_dict)
    # top_non_white = top_non_white_ships(femslash_separated_dict)
    # average_non_white_rank = average_non_white_ranking(femslash_separated_dict)
    #     # in 2020 we have non-white-ea ranking highest bc there's a singular ship and they 
    #     # happened to be 47th in the ranking which was higher than everyone else's averages lmao


