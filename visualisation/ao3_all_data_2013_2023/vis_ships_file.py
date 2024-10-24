from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.df_utils.retrieve_numbers import get_label_counts
from visualisation.input_data_code.get_data_df import get_data_df
import pandas as pd

def fandom_market_share_srs(ships_df:pd.DataFrame):
    """
    takes read-in dataframe from ships file

    returns a series with the fandoms that account for more than 1% of total ships
    """
    ships_per_fandom = get_data_df(ships_df, data_case="ships_per_fandom_util", ranking="total")
    total_ships = get_data_df(ships_df, data_case="total_ships", ranking="total")

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
    ships_per_fandom = get_data_df(ships_df, data_case="ships_per_fandom", ranking="total")
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

def interracial_srs(total_race_combo_counts:pd.DataFrame):
    """
    takes output dataframe from get_data_df (data_case="total_race_combos")

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
    takes output dataframe from get_data_df (data_case="total_race_combos")

    returns a series with the total number of ships that involve white ppl, involve east asian ppl, 
    do not involve white ppl, and involve neither white nor east asian people
    """
    # this one's the big oof
    non_white_ships = total_race_combo_counts.copy()
    non_white_ships["contains_white_person"] = non_white_ships.index.str.contains("White|Eu Ind")
    non_white_ships["contains_e_asian_person"] = non_white_ships.index.str.contains("^E Asian", regex=True)
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
