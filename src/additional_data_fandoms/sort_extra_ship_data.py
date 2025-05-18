# must be attached to characters 
    # -> make a src func to sort that?
    # make src funcs to sort added data to chars & ships & make new files
    # should include specifying by gender
        # -> could cross reference gender labels & orientation labels
    # needs to specify (in ships) if orientation is aligned w pairing type

from visualisation.vis_utils.read_csv_to_df import df_from_csv
from visualisation.input_data_code.make_file_dfs import make_characters_df, make_ships_df
from src.util_functions.find_all_gen_only_ships import find_non_slash_ships
from src.util_functions.assign_orientations import assign_orientations, cross_reference_with_gender
from src.util_functions.conflicting_orientations import conflicting_orientations

def parse_extra_ship_data():
    """
    uses data from (additional ship data & ship files) to create a df

    - removes any ships that were only represented as a non-slash ship
    - removes any multi-ships as there were no canon multi ships 
    and this makes it easier to assign values to characters
    """

    # read in file
    new_data_path = "data/reference_and_test_files/additional_data/additional_ship_data_filled_out.csv"
    new_data = df_from_csv(new_data_path).set_index("slash_ship")
    new_data.pop("fandom")

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

    return joined_ship_df

def assign_to_characters(joined_ship_df):
    """
    processes and adds orientation data to the characters 
    (ex which characters are attracted to men and/or women, which characters are canon queer, etc)
    """
    character_df = make_characters_df()

    # assign orientations to characters 
    # (and remove characters not represented in relevant ships - currently removes 13 chars)
    oriented_chars = assign_orientations(joined_ship_df, character_df)

    # now cross reference with gender! 
    # -> adds more specific columns based on gender (ie woman/man attracted etc)
    specified_orientations_char_df = cross_reference_with_gender(oriented_chars)

    return specified_orientations_char_df

def assign_to_ships(joined_ship_df):
    """
    adds info on whether canon orientation conflicts or aligns with the ship type (or is ambiguous/unspecified)

    it also adds helpful columns on whether ships are mlm wlw het or other 
    (to include say M | Other characters in mlm)
    """
    
    # now to compare which ships are conflicting w canon orientations & which aren't
    conflicts_ship_df = conflicting_orientations(joined_ship_df)

    return conflicts_ship_df

# TODO print new files?

# canon should only be ["Yes", "No", "One-sided", "fanon"] (and the former 3 with *)
# print(new_data["canon"].unique())

# incest should only be ["Yes", "No", "step", "foster", "adoptive", "in-law"] (ditto)
# print(new_data["related"].unique())

if __name__ == "__main__":
    parsed_df = parse_extra_ship_data()
    assigned_char_df = assign_to_characters(parsed_df)
    assigned_ship_df = assign_to_ships(parsed_df)
