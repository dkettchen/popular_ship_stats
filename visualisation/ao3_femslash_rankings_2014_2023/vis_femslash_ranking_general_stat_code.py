from visualisation.vis_utils.invert_rank import invert_rank
from visualisation.vis_utils.make_name_string import make_name_string
from copy import deepcopy
import pandas as pd

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
        year_df = year_df.sort_values(by="rank_sum", ascending=False).head(15)#.dropna()
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
def hottest_sapphic_ranking(character_info_df):
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
def hottest_sapphic(character_info_df):
    """
    takes dataframe that (at least) contains "year", "full_name", "ship", "rank_no", 
    "fandom", "race", "rpf_or_fic" columns

    returns a dict with year keys and dict values

    each dict contains three keys: "ship_counts", "over_3_ships", and "ranking"

    ship_counts contains a dataframe with how many characters were in each number of ships that year 
    (ie x characters were in y ships)

    over_3_ships contains a dataframe with all characters that were in 3 or more ships that year 
    (including the info columns on highest ranked ship and demo as put out by hottest_sapphic_ranking)

    ranking contains a list of dicts with "no" and "names" keys, whose values represent the number 
    of ships (3+ only) and the names of all characters who tied for that number of ships that year
    """

    hottest_dict = hottest_sapphic_ranking(character_info_df)

    hottest_data = {}
    for year in hottest_dict:
        hottest_df = hottest_dict[year].copy()

        ship_count_df = hottest_df.copy().get(
            ["ship", "full_name"]
        ).groupby("ship").count().sort_index(ascending=False).reset_index().rename(
            columns={"full_name": "count", "ship": "no_of_ships"}
        ) # columns = ["no_of_ships", "count"]

        over_3_ships_df = hottest_df.where(hottest_df["ship"] > 2).dropna()

        year_ranking = []
        for num in [3,4,5]:
            rank_df = over_3_ships_df.copy().where(over_3_ships_df["ship"] == num).dropna()
            if len(rank_df) > 0:
                all_characters = sorted([character for character in rank_df["full_name"]])
                char_string = make_name_string(all_characters)
                year_ranking.append({"no": num, "names": char_string})
        
        hottest_data[year] = {
            "ship_counts": ship_count_df,
            "over_3_ships": over_3_ships_df,
            "ranking": year_ranking
        }

    return hottest_data



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

