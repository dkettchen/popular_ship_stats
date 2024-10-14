import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.sort_race_combos import sort_race_combos
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
import visualisation.vis_utils.diagram_utils.labels as lbls

def visualise_pies(input_item:pd.DataFrame|dict, data_case:str, ranking:str):
    """
    visualise the output (ranking=(currently implemented:)"femslash") from 
    - total_multi_nos_by_year ("race" (data_case="multi_chars") 
    & "race_combo" (data_case="multi_char_ships") version), 
    - total_interracial_ratio (data_case="interracial_ships")
    - rpf_vs_fic (data_case="rpf")
    
    as pie charts
    """
    suffix = lbls.suffixes[ranking]

    if data_case in ["multi_chars", "multi_char_ships", "interracial_ships"]:
        years = input_item.columns
    elif data_case in ["rpf"]:
        years = input_item.keys()

    num_of_years = len(years)
    fig = make_subplots_by_year(num_of_years) # making appropriate amount of subplots
    max_count = make_max_count(num_of_years)

    row_count = 1
    col_count = 1

    for year in years:
        if data_case == "rpf":
            year_series = input_item[year]["no_of_items"]
        else:    
            year_series = input_item[year]

        if data_case == "multi_chars":
            labels = ["multiracial characters", "non-multiracial characters"]
            title = f"Multiracial characters by year{suffix}"
            items = 2
        elif data_case == "multi_char_ships":
            labels = ["with multiracial characters", "w/out multiracial characters"]
            title = f"Ships with multiracial characters by year{suffix}"
            items = 2
        elif data_case == "interracial_ships":
            labels = year_series.index
            title = f"Interracial ships by year{suffix}"
            items = 3
        elif data_case == "rpf":
            labels = ["RPF", "fictional"]
            title = f"Real Person Fic vs fictional ships by year{suffix}"
            items = 2
        else: print(input_item)

        if items == 2:
            if data_case == "rpf":
                colours = ["deeppink", "darkred"]
            else: 
                colours = [colour_palettes.oranges[0], colour_palettes.oranges[2]]
        elif items == 3:
            colours = colour_palettes.oranges

        fig.add_trace(go.Pie(
            labels=labels, 
            values=year_series.values, # ⭕ check that this is the right way around for rpf
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

    fig.update_traces(
        textinfo='percent',
    )
    fig.update_layout(
        title=title, 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
    )

    return fig

# leaving this one separate due to different sizing & more complicated colouring process
def visualise_market_share_and_popularity(input_dict:dict, colour_lookup:dict, ranking:str):
    """
    visualise the output (ranking=(currently implemented:)"femslash") from
    - fandom_market_share_by_year 
    - fandoms_popularity_by_year 
    
    as pie charts
    """
    suffix = lbls.suffixes[ranking]

    num_of_years = len(input_dict.keys)
    fig = make_subplots_by_year(num_of_years)
    max_count = make_max_count(num_of_years)

    row_count = 1
    col_count = 1

    if "no_of_ships" in input_dict[2023].columns:
        femslash_title = f"Fandoms (> 1 ship) by market share by year{suffix}"
        column_name = "no_of_ships"
    elif "rank_sum" in input_dict[2023].columns:
        femslash_title = f"Top 15 fandoms by popularity by year{suffix}"
        column_name = "rank_sum"

    for year in input_dict:
        year_df = input_dict[year].copy()
        
        fandoms = clean_fandoms(year_df.index)
        ships_no = year_df[column_name]

        colours = list(year_df.reset_index()["fandom"].apply(lambda x: colour_lookup[x]))

        fig.add_trace(go.Pie(
            labels=fandoms, 
            values=ships_no, 
            hole=0.3, # determines hole size
            title=year, # text that goes in the middle of the hole
            sort=False, # if you want to keep it in its original order rather than sorting by size
            titlefont_size=25, # to format title text
            marker_colors=colours,
            automargin=False,
            textposition="inside"
        ), row_count, col_count)

        if col_count == max_count:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    fig.update_traces(
        textinfo='label',
    )
    fig.update_layout(
        title=femslash_title, 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        showlegend=False,
    )

    return fig



#TODO: refactor these two to be added to visualise_pies ideally, 
# or to be unified in one func if that's not possible

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
