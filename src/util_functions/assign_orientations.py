from re import split
import pandas as pd

def assign_orientations(joined_ship_df:pd.DataFrame, character_df:pd.DataFrame):
    """
    assigns orientation data in ship df to 2 person ships

    returns a new character df with an added "orientation" column 
    and all characters only represented in gen or multi ships removed
    """
    
    orientation_info = joined_ship_df.copy().get([
        "slash_ship", "canon_orientation", "member_1", "member_2"
    ]).set_index("slash_ship")
    characters = {}
    for ship in list(orientation_info.index):
        current_row = orientation_info.loc[ship]

        orientation_cell = current_row["canon_orientation"]
        member_1 = split(" - ", current_row["member_1"])[1]
        member_2 = split(" - ", current_row["member_2"])[1]

        for member in [member_1, member_2]:
            if member not in characters.keys():
                characters[member] = set()

            # if it's "unspecified" for both
            if orientation_cell == "unspecified":
                characters[member].add("unspecified")

        if orientation_cell != "unspecified":
            split_orientations = split("/", orientation_cell)
            characters[member_1].add(split_orientations[0])
            characters[member_2].add(split_orientations[1])

    new_df = character_df.copy()

    new_df["orientation"] = new_df["full_name"].apply(
        lambda x: list(characters[x])[0] if x in characters.keys() else "gen_or_multi_only"
    )
    
    new_df = new_df.where(
        new_df["orientation"] != "gen_or_multi_only"
    ).dropna(how="all")

    return new_df

def cross_reference_with_gender(char_df:pd.DataFrame):
    """
    returns a new df with the following bool columns added:

    - canon_woman_attracted
    - canon_man_attracted
    - canon_other_attracted
    - canon_acearo
    - unspecified_orientation
    - canon_str8
    - canon_bi
    - canon_gay
    - canon_queer
    - canon_wlw
    - canon_mlm

    """
    pd.options.mode.copy_on_write = True # to make warning go away

    character_df = char_df.copy()

    for new_column in [
        "canon_woman_attracted",
        "canon_man_attracted",
        "canon_other_attracted",
        "canon_acearo",
        "unspecified_orientation",
        "canon_str8",
        "canon_bi",
        "canon_gay",
        "canon_queer",
        "canon_wlw",
        "canon_mlm",
    ]:
        character_df[new_column] = False

    for i in character_df.index:
        current_char_row = character_df.loc[i].copy()

        char_name = current_char_row["full_name"]
        char_fandom = current_char_row["fandom"]
        char_gender = current_char_row["gender"]
        char_orientation = current_char_row["orientation"]
        if char_orientation[-1] == "*":
            char_orientation = char_orientation[:-1]

        if char_gender in ["F", "F | Other"]:
            if char_orientation in ["gay", "bi"] \
            and not ("Eda" in char_name and "Owl" in char_fandom): 
            # as Eda only has men & transmasc nb love interests
                current_char_row["canon_woman_attracted"] = True
                current_char_row["canon_wlw"] = True

            if char_orientation in ["bi", "str8"]:
                current_char_row["canon_man_attracted"] = True
        
            if "Eda" in char_name and "Owl" in char_fandom:
                current_char_row["canon_other_attracted"] = True

        if char_gender in ["M", "M | Other", "M | F | Other"]: # incl our cis-male drag queens
            if char_orientation in ["gay", "bi"]:
                current_char_row["canon_man_attracted"] = True
                current_char_row["canon_mlm"] = True

            if char_orientation in ["bi", "str8"]:
                current_char_row["canon_woman_attracted"] = True
        
        # other cases
        if char_orientation == "unspecified":
            current_char_row["unspecified_orientation"] = True
        elif char_orientation == "acearo":
            current_char_row["canon_acearo"] = True
        elif char_orientation == "woman_attracted":
            current_char_row["canon_woman_attracted"] = True
        
        # queer, bi & str8 categories for ease of grouping later
        if char_orientation in ["gay", "bi", "acearo"]:
            current_char_row["canon_queer"] = True
        if char_orientation == "bi":
            current_char_row["canon_bi"] = True
        elif char_orientation == "str8":
            current_char_row["canon_str8"] = True

        # making sure there's not unexpected orientation tags we would've missed
        if char_orientation not in ["gay", "bi", "str8", "acearo", "woman_attracted", "unspecified", "fanon"]:
            print(char_name, char_fandom, char_orientation)

        character_df.loc[i] = current_char_row # need to reassign cause it doesn't edit in place

    return character_df