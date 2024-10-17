from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.sort_race_combos import sort_race_combos
from visualisation.vis_utils.df_utils.retrieve_numbers import (
    get_label_counts, 
    sum_label_nums
)
from visualisation.vis_utils.df_utils.make_dfs import sort_df
import pandas as pd

def total_ships_df(ships_df:pd.DataFrame): # util
    """
    takes read-in dataframe from ships file

    returns a dataframe with the total number of ships in the file
    """
    total_ships = ships_df.copy().get(["slash_ship"]).count().rename(
        index={"slash_ship":"total_num_of_ships"}
    )

    return total_ships

def total_gender_combo_percent_df(ships_df:pd.DataFrame):
    """
    takes read-in dataframe from ships file

    returns a dataframe with the total numbers of ships of each gender combo
    """
    total_gender_percentages = ships_df.copy().get(
        ["slash_ship","gender_combo"]
    )

    total_gender_percentages = get_label_counts(total_gender_percentages, "gender_combo", "slash_ship")
    total_gender_percentages = total_gender_percentages.rename(index={
        "F / M": "M / F",
        "Ambig / M": "M / Ambig",
        "Ambig / F": "F / Ambig",
        "M | Other / M": "M / M | Other"
    })

    total_gender_percentages = sum_label_nums(total_gender_percentages, "index")
    total_gender_percentages = sort_df(total_gender_percentages, "count", asc=True) # asc??

    return total_gender_percentages

def get_ships_per_fandom(ships_df:pd.DataFrame): # util
    """
    takes read-in dataframe from ships file

    returns a dataframe with only the fandom, slash_ship, gender_combo, and race_combo columns
    """
    ships_per_fandom = ships_df.copy().get(["fandom", "slash_ship", "gender_combo", "race_combo"])
    return ships_per_fandom

def make_ships_per_fandom_df(ships_df:pd.DataFrame): # util
    """
    takes read-in dataframe from ships file

    returns a dataframe with the number of ships per fandom
    """
    ships_per_fandom = get_ships_per_fandom(ships_df)
    ships_counts = get_label_counts(ships_per_fandom, "fandom", "slash_ship")

    ships_per_fandom = ships_per_fandom.join(
        other=ships_counts["count"], 
        on=ships_per_fandom.fandom, 
        how="inner", 
    ).rename(
        columns={"count": "total_ships"}
    )
    ships_per_fandom.pop("key_0")

    return ships_per_fandom

def fandom_market_share_srs(ships_df:pd.DataFrame):
    """
    takes read-in dataframe from ships file

    returns a series with the fandoms that account for more than 1% of total ships
    """
    ships_per_fandom = get_ships_per_fandom(ships_df)
    total_ships = total_ships_df(ships_df)

    fandom_market_share = get_label_counts(ships_per_fandom, "fandom", "slash_ship")
    
    fandom_market_share = fandom_market_share.where(
        (fandom_market_share["count"] / total_ships["total_num_of_ships"]) >= 0.01
    )["count"].sort_values(ascending=False)

    values = fandom_market_share.values
    fandoms = clean_fandoms(fandom_market_share.index)

    english_titles_market_share = pd.Series(data=values, index=fandoms)

    return english_titles_market_share

def ship_per_fandom_by_type_df(ships_df:pd.DataFrame):
    """
    takes read-in dataframe from ships file

    returns a dataframe with various stats on ships of different types by fandom
    (total number per fandom, % of fandom's ships, etc)
    """
    ships_per_fandom = make_ships_per_fandom_df(ships_df)
    ships_per_fandom_by_type = ships_per_fandom.copy().get(
        ["fandom", "total_ships", "gender_combo"]
    )

    # how many ships of type by fandom
    ships_per_fandom_by_type["wlw_ships"] = ships_per_fandom_by_type.gender_combo.where(
        (ships_per_fandom_by_type.gender_combo == "F / F"
        ) | (ships_per_fandom_by_type.gender_combo == "F | Other / F | Other"
        ) | (ships_per_fandom_by_type.gender_combo == "F / F | Other")
    )
    ships_per_fandom_by_type["mlm_ships"] = ships_per_fandom_by_type.gender_combo.where(
        (ships_per_fandom_by_type.gender_combo == "M / M"
        ) | (ships_per_fandom_by_type.gender_combo == "M | Other / M / M"
        ) | (ships_per_fandom_by_type.gender_combo == "M / M | Other"
        ) | (ships_per_fandom_by_type.gender_combo == "M | Other / M")
    )
    ships_per_fandom_by_type["het_ships"] = ships_per_fandom_by_type.gender_combo.where(
        (ships_per_fandom_by_type.gender_combo == "F / M"
        ) | (ships_per_fandom_by_type.gender_combo == "M / F")
    )
    ships_per_fandom_by_type.pop("gender_combo")
    ships_per_fandom_by_type = get_label_counts(ships_per_fandom_by_type, "fandom")
        # this makes fandom the index/columns -> no longer counted for length

    for ship_type in ["mlm", "wlw", "het"]:
        # percent of total that is
        ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] = (
            ships_per_fandom_by_type[f"{ship_type}_ships"] / ships_per_fandom_by_type["count"] * 100
        ).round(2)

        # diff conditions it fulfills
        ships_per_fandom_by_type[f"no_{ship_type}"] = ships_per_fandom_by_type["count"].where(
            ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] == 0
        )
        ships_per_fandom_by_type[f"all_{ship_type}"] = ships_per_fandom_by_type["count"].where(
            ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] == 100
        )
        ships_per_fandom_by_type[f"more_than_50%_{ship_type}"] = ships_per_fandom_by_type[f"%_of_{ship_type}_ships"].where(
            (ships_per_fandom_by_type[f"{ship_type}_ships"] > 1
            ) & (ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] < 100
            ) & (ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] >= 50)
        )

    return ships_per_fandom_by_type

