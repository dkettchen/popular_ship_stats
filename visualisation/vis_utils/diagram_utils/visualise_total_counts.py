import plotly.graph_objects as go
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.sort_race_combos import sort_race_combos
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count
import plotly.express as px

# this one has multi plots
def visualise_sapphic_genders(input_dict:dict):
    """
    visualise the femslash output from sapphic_gender_stats as pie charts
    """
    num_of_years = len(input_dict.keys)
    year_donuts_fig = make_subplots_by_year(num_of_years)
    max_count = make_max_count(num_of_years)

    row_count = 1
    col_count = 1

    for year in input_dict:
        year_df = input_dict[year].copy().reset_index()

        colours = ["deeppink", "violet", "darkorchid"]

        year_donuts_fig.add_trace(go.Pie(
            labels=year_df["gender"], 
            values=year_df["count"], 
            hole=0.3, # determines hole size
            title=year, # text that goes in the middle of the hole
            sort=False, # if you want to keep it in its original order rather than sorting by size
            titlefont_size=10, # to format title text
            marker_colors=colours,
            automargin=False,
            textposition="inside"
        ), row_count, col_count)

        if col_count == max_count:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    year_donuts_fig.update_traces(
        textinfo='percent',
    )
    year_donuts_fig.update_layout(
        title="Genders by year (AO3 femslash ranking 2014-2023)", 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        #showlegend=False,
    )

    return year_donuts_fig

# multi plots
def visualise_total_race_percent(input_dict:dict):
    """
    visualise the femslash output from total_race_nos_by_year ("race" and 
    "race_combo" version) as pie charts
    """
    num_of_years = len(input_dict.keys)
    year_donuts_fig = make_subplots_by_year(num_of_years)
    max_count = make_max_count(num_of_years)

    if "E Asian / White" in input_dict[2023].index:
        title = "Pairing race combinations by year (AO3 femslash ranking 2014-2023)"
        labels = "label"
        is_combos = True
    else: 
        title = "Racial groups by year (AO3 femslash ranking 2014-2023)"
        labels = "label+percent"
        is_combos = False

    row_count = 1
    col_count = 1

    for year in input_dict:
        year_srs = input_dict[year].copy()
        if is_combos:
            rename_dict = sort_race_combos(year_srs.index)
            year_srs = year_srs.rename(index=rename_dict)
            year_srs = year_srs.groupby(
                year_srs.index
            ).aggregate("sum").sort_values(
                by="count", ascending=False
            )

        values = [value[0] for value in year_srs.values]

        year_donuts_fig.add_trace(go.Pie(
            labels=year_srs.index, 
            values=values, 
            hole=0.3, # determines hole size
            title=year, # text that goes in the middle of the hole
            sort=False, # if you want to keep it in its original order rather than sorting by size
            titlefont_size=25, # to format title text
            automargin=False,
            textposition="inside"
        ), row_count, col_count)

        if col_count == max_count:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    year_donuts_fig.update_traces(
        textinfo=labels,
    )
    year_donuts_fig.update_layout(
        title=title, 
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        colorway=px.colors.qualitative.Pastel + px.colors.qualitative.Prism + \
            px.colors.qualitative.Vivid + px.colors.qualitative.Bold,
        #showlegend=False,
    )

    return year_donuts_fig
