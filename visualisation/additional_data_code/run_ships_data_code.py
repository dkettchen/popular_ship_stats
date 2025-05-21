from src.additional_data_fandoms.sort_extra_ship_data import (
    parse_extra_ship_data, 
    assign_to_characters, 
    assign_to_ships
)
from visualisation.diagram_code.visualise_pies import visualise_single_pie
from visualisation.diagram_code.visualise_bars import visualise_stacked_bars
import pandas as pd

folder = "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts"

parsed_df = parse_extra_ship_data()
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


assigned_char_df = assign_to_characters(parsed_df).replace({False:None})

# extract numbers
# orientation labels
orientation_totals = assigned_char_df.groupby("orientation").count()["full_name"]
# other categories
for column in ["queer", "wlw", "mlm", "man_attracted", "woman_attracted", "other_attracted"]:
    orientation_totals[column] = assigned_char_df[f"canon_{column}"].count()
# orientations by male/female
orientation_by_gender = assigned_char_df.groupby(
    ["gender", "orientation"]
).count()["full_name"].reset_index().rename(columns={"full_name" : "total"})
for label in ["str8", "bi", "gay", "unspecified", "acearo"]:
    orientation_totals[f"{label}_women"] = orientation_by_gender.where(
        ((orientation_by_gender["gender"] == "F") | (orientation_by_gender["gender"] == "F | Other")) & (
        orientation_by_gender["orientation"] == label)
    ).dropna(how="all")["total"].sum()

    orientation_totals[f"{label}_men"] = orientation_by_gender.where(
        ((orientation_by_gender["gender"] == "M") | (
            orientation_by_gender["gender"] == "M | Other") | (
            orientation_by_gender["gender"] == "M | F | Other")) & (
        orientation_by_gender["orientation"] == label)
    ).dropna(how="all")["total"].sum()

# orientation
# totals (str8 ppl, queer ppl, unspecified)
totals = orientation_totals.get(["str8", "queer", "unspecified"])
# by attraction (woman, man, other attracted) (minus unspecified I guess)
totals_by_attraction = orientation_totals.get(["woman_attracted", "man_attracted", "other_attracted"])
# totals by gender (str8 men, str8 women, mlm, wlw, other, unspecified men, unspecified women)
totals_by_gender = orientation_totals.get([
    "str8_men", "str8_women", 
    "mlm", "wlw", 
    "unspecified_men", "unspecified_women",
    "acearo_men", "acearo_women",
])
# orientation by gender (str8, bi, gay, other, unspecified) by male/female
gender_orientations = pd.DataFrame(
    {"men": {
        "str8": orientation_totals["str8_men"],
        "gay": orientation_totals["gay_men"],
        "bi": orientation_totals["bi_men"],
        "acearo": orientation_totals["acearo_men"],
        "unspecified": orientation_totals["unspecified_men"],
    },
    "women": {
        "str8": orientation_totals["str8_women"],
        "gay": orientation_totals["gay_women"],
        "bi": orientation_totals["bi_women"],
        "acearo": orientation_totals["acearo_women"],
        "unspecified": orientation_totals["unspecified_women"],
    }}
)


for data_case in [
    "orientation_totals", # pie
    "orientation_by_attraction", # pie
    "orientation_men", # pie
    "orientation_women", # pie
    "orientation_labels_by_gender" # stacked bars
]:
    # TODO make data cases in diagram thingies

    if data_case in [
        "orientation_totals",
        "orientation_by_attraction",
        "orientation_men",
        "orientation_women",
    ]:

        if data_case == "orientation_totals":
            df = totals
        elif data_case == "orientation_by_attraction":
            df = totals_by_attraction
        elif data_case == "orientation_men":
            df = totals_by_gender.get([
                "str8_men", 
                "mlm",
                "unspecified_men", 
                "acearo_men", 
            ])
        elif data_case == "orientation_women":
            df = totals_by_gender.get([
                "str8_women", 
                "wlw",
                "unspecified_women",
                "acearo_women",
            ])

        df = df.where(df.values > 0).dropna(how="all")

        # make totals pie
        pie = visualise_single_pie(df, data_case, "total")
        pie.write_image(
            f"{folder}/additional_diagrams/total_{data_case}.png",
            width = 700,
            height = 700, 
            scale=2
        )

    elif data_case == "orientation_labels_by_gender":
        df = gender_orientations

        # make totals pie
        pie = visualise_stacked_bars(df, data_case, "total")
        pie.write_image(
            f"{folder}/additional_diagrams/total_{data_case}.png",
            width = 1000,
            height = 700, 
            scale=2
        )

# print(assigned_char_df.columns)
# print(orientation_totals)    

# refactor/fix TODO:
# - after we're done with these, refactor all your initial bits to 
# later be able to run with 2024 & tumblr data
    # I bet we can make all our parsing stuff WAY more efficient
    # and I wanna find a solution for the multi-graph layouts