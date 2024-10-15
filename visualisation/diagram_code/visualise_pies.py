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
    - sapphic_gender_stats (data_case="gender", ranking="femslash")
    - total_race_nos_by_year ("race" (data_case="race") & "race_combo" 
    (data_case="race_combos") version)
    
    as pie charts
    """
    #making input case insensitive
    data_case = data_case.lower()
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    if data_case in ["multi_chars", "multi_char_ships", "interracial_ships"]: # dfs
        years = input_item.columns
    elif data_case in ["rpf", "gender", "race", "race_combos"]: # dict
        years = input_item.keys()

    num_of_years = len(years)
    fig = make_subplots_by_year(num_of_years) # making appropriate amount of subplots
    max_count = make_max_count(num_of_years)

    row_count = 1
    col_count = 1

    text_info = 'percent'
    colours = None
    colourway = None
    title_size = 10
    min_size = 12

    if data_case in ["multi_chars", "multi_char_ships",]: 
        colours = [colour_palettes.oranges[0], colour_palettes.oranges[2]]
        if data_case == "multi_chars":
            labels = ["multiracial characters", "non-multiracial characters"]
            title = f"Multiracial characters by year{suffix}"
        elif data_case == "multi_char_ships":
            labels = ["with multiracial characters", "w/out multiracial characters"]
            title = f"Ships with multiracial characters by year{suffix}"
    elif data_case == "interracial_ships":
        title = f"Interracial ships by year{suffix}"
        colours = colour_palettes.oranges
    elif data_case == "rpf":
        labels = ["RPF", "fictional"]
        title = f"Real Person Fic vs fictional ships by year{suffix}"
        colours = ["deeppink", "darkred"]
    elif data_case == "gender":
        title = f"Genders by year{suffix}"
        colours = colour_palettes.violets
    elif data_case in ["race", "race_combos"]:
        colourway = px.colors.qualitative.Pastel + px.colors.qualitative.Prism + \
        px.colors.qualitative.Vivid + px.colors.qualitative.Bold
        title_size = 25
        min_size = 8
        if data_case == "race":
            title = f"Racial groups by year{suffix}"
            text_info = "label+percent"
        elif data_case == "race_combos":
            title = f"Pairing race combinations by year{suffix}"
            text_info = "label"
    else: print(input_item)

    for year in years:
        if data_case == "gender":
            year_df = input_item[year].copy().reset_index()
            year_series = year_df["count"]
        elif data_case == "race_combos":
            year_series = input_item[year].copy()
            rename_dict = sort_race_combos(year_series.index)
            year_series = year_series.rename(index=rename_dict)
            year_series = year_series.groupby(
                year_series.index
            ).aggregate("sum").sort_values(
                by="count", ascending=False
            )
        else:    
            year_series = input_item[year].copy()

        # defaults to replace for certain cases
        values = year_series.values

        if data_case == "interracial_ships":
            labels = year_series.index
        elif data_case == "rpf":
            values = year_series["no_of_ships"]
        elif data_case == "gender":
            labels = year_df["gender"]
            values = year_series
        elif data_case in ["race", "race_combos"]:
            labels = year_series.index
            values = [value[0] for value in year_series.values]

        fig.add_trace(go.Pie(
            labels=labels, 
            values=values,
            hole=0.3, # determines hole size
            title=year, # text that goes in the middle of the hole
            sort=False, # if you want to keep it in its original order rather than sorting by size
            titlefont_size=title_size, # to format title text
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
        textinfo=text_info,
    )
    fig.update_layout(
        title=title, 
        uniformtext_minsize=min_size,
        uniformtext_mode="hide",
        colorway=colourway
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
    #making input case insensitive
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    num_of_years = len(input_dict.keys())
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


# single pies

def visualise_gender_totals(total_gender_percentages:pd.DataFrame):
    """
    takes output dataframe from all_characters_gender_df

    returns a pie chart visualising it
    """
    gender_distr_pie = go.Figure(
        data=[
            go.Pie(
                labels=total_gender_percentages.index,
                values=total_gender_percentages["count"],
                textinfo="label+value",
                textposition="outside",
                sort=False,
                marker=dict(
                    colors=[
                        "darkturquoise",
                        "red",
                        "hotpink",
                        "yellow",
                        "gold",
                        "green",
                        "cornflowerblue",
                    ]
                )
            )
        ]
    )
    gender_distr_pie.update_layout(
        title="Characters' gender distribution (AO3 2013-2023)",
        #showlegend=False, # if you want it to not show the legend
    )

    return gender_distr_pie

# could colour code this one still/apply a buildin colour thing that looks better than default
def visualise_racial_group_totals(total_race_percentages:pd.DataFrame):
    """
    takes output dataframe from all_characters_racial_groups_df

    returns a pie chart visualising it
    """
    all_race_percent_pie = go.Figure(
        data=[
            go.Pie(
                labels=total_race_percentages.index,
                values=total_race_percentages["count"],
                textinfo="label",
                insidetextorientation="horizontal",
                automargin=False,
                # marker=dict(
                    # colors=template colours or builtin colour sequence
                # )
            )
        ]
    )
    all_race_percent_pie.update_traces(textposition='inside')
    all_race_percent_pie.update_layout(
        title="Characters' racial groups distribution (AO3 2013-2023)",
        uniformtext_minsize=10, 
        uniformtext_mode='hide'
    )

    return all_race_percent_pie

def visualise_racial_diversity(plural_vs_monoracial_fandoms:pd.DataFrame):
    """
    takes output dataframe from plural_vs_monoracial_fandoms_df

    returns a pie chart visualising it
    """
    # (dunno why this didn't wanna work without prep code in same cell smh)

    plural_vs_monoracial_fandoms = plural_vs_monoracial_fandoms.get(
        ["fandoms_with_only_one_racial_group", "fandoms_with_multiple_racial_groups"]
    ).transpose().rename(index={
        "fandoms_with_only_one_racial_group": "one group", 
        "fandoms_with_multiple_racial_groups": "multiple groups"
    })

    number_of_groups_by_fandom = go.Figure(
        data=[
            go.Pie(
                labels=plural_vs_monoracial_fandoms.index,
                values=plural_vs_monoracial_fandoms["count"],
                textinfo="label+percent",
                insidetextorientation="horizontal",
                automargin=False,
                marker=dict(
                    colors=["turquoise", "teal"]
                )
            )
        ]
    )

    number_of_groups_by_fandom.update_layout(
        title="Fandoms with one vs multiple racial groups (AO3 2013-2023)",
        showlegend=False, # if you want it to not show the legend
    )

    return number_of_groups_by_fandom

def visualise_fandom_market_share(fandom_market_share:pd.Series):
    """
    takes output series from fandom_market_share_srs

    returns a pie chart of all fandoms that account for more than 1% of total fandoms
    """
    market_share_fig = go.Figure(
        data=[
            go.Pie(
                labels=fandom_market_share.index,
                values=fandom_market_share.values,
                textinfo="label",
                #textposition="outside",
                #insidetextorientation="radial",
                automargin=False,
                marker=dict(
                    colors=[
                        "crimson", "red", "green", "dodgerblue", "orange", "gold"
                    ] + px.colors.qualitative.Bold + px.colors.qualitative.Bold
                )
            )
        ]
    )
    market_share_fig.update_layout(
        title="Fandoms accounting for more than 1% of ships (AO3 2013-2023)",
        showlegend=False,
    )

    return market_share_fig

def visualise_interracial_ships(interracial_ships_counts:pd.Series):
    """
    takes output series from interracial_srs

    returns a pie chart visualising the ratio of interracial, non-interracial and ambiguous ships
    """
    interracial_labels = ["non-interracial", "interracial", "ambiguous"]
    interracial_values = interracial_ships_counts.values

    interracial_pie = go.Figure(
        data=[
            go.Pie(
                labels=interracial_labels,
                values=interracial_values,
                textinfo="label+percent",
                textposition="outside",
                marker=dict(
                    colors=px.colors.qualitative.Prism
                )
            )
        ]
    )
    interracial_pie.update_layout(
        title="Interracial vs other ships (AO3 2013-2023)",
        showlegend=False, # if you want it to not show the legend
    )

    return interracial_pie

def visualise_rpf_fic(rpf_vs_fic_df:pd.DataFrame):
    """
    takes output dataframe from rpf_fic_df

    returns a pie chart showing the ratio of rpf to non-rpf ships
    """
    rpf_pie = go.Figure(
        data=[
            go.Pie(
                labels=rpf_vs_fic_df["count"].index,
                values=rpf_vs_fic_df["count"].values,
                textinfo="label+percent",
                textposition="inside",
                marker=dict(
                    colors=["deeppink", "purple", ]
                )
            )
        ]
    )
    rpf_pie.update_layout(
        title="Real Person Fic vs Fictional Ships (AO3 2013-2023)",
        showlegend=False, # if you want it to not show the legend
    )
    return rpf_pie

