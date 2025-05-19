from src.additional_data_fandoms.sort_extra_ship_data import (
    parse_extra_ship_data, 
    assign_to_characters, 
    assign_to_ships
)
from visualisation.diagram_code.visualise_pies import visualise_single_pie
from visualisation.diagram_code.visualise_bars import visualise_stacked_bars

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
# reclass fanon ship as no & rename
new_df = canon_df.transpose()
new_df["No"] = new_df["No"] + new_df["fanon"]
canon_df = new_df.get(["No", "Yes", "One-sided"]).rename(columns={
    "No": "Not canon",
    "Yes": "Canon",
    "One-sided": "Canon one-sided",
}).transpose()

# get incest numbers for total & ship types
incest_df = get_total_and_by_ship_type(assigned_ship_df, "related")
# combine non-blood-related ships into one column & rename
new_df = incest_df.transpose()
new_df["Non-blood-related"] = new_df["adoptive"] + new_df["foster"] + new_df["foster"] + new_df["in-law"] + new_df["step"]
incest_df = new_df.get(["No", "Yes", "Non-blood-related"]).rename(columns={
    "No" : "Not related",
    "Yes": "Blood-related",
}).transpose()

# get canon alignment for total & ship types
aligned_df = get_total_and_by_ship_type(assigned_ship_df, "canon_alignment")

# pie & stacked bar charts for ship data
for data_case in ["canon", "incest", "orientation_alignment"]:
    folder = "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts"

    if data_case == "canon":
        df = canon_df
    elif data_case == "incest":
        df = incest_df
    elif data_case == "orientation_alignment":
        df = aligned_df

    # make totals pie
    pie = visualise_single_pie(df["total"], data_case, "total")
    pie.write_image(
        f"{folder}/additional_diagrams/total_{data_case}.png",
        width = 700,
        height = 700, 
        scale=2
    )

    # make stacked bar charts
    non_total_df = df.copy()
    non_total_df.pop("total")
    bars = visualise_stacked_bars(non_total_df, data_case, "total")
    bars.write_image(
        f"{folder}/additional_diagrams/total_{data_case}_by_gender_combo.png",
        width = 1000,
        height = 700, 
        scale=2
    )


# TODO extract orientations info better

# orientation
# totals (str8 ppl, queer ppl, unspecified)
# totals by gender (str8 men, str8 women, mlm, wlw, other, unspecified men, unspecified women)
# orientation by gender (str8, bi, gay, other, unspecified) by male/female


# refactor/fix TODO:
# - acearo should be counted as conflicted
# - after we're done with these, refactor all your initial bits to 
# later be able to run with 2024 & tumblr data
    # I bet we can make all our parsing stuff WAY more efficient
    # and I wanna find a solution for the multi-graph layouts