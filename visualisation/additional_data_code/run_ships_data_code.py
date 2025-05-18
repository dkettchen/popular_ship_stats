from src.additional_data_fandoms.sort_extra_ship_data import (
    parse_extra_ship_data, 
    assign_to_characters, 
    assign_to_ships
)

parsed_df = parse_extra_ship_data()
# assigned_char_df = assign_to_characters(parsed_df)
assigned_ship_df = assign_to_ships(parsed_df)

# replacing false values with none values for counting
for column in ["mlm_ship", "wlw_ship", "het_ship", "other_ship"]:
    assigned_ship_df[column] = assigned_ship_df[column].where(
        assigned_ship_df[column] != False
    )

def get_total_and_by_ship_type(input_df, column):
    """
    groups df by column, counts non-none columns, 
    and retrieves only total, mlm, wlw, het and other ship values
    """

    new_df = input_df.groupby(column).count().get([
        "slash_ship", "mlm_ship", "wlw_ship", "het_ship", "other_ship"
    ]).rename(columns={"slash_ship":"total"})

    return new_df

# get canon numbers for total & ship types
canon_df = get_total_and_by_ship_type(assigned_ship_df, "canon")

# get incest numbers for total & ship types
incest_df = get_total_and_by_ship_type(assigned_ship_df, "related")

# get canon alignment for total & ship types
aligned_df = get_total_and_by_ship_type(assigned_ship_df, "canon_alignment")

# make pie (for totals) & stacked bar charts (for by ship type)
# incest one can be just for total


# orientation
# totals (str8 ppl, queer ppl, unspecified)
# totals by gender (str8 men, str8 women, mlm, wlw, other, unspecified men, unspecified women)
# orientation by gender (str8, bi, gay, other, unspecified) by male/female