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
        "canon_queer",
        "canon_wlw",
        "canon_mlm",
    ]:
        character_df[new_column] = False

    character_df["canon_woman_attracted"] = character_df["canon_woman_attracted"].mask(
        (
            ((character_df["gender"] == "F") | (
                character_df["gender"] == "F | Other")) & (
            (character_df["orientation"] == "gay") | (
                character_df["orientation"] == "bi")) & (
            (character_df["full_name"] != "Eda Clawthorne")) 
            # Eda doesn't have female love interests
        ) | (
            ((character_df["gender"] == "M") | (
                character_df["gender"] == "M | Other") | (
                character_df["gender"] == "M | F | Other")) & (
            (character_df["orientation"] == "str8") | (
                character_df["orientation"] == "bi"))
        ) | (
            character_df["orientation"] == "woman_attracted"
        ), 
        other=True
    )
    character_df["canon_man_attracted"] = character_df["canon_man_attracted"].mask(
        (
            ((character_df["gender"] == "M") | (
                character_df["gender"] == "M | Other") | (
                character_df["gender"] == "M | F | Other")) & (
            (character_df["orientation"] == "gay") | (
                character_df["orientation"] == "bi"))
        ) | (
            ((character_df["gender"] == "F") | (
                character_df["gender"] == "F | Other")) & (
            (character_df["orientation"] == "str8") | (
                character_df["orientation"] == "bi"))
        ) | (
            character_df["orientation"] == "man_attracted"
        ),
        other=True
    )
    character_df["canon_other_attracted"] = character_df["canon_other_attracted"].mask(
        # canon nb attracted
        (character_df["full_name"] == "Eda Clawthorne"),
        other=True
    )
    character_df["unspecified_orientation"] = character_df["unspecified_orientation"].mask(
        (character_df["orientation"] == "unspecified"),
        other=True
    )
    character_df["canon_acearo"] = character_df["canon_acearo"].mask(
        (character_df["orientation"] == "acearo"),
        other=True
    )

    character_df["canon_mlm"] = character_df["canon_mlm"].mask(
        ((character_df["gender"] == "M") | (
            character_df["gender"] == "M | Other") | (
            character_df["gender"] == "M | F | Other")) & (
        character_df["canon_man_attracted"] == True),
        other=True
    )
    character_df["canon_wlw"] = character_df["canon_wlw"].mask(
        ((character_df["gender"] == "F") | (
            character_df["gender"] == "F | Other")) & (
        character_df["canon_woman_attracted"] == True),
        other=True
    )
    character_df["canon_queer"] = character_df["canon_queer"].mask(
        (character_df["canon_wlw"] == True) | (
            character_df["canon_mlm"] == True) | (
            character_df["canon_other_attracted"] == True) | (
            character_df["canon_acearo"] == True) | (
            character_df["gender"] == "Other")
    )

    return character_df