# must be attached to characters 
    # -> make a src func to sort that?
    # make src funcs to sort added data to chars & ships & make new files
    # should include specifying by gender
        # -> could cross reference gender labels & orientation labels
    # needs to specify (in ships) if orientation is aligned w pairing type

from visualisation.vis_utils.read_csv_to_df import df_from_csv
from visualisation.input_data_code.make_file_dfs import make_characters_df, make_ships_df
from src.util_functions.find_all_gen_only_ships import find_non_slash_ships
from src.util_functions.assign_orientations import assign_orientations

def parse_extra_ship_data():
    """
    uses data from (additional ship data, character & ship files)

    - removes any ships that were only represented as a non-slash ship
    - removes any multi-ships as there were no canon multi ships 
    and this makes it easier to assign values to characters
    """

    # read in file
    new_data_path = "data/reference_and_test_files/additional_data/additional_ship_data_filled_out.csv"
    new_data = df_from_csv(new_data_path).set_index("slash_ship")
    new_data.pop("fandom")

    character_df = make_characters_df()
    ship_df = make_ships_df()

    joined_ship_df = ship_df.join(other=new_data, on="slash_ship", lsuffix="_left", rsuffix="_right")

    # id, canon, incest, orientation
        # disregard ships with more than 2 characters pls -> join w char df already?

    # find non-slash ships (as we don't care abt those for this bit)
    # & remove em -> currently removes 22 gen-only ships
    gen_only_ships = find_non_slash_ships()
    joined_ship_df["gen_only"] = False
    for ship in gen_only_ships:
        joined_ship_df["gen_only"] = joined_ship_df["gen_only"].mask(
            joined_ship_df["gen_ship"] == ship, other=True
        )
    joined_ship_df = joined_ship_df.where(
        joined_ship_df["gen_only"] == False
    ).dropna(how="all")
    joined_ship_df.pop("gen_only") # can remove temp column again

    # we'll only look at 2-member ships as there were no canon multi-ships 
    # and most of em are gen anyway (removes 4 more ships)
    joined_ship_df = joined_ship_df.where(
        joined_ship_df["members_no"] == 2
    ).dropna(how="all")
    joined_ship_df.pop("members_no") # they're all 2 now

    # assign orientations to characters
    oriented_chars = assign_orientations(joined_ship_df, character_df)

    # canon should only be ["Yes", "No", "One-sided", "fanon"] (and the former 3 with *)
    # print(new_data["canon"].unique())

    # incest should only be ["Yes", "No", "step", "foster", "adoptive", "in-law"] (ditto)
    # print(new_data["related"].unique())

    # orientation should be the following combos and a few wild cards we can print
    # [
    #     "unspecified",
    #     "str8/unspecified",
    #     "unspecified/str8",
    #     "gay/unspecified",
    #     "unspecified/gay",
    #     "bi/unspecified",
    #     "unspecified/bi",
    #     "str8/str8",
    #     "gay/str8",
    #     "str8/gay",
    #     "bi/str8",
    #     "str8/bi",
    #     "gay/gay",
    #     "gay/bi",
    #     "bi/gay",
    #     "bi/bi",

    #     # some with acearo
    #     # unspecified doctor & canon nb that are woman_attracted
    #     # some of these ones but with * in there
    # ]
    # [
    #     'str8/str8',
    #     'str8/bi', 
    #     'str8/unspecified',
    #     'str8*/str8',
    #     'str8/str8*', 
    #     'str8/gay', 
    #     'str8*/gay', 
    #     'str8/gay*', 
    #     'str8/acearo', 
    #     'str8*/unspecified', 
    #     'str8/fanon', 
    #     'str8/bi*', 
    #     'str8/unspecified*'

    #     'bi/gay', 
    #     'bi/bi*', 
    #     'bi/bi', 
    #     'bi/str8', 
    #     'bi/woman_attracted',
    #     'bi/unspecified', 
    #     'bi/str8*',
    #     'bi*/str8', 

    #     'unspecified', 
    #     'unspecified/str8',
    #     'unspecified/gay',
    #     'unspecified*/str8', 
    #     'unspecified/bi', 
    #     'unspecified/acearo', 

    #     'gay/str8', 
    #     'gay/gay', 
    #     'gay/unspecified',  
    #     'gay/gay*', 
    #     'gay/str8*', 
    #     'gay/bi', 
    #     'gay/unspecified*', 
        
    # ]

    # make columns by crossreferencing for

    # "canon_man_attracted", 
    # "canon_woman_attracted", (all bis except for eda)
    # "canon_other_attracted", (only eda)
    # "canon_acearo", (only 2)
    # "unspecified_orientation",

    # then cross reference??
    # "canon_str8",
    # "canon_queer",
    # "canon_bi",

    # all should have a / in there or be "unspecified"
    # print(new_data["canon_orientation"].unique())

    pass

def assign_to_characters():
    pass

def assign_to_ships():
    pass

if __name__ == "__main__":
    parsed_df = parse_extra_ship_data()