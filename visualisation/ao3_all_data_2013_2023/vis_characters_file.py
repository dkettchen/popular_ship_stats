from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    get_average_num, 
    get_total_items
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df
import pandas as pd

def average_gender_per_fandom_df(characters_df:pd.DataFrame):
    """
    takes read-in characters file dataframe

    returns a series with the average number of male, female, and other characters in a fandom
    """
    # how many male vs female vs other characters a fandom has on average
    average_gender_per_fandom = characters_df.copy().get(
        ["full_name","fandom","gender"]
    )
    average_gender_per_fandom["women"] = average_gender_per_fandom.gender.where(
        cond=(characters_df.gender == "F") | (characters_df.gender == "F | Other")
    )
    average_gender_per_fandom["men"] =average_gender_per_fandom.gender.where(
        cond=(characters_df.gender == "M") | (characters_df.gender == "M | Other")
    )
    average_gender_per_fandom["characters of other or ambiguous gender"] = average_gender_per_fandom.gender.where(
        (characters_df.gender != "F") & (
        characters_df.gender != "F | Other") & (
        characters_df.gender != "M") & (
        characters_df.gender != "M | Other")
    )
    
    average_gender_per_fandom = get_label_counts(average_gender_per_fandom, "fandom")
    average_gender_per_fandom = average_gender_per_fandom.get(
        ["men","women","characters of other or ambiguous gender"]
    )
    average_gender_per_fandom = get_average_num(average_gender_per_fandom)

    return average_gender_per_fandom

def plural_vs_monoracial_fandoms_df(characters_df:pd.DataFrame, racial_div_by_fandom:pd.DataFrame):
    """
    takes read-in characters file dataframe and dataframe output 
    by get_data_df (data_case="racial_diversity")

    returns a dataframe with the number of fandoms that contain only one racial group 
    and the ones that contain more than one group
    """
    total_items = get_total_items(characters_df, "fandom")

    plural_vs_monoracial_fandoms = pd.DataFrame(
        columns=["total_fandoms"],
        data={"total_fandoms": total_items},
        index=[0]
        # counting all unique fandom names for total
    )

    plural_vs_monoracial_fandoms["fandoms_with_only_one_racial_group"] = racial_div_by_fandom.where( 
        # there is only one racial group in the fandom
        racial_div_by_fandom.groupby(racial_div_by_fandom.index.droplevel(1)).count() == 1 
    ).count().rename(
        index={"count": "fandoms_with_only_one_racial_group"}
    )["fandoms_with_only_one_racial_group"]

    plural_vs_monoracial_fandoms["fandoms_with_multiple_racial_groups"] = plural_vs_monoracial_fandoms[
        "total_fandoms"] - plural_vs_monoracial_fandoms["fandoms_with_only_one_racial_group"]
        # total minus monoracial fandoms

    plural_vs_monoracial_fandoms = plural_vs_monoracial_fandoms.rename(index={0: "count"})

    return plural_vs_monoracial_fandoms

def highest_racial_diversity_df(racial_div_by_fandom:pd.DataFrame):
    """
    takes output dataframe from get_data_df (data_case="racial_diversity")

    returns a dataframe with the top 6 fandoms that contain the most different racial groups
    """

    highest_racial_div = racial_div_by_fandom.where(
        racial_div_by_fandom.groupby(racial_div_by_fandom.index.droplevel(1)).count() > 1
    ).droplevel(1).dropna()

    highest_racial_div = get_label_counts(highest_racial_div, "index")
    highest_racial_div = sort_df(highest_racial_div, "count")
    
    return highest_racial_div.head(6) # everything else was under 5

def average_racial_diversity_df(racial_div_by_fandom:pd.DataFrame):
    """
    takes output dataframe from get_data_df (data_case="racial_diversity")

    returns a dataframe with the average number of racial groups per fandom
    """

    average_racial_div = racial_div_by_fandom.groupby(
        racial_div_by_fandom.index.droplevel(1)
    ).count()
    
    average_racial_div = get_average_num(average_racial_div)
    
    average_racial_div = average_racial_div.rename(
        index={"count":"average no of racial groups per fandom overall"}
    )

    return average_racial_div