def total_gender_combos_srs(ships_per_fandom_by_type:pd.DataFrame):
    """
    takes output dataframe from ship_per_fandom_by_type_df

    returns a series with how many fandoms contained no, only, or over 50% of each ship type
    """
    total_gender_combos_dict = {
        "no_mlm_ship_fandoms": ships_per_fandom_by_type["no_mlm"].count(),
        "more_than_50%_mlm": ships_per_fandom_by_type["more_than_50%_mlm"].count(),
        "only_mlm_ship_fandoms": ships_per_fandom_by_type["all_mlm"].count(),
        "no_wlw_ship_fandoms": ships_per_fandom_by_type["no_wlw"].count(),
        "more_than_50%_wlw": ships_per_fandom_by_type["more_than_50%_wlw"].count(),
        "only_wlw_ship_fandoms": ships_per_fandom_by_type["all_wlw"].count(),
        "no_het_ship_fandoms": ships_per_fandom_by_type["no_het"].count(),
        "more_than_50%_het": ships_per_fandom_by_type["more_than_50%_het"].count(),
        "only_het_ship_fandoms": ships_per_fandom_by_type["all_het"].count(),
    }
    total_gender_combos_series = pd.Series(total_gender_combos_dict)

    return total_gender_combos_series

def highest_of_this_type_df(ships_per_fandom_by_type:pd.DataFrame):
    """
    takes output dataframe from ship_per_fandom_by_type_df

    returns a dataframe with the top 3 fandoms for number of ships of each type
    """
    most_wlw = ships_per_fandom_by_type["wlw_ships"].where(
        ships_per_fandom_by_type["wlw_ships"] > 1
    ).sort_values(ascending=False).dropna()
    most_mlm = ships_per_fandom_by_type["mlm_ships"].where(
        ships_per_fandom_by_type["mlm_ships"] > 1
    ).sort_values(ascending=False).dropna()
    most_het = ships_per_fandom_by_type["het_ships"].where(
        ships_per_fandom_by_type["het_ships"] > 1
    ).sort_values(ascending=False).dropna()

    highest_of_type = {
        "highest num of mlm ships": [most_mlm.head(3).values[num] for num in [0,1,2]],
        "highest num of wlw ships": [most_wlw.head(3).values[num] for num in [0,1,2]],
        "highest num of het ships": [most_het.head(3).values[num] for num in [0,1,2]],
        "highest mlm fandom": [list(most_mlm.head(3).index)[num] for num in [0,1,2]],
        "highest wlw fandom": [list(most_wlw.head(3).index)[num] for num in [0,1,2]],
        "highest het fandom": [list(most_het.head(3).index)[num] for num in [0,1,2]],
    }
    highest_index = ["1st", "2nd", "3rd"]

    highest_of_type_df = pd.DataFrame(
        highest_of_type, 
        index=highest_index
    )

    return highest_of_type_df

