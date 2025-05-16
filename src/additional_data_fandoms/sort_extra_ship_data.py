# must be attached to characters 
    # -> make a src func to sort that?
    # make src funcs to sort added data to chars & ships & make new files
    # should include specifying by gender
        # -> could cross reference gender labels & orientation labels
    # needs to specify (in ships) if orientation is aligned w pairing type

from visualisation.vis_utils.read_csv_to_df import df_from_csv
from visualisation.input_data_code.make_file_dfs import make_characters_df, make_ships_df

def parse_extra_ship_data():
    # read in file
    new_data_path = "data/reference_and_test_files/additional_data/additional_ship_data_filled_out.csv"
    new_data = df_from_csv(new_data_path).set_index("slash_ship")
    new_data.pop("fandom")

    character_df = make_characters_df()
    ship_df = make_ships_df()

    joined_ship_df = ship_df.join(other=new_data, on="slash_ship", lsuffix="_left", rsuffix="_right")

    # id, canon, incest, orientation
        # disregard ships with more than 2 characters pls -> join w char df already?

    # we'll only look at 2-member ships as there were no canon multi-ships 
    # and most of em are gen anyway (removes 8 ships)
    joined_ship_df = joined_ship_df.where(
        joined_ship_df["members_no"] == 2
    ).dropna(how="all")
    

    gen_only_ships = [
        "Aizawa Shouta | Eraserhead & Midoriya Izuku | Deku",
        "Alexander | Technoblade & Clay | Dream",
        "Alexander | Technoblade & Phil Watson | Philza",
        "Alexander | Technoblade & Phil Watson | Philza & Thomas Michael Simons | TommyInnit & William Patrick Spencer Gold | Wilbur Soot",
        "Alexander | Technoblade & Thomas Michael Simons | TommyInnit",
        "Alexander | Technoblade & William Patrick Spencer Gold | Wilbur Soot",
        "Clay | Dream & George Davidson | GeorgeNotFound & Nicholas Armstrong | Sapnap",
        "Clay | Dream & Nicholas Armstrong | Sapnap",
        "Clay | Dream & Thomas Michael Simons | TommyInnit",
        "Donatello & Leonardo",
        "Donatello & Leonardo & Michelangelo & Raphael",
        "Ellie & Joel",
        "Midoriya Izuku | Deku & Yagi Toshinori | All Might",
        "Phil Watson | Philza & Thomas Michael Simons | TommyInnit",
        "Phil Watson | Philza & William Patrick Spencer Gold | Wilbur Soot",
        "Ranboo & Thomas Michael Simons | TommyInnit",
        "Ranboo & Thomas Michael Simons | TommyInnit & Toby Smith | Tubbo",
        "Ranboo & Toby Smith | Tubbo",
        "Regulus Black & Sirius Black",
        "Robin Buckley & Steve Harrington",
        "Thomas Michael Simons | TommyInnit & Toby Smith | Tubbo",
        "Thomas Michael Simons | TommyInnit & William Patrick Spencer Gold | Wilbur Soot",
    ]

    # TODO assign orientations to characters


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