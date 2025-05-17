from re import split

def conflicting_orientations(ship_df):
    """
    returns new df with added columns:
    - clean_orientation (removes * and puts spaces around the /)

    - mlm_ship (ships between any M, M | Other, and M | F | Other characters)
    - wlw_ship (ships between any F and F | Other characters)
    - het_ship (ships between any F and M characters)
    - other_ship (any other ship types (ie that contain Ambig, Other))

    - canon_aligned (canon orientations of characters allow for ship type (ex str8/str8 in het ship))
    - canon_conflicted (canon orientations of characters do not allow for ship type 
    (ex str8 person in same-sex ship))
    - canon_ambiguous (any unspecified (unless already conflicted) or varying (ex gay/str8 NPC paired with an 
    Ambig player character -> would be aligned for one and conflicted for the other 
    gendered version) canon orientations)
    """

    new_df = ship_df.copy()

    # clean up orientation column
    new_df["clean_orientation"] = None
    for i in new_df.index:
        current_orientation = new_df.loc[i, "canon_orientation"]
        
        if current_orientation == "unspecified":
            new_df.loc[i, "clean_orientation"] = "unspecified / unspecified"
        else:
            # split
            split_orient = split("/", current_orientation)
            first_item = split_orient[0]
            second_item = split_orient[1]
            # remove *
            if first_item[-1] == "*":
                first_item = first_item[:-1]
            if second_item[-1] == "*":
                second_item = second_item[:-1]
            # reassemble
            new_orient = first_item + " / " + second_item
            # assign
            new_df.loc[i, "clean_orientation"] = new_orient
    
    # short cuts to mlm wlw & het ships
    new_df["mlm_ship"] = False
    new_df["mlm_ship"] = new_df["mlm_ship"].mask(
        (new_df["gender_combo"] == "M / M") | (
        new_df["gender_combo"] == "M | Other / M") | (
        new_df["gender_combo"] == "M / M | Other") | (
        new_df["gender_combo"] == "M | Other / M | Other") | (
        new_df["gender_combo"] == "M | F | Other / M | F | Other"), 
        other=True
    )
    new_df["wlw_ship"] = False
    new_df["wlw_ship"] = new_df["wlw_ship"].mask(
        (new_df["gender_combo"] == "F / F") | (
        new_df["gender_combo"] == "F | Other / F") | (
        new_df["gender_combo"] == "F / F | Other") | (
        new_df["gender_combo"] == "F | Other / F | Other"), 
        other=True
    )
    new_df["het_ship"] = False
    new_df["het_ship"] = new_df["het_ship"].mask(
        (new_df["gender_combo"] == "F / M") | (
        new_df["gender_combo"] == "M / F"), 
        other=True
    )
    
    new_df["other_ship"] = False
    new_df["other_ship"] = new_df["other_ship"].mask(
        (new_df["wlw_ship"] == False) & (new_df["mlm_ship"] == False) & (new_df["het_ship"] == False),
        other=True
    )

    # prep canon alignment
    new_df["canon_aligned"] = False
    new_df["canon_conflicted"] = False
    new_df["canon_ambiguous"] = False

    # canon conflicted orientations
    new_df["canon_conflicted"] = new_df["canon_conflicted"].mask(
        (
            (new_df["clean_orientation"].str.contains("str8")) & (
            new_df["het_ship"] == False) # straight ppl in non-straight ships
        ) | (
            (new_df["clean_orientation"].str.contains("gay")) & (
            new_df["het_ship"] == True) # gay ppl in straight ships
        ), 
        other=True
    )

    # if unspecified in orientations -> ambiguous
    new_df["canon_ambiguous"] = new_df["canon_ambiguous"].mask(
        ( # any unspecified members unless it's already conflicted (ex str8/unspecified mlm ship)
            (new_df["clean_orientation"].str.contains("unspecified")) & (
            new_df["canon_conflicted"] == False)
        ) | ( # or chars romancing 2-gender player chars but only interested in one gender option
            (new_df["clean_orientation"] != "bi / woman_attracted") & (
            new_df["clean_orientation"] != "bi / bi") & (
            new_df["other_ship"])
        ), 
        other=True
    )

    # canon aligned orientations
    new_df["canon_aligned"] = new_df["canon_aligned"].mask(
        ( # straight & bi ppl in straight ships
            (
                (new_df["clean_orientation"] == "str8 / str8") | (
                new_df["clean_orientation"] == "str8 / bi") | (
                new_df["clean_orientation"] == "bi / str8") | (
                new_df["clean_orientation"] == "bi / bi")
            ) & (
            new_df["het_ship"] == True)
        ) | ( # gay & bi ppl in mlm or wlw ships
            (
                (new_df["clean_orientation"] == "gay / gay") | (
                new_df["clean_orientation"] == "gay / bi") | (
                new_df["clean_orientation"] == "bi / gay") | (
                new_df["clean_orientation"] == "bi / bi")
            ) & (
                (new_df["wlw_ship"] == True) | new_df["mlm_ship"] == True
            )
        ) | ( # bi char x 2-gender player character or eda & raine whispers or river & doctor (general)
            (
                (new_df["clean_orientation"] == "bi / woman_attracted") | (
                new_df["clean_orientation"] == "bi / bi")
            ) & (
                new_df["other_ship"]
            )
        ), 
        other=True
    )

    return new_df