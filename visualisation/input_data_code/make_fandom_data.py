from visualisation.vis_utils.invert_rank import invert_rank
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_unique_values_list,
    sum_label_nums
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df, get_year_df
import pandas as pd
import visualisation.vis_utils.diagram_utils.ranks as ranks

# marketshare of fandoms each year
def fandom_market_share_by_year(ship_info_df:pd.DataFrame):
    """
    takes a dataframe that contains (at least) "year", "ship", and "fandom" columns

    returns a dictionary with year keys and dataframe values, of the counted 
    amount of ships per fandom in that year ("year" and "no_of_ships" columns)
    """
    new_df = ship_info_df.copy().get(["year", "ship", "fandom"])

    year_dict = {}
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)
        year_df = get_label_counts(year_df, "fandom", "ship")
        year_df = year_df.rename(
            columns={"count": "no_of_ships"}
        )

        year_df = year_df.where(
            year_df["no_of_ships"] > 1
        )
        year_df = sort_df(year_df, "no_of_ships")
        year_df = year_df.dropna()

        year_df["year"] = year
        year_dict[int(year)] = year_df

    return year_dict

# fandoms with most popular ships (add together rankings!)
def fandoms_popularity_by_year(ship_info_df:pd.DataFrame):
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
    unique_year_list = get_unique_values_list(new_df, "year")
    for year in unique_year_list:
        year_df = get_year_df(new_df, year)
        year_df = sum_label_nums(year_df, "fandom", "rank_no")
        year_df = year_df.rename(
            columns={"sum": "rank_sum"}
        )
        year_df = sort_df(year_df, "rank_sum")
        year_df = year_df.head(15)

        year_df["year"] = year
        year_dict[int(year)] = year_df

    return year_dict

# fandoms with most ships in ranking each year and most popular fandoms
def top_5_fandoms_by_year(market_share:dict, popularity:dict):
    """
    takes outputs from fandom_market_share_by_year and fandoms_popularity_by_year

    returns a dict of dataframes with the top 5 fandoms for each year by number of 
    ships and by popularity
    """
    # make a df with 1st, 2nd, 3rd place as index
    # and top by number of ships and top by popularity as columns
    index = ranks.top_10_list[:5]
    columns = ["most_ships", "most_popular"]

    top_5_dict = {}
    for year in market_share:
        market_share_top = market_share[year].head().index
        popularity_top = popularity[year].head().index

        new_df = pd.DataFrame(
            data={columns[0]: market_share_top, columns[1]: popularity_top},
            index=index
        )
        new_df["year"] = year
        top_5_dict[year] = new_df

    return top_5_dict