def average_gender_combo_srs(ships_per_fandom_by_type:pd.DataFrame):
    """
    takes output dataframe from ship_per_fandom_by_type_df

    returns a series with the average number of ships of each gender combo in a fandom
    """
    average_gender_combo_dict = {
        "ships": ships_per_fandom_by_type["count"].mean().round(2),
        "mlm": ships_per_fandom_by_type["mlm_ships"].mean().round(2),
        "wlw": ships_per_fandom_by_type["wlw_ships"].mean().round(2),
        "hets": ships_per_fandom_by_type["het_ships"].mean().round(2)
    }
    average_gender_combo_per_fandom_series = pd.Series(average_gender_combo_dict)

    return average_gender_combo_per_fandom_series

def total_race_combo_df(ships_df:pd.DataFrame):
    """
    takes read-in dataframe from ships file

    returns a dataframe with the total numbers of ships of each race combo
    """
    total_race_combo_counts = ships_df.get(["slash_ship","race_combo"])

    unique_combos = sorted(list(set(total_race_combo_counts.race_combo)))
    rename_dict = sort_race_combos(unique_combos)

    total_race_combo_counts = get_label_counts(total_race_combo_counts, "race_combo", "slash_ship")
    total_race_combo_counts = total_race_combo_counts.rename(
        index=rename_dict,
    )
    total_race_combo_counts = sum_label_nums(total_race_combo_counts, "index")
    total_race_combo_counts = sort_df(total_race_combo_counts, "count")

    return total_race_combo_counts

def interracial_srs(total_race_combo_counts:pd.DataFrame):
    """
    takes output dataframe from total_race_combo_df

    returns a series with the total number of interracial, non-interracial and ambiguous ships
    """
    interracial_ships = total_race_combo_counts.copy()
    interracial_ships["is_interracial_pairing"] = interracial_ships.index.str.contains("/")
    interracial_ships["is_ambig"] = interracial_ships.index.str.contains("Ambig")
    interracial_ships_counts = pd.Series({
        "same_race_pairings": interracial_ships["count"].where(
            (interracial_ships.is_ambig == False) & (interracial_ships.is_interracial_pairing == False)
        ).aggregate("sum"),
        "interracial_pairings": interracial_ships["count"].where(
            (interracial_ships.is_ambig == False) & (interracial_ships.is_interracial_pairing == True)
        ).aggregate("sum"), 
        "ambiguous_pairings": interracial_ships["count"].where(
            interracial_ships.is_ambig == True
        ).aggregate("sum"), 
    })

    return interracial_ships_counts

def non_white_ships_srs(total_race_combo_counts:pd.DataFrame): 
    """
    takes output dataframe from total_race_combo_df

    returns a series with the total number of ships that involve white ppl, involve east asian ppl, 
    do not involve white ppl, and involve neither white nor east asian people
    """
    # this one's the big oof
    non_white_ships = total_race_combo_counts.copy()
    non_white_ships["contains_white_person"] = non_white_ships.index.str.contains("White|Eu Ind")
    non_white_ships["contains_e_asian_person"] = non_white_ships.index.str.contains("E Asian")
    non_white_ships["contains_ambig_person"] = non_white_ships.index.str.contains("Ambig")
    non_white_ships["contains_non_human"] = non_white_ships.index.str.contains("N.H.")
    non_white_ships["contains_unknown"] = non_white_ships.index.str.contains("Unknown")

    non_white_ships_counts = pd.Series(
        {
            "pairings_with_white_people": non_white_ships["count"].where(
                non_white_ships.contains_white_person == True
            ).aggregate("sum"), 
            "pairings_with_east_asian_people": non_white_ships["count"].where(
                non_white_ships.contains_e_asian_person == True
            ).aggregate("sum"), 
            "non_white_pairings": non_white_ships["count"].where(
                (non_white_ships.contains_ambig_person == False) & (
                non_white_ships.contains_non_human == False) & (
                non_white_ships.contains_unknown == False) & (
                non_white_ships.contains_white_person == False)
            ).aggregate("sum"),
            "non_white_or_east_asian_pairings": non_white_ships["count"].where(
                (non_white_ships.contains_ambig_person == False) & (
                non_white_ships.contains_non_human == False) & (
                non_white_ships.contains_unknown == False) & (
                non_white_ships.contains_white_person == False) & (
                non_white_ships.contains_e_asian_person == False)
            ).aggregate("sum"),
        }
    )

    return non_white_ships_counts

def rpf_fic_df(ships_df:pd.DataFrame):
    """
    takes read-in dataframe from ships file

    returns a dataframe with the number of rpf and non-rpf ships
    """
    rpf_vs_fic_df = ships_df.get(
        ["slash_ship", "rpf_or_fic"]
    )
    rpf_vs_fic_df = get_label_counts(rpf_vs_fic_df, "rpf_or_fic", "slash_ship")

    return rpf_vs_fic_df
