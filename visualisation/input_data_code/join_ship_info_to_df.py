from visualisation.input_data_code.make_file_dfs import make_ships_df
import pandas as pd

def join_ship_info_to_df(input_df_dict:dict, ranking:str):
    """
    takes yearly df dict of (currently implemented:) "femslash" and "overall" ranking

    combines all input ranking dfs into one big ranking df and joins "fandom", 
    "rpf_or_fic", "gender_combo", "race_combo", and the 4 "member_" columns from ships file onto their 
    respective ranked ships
    """

    base_ships_df = make_ships_df()

    if ranking == "femslash":
        ships_df = base_ships_df.get([
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

    elif ranking == "overall":
        # making two dfs, one w only slash ship tags & one w only gen ship tags
        slash_df = base_ships_df.copy().rename(columns={"slash_ship":"ship"})
        slash_df.pop("gen_ship")
        gen_df = base_ships_df.copy().rename(columns={"gen_ship":"ship"})
        gen_df.pop("slash_ship")

        # making a df that has a gen & a slash version of each ship
        ships_df = pd.concat([slash_df, gen_df])
        print(slash_df.shape, gen_df.shape, ships_df.shape)

        ships_df = ships_df.get([
            "ship",
            "fandom",
            "rpf_or_fic",
            "gender_combo",
            "race_combo",
            "member_1",
            "member_2",
            "member_3",
            "member_4",
        ]).set_index("ship")
    
    input_df_list = [input_df_dict[year] for year in input_df_dict]
    full_df = pd.concat(input_df_list)

    joined_df = full_df.join(other=ships_df, on="ship", lsuffix="_left", rsuffix="_right")

    return joined_df