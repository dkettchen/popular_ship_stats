from re import split

def assign_orientations(joined_ship_df, character_df):
    """
    assigns orientation data in ship df to 2 person ships

    returns a new character df with an added "orientation" column
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
        lambda x: list(characters[x])[0] if x in characters.keys() else "gen_ship_only"
    )
    
    return new_df