import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.sort_race_combos import sort_race_combos
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
import visualisation.vis_utils.diagram_utils.labels as lbls
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup_racial_groups

def visualise_pies(input_item:pd.DataFrame|dict, data_case:str, ranking:str):
    """
    visualise the output (ranking=(currently implemented:)"femslash") from 
    - total_multi_nos_by_year ("race" (data_case="multi_chars") 
    & "race_combo" (data_case="multi_char_ships") version), 
    - total_interracial_ratio (data_case="interracial_ships")
    - rpf_vs_fic (data_case="rpf")
    - sapphic_gender_stats (data_case="gender", ranking="femslash")
    - (data_case="gender", ranking="overall")
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
        #colours = colour_palettes.violets
    elif data_case in ["race", "race_combos"]:
        if ranking == "femslash":
            title_size = 25
        elif ranking == "overall":
            title_size = 12
        min_size = 8
        if data_case == "race":
            title = f"Racial groups by year{suffix}"
            text_info = "label+percent"
            colour_palette = make_colour_lookup_racial_groups()
        elif data_case == "race_combos":
            title = f"Pairing race combinations by year{suffix}"
            text_info = "label"
            colourway = px.colors.qualitative.Pastel + px.colors.qualitative.Prism + \
            px.colors.qualitative.Vivid + px.colors.qualitative.Bold
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
            colours = [colour_palettes.gender_colours[gender] for gender in labels]
        elif data_case in ["race", "race_combos"]:
            labels = year_series.index
            if data_case == "race":
                colours = [colour_palette[label] for label in labels]
            if ranking == "femslash":
                values = [value[0] for value in year_series.values]
            elif ranking == "overall":
                values = year_series.values

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


def visualise_single_pie(input_item:pd.DataFrame|pd.Series, data_case:str, ranking:str):
    """
    visualise the output (ranking=(currently implemented:)"total") from 
    - all_characters_gender_df (data_case="gender")
    - all_characters_racial_groups_df (data_case="racial_groups")
    - plural_vs_monoracial_fandoms_df (data_case="racial_diversity")
    - fandom_market_share_srs (data_case="market_share")
    - interracial_srs (data_case="interracial_ships")
    - rpf_fic_df (data_case="rpf")
    
    as a single pie chart
    """
    #making input case insensitive
    data_case = data_case.lower()
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    if data_case == "racial_diversity": # prepping stuff
        input_item = input_item.get(
            ["fandoms_with_only_one_racial_group", "fandoms_with_multiple_racial_groups"]
        ).transpose().rename(index={
            "fandoms_with_only_one_racial_group": "one group", 
            "fandoms_with_multiple_racial_groups": "multiple groups"
        })

    # defaults to replace
    text_info = "label"
    text_position = None
    auto_margin = None
    inside_text = None
    show_legend = None
    colours = None
    labels = input_item.index

    # values
    if data_case in ["gender", "racial_diversity", "racial_groups", "rpf"]:
        values = input_item["count"]
    elif data_case in ["market_share", "interracial_ships"]:
        values = input_item.values

    # text info
    if data_case in ["racial_diversity", "rpf", "interracial_ships"]:
        text_info += "+percent"
    
    # text position
    if data_case in ["gender", "interracial_ships"]:
        text_position = "outside"
    elif data_case in ["rpf", "racial_groups"]:
        text_position = "inside"

    # auto margin
    if data_case in ["racial_diversity", "market_share", "racial_groups"]:
        auto_margin = False
    
    # show legend
    if data_case in ["racial_diversity", "rpf", "market_share", "interracial_ships"]:
        show_legend = False

    # colours, titles & single case edits
    if data_case == "gender":
        text_info += "+value"
        colours = list(colour_palettes.gender_colours.values())
        title = f"Characters' gender distribution{suffix}"
    elif data_case == "racial_diversity":
        inside_text = "horizontal"
        colours = ["turquoise", "teal"]
        title = f"Fandoms with one vs multiple racial groups{suffix}"
    elif data_case == "rpf":
        colours = ["deeppink", "purple"]
        title = f"Real Person Fic vs Fictional Ships{suffix}"
    elif data_case == "market_share":
        colours = [
            "crimson", "red", "green", "dodgerblue", "orange", "gold"
        ] + px.colors.qualitative.Bold + px.colors.qualitative.Bold
        title = f"Fandoms accounting for more than 1% of ships{suffix}"
    elif data_case == "interracial_ships":
        labels = ["non-interracial", "interracial", "ambiguous"]
        colours = px.colors.qualitative.Prism
        title = f"Interracial vs other ships{suffix}"
    elif data_case == "racial_groups":
        # could colour code this one still/apply a buildin colour thing that looks better than default
        title = f"Characters' racial groups distribution{suffix}"

    # making base figure
    pie = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo=text_info,
            )
        ],
        layout={
            "title":title
        }
    )

    # updating stuff where needed
    if text_position:
        pie.update_traces(textposition=text_position)
    if inside_text:
        pie.update_traces(insidetextorientation=inside_text)
    if auto_margin != None:
        pie.update_traces(automargin=auto_margin)
    if show_legend != None:
        pie.update_layout(showlegend=show_legend)
    if data_case == "gender":
        pie.update_traces(sort=False)
    if data_case == "racial_groups":
        pie.update_traces(insidetextorientation="horizontal")
        pie.update_layout(
            uniformtext_minsize=10, 
            uniformtext_mode='hide'
        )
    else:
        pie.update_traces(marker_colors=colours)
        pass

    return pie
