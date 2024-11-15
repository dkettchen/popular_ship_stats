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
from visualisation.vis_utils.df_utils.retrieve_numbers import get_label_counts, get_unique_values_list
from visualisation.vis_utils.rename_gender_combos import rename_gender_combos
from visualisation.vis_utils.sort_race_combos import sort_race_combos

def visualise_pies(input_item:pd.DataFrame|dict, data_case:str, ranking:str):
    """
    visualise 
    - numbers of relevant data case per year:
        - data_case="multi_chars", ranking="femslash"|"overall"|"annual"
        - data_case="multi_char_ships", ranking="femslash"|"overall"|"annual"
        - data_case="interracial_ships", ranking="femslash"|"overall"|"annual"
        - data_case="rpf", ranking="femslash"|"overall"|"annual"
        - data_case="gender", ranking="femslash"|"overall"|"annual"
        - data_case="race", ranking="femslash"|"overall"|"annual"
        - data_case="race_combos", ranking="femslash"|"overall"|"annual"
        - data_case="fic_type", ranking="overall"|"annual"
        - data_case="gender_combos", ranking="overall"|"annual"
        - data_case="ships_by_country", ranking="femslash"|"overall"|"annual"
        - data_case="ships_by_continent", ranking="femslash"|"overall"|"annual"
        - data_case="ships_by_language", ranking="femslash"|"overall"|"annual"

    - demographic data about the top 100 most popular ships of all time 
    (data_case="most_popular_ships", ranking="femslash"|"overall"|"annual")
    
    as pie charts
    """
    #making input case insensitive
    data_case = data_case.lower()
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    # making subplots
    if data_case == "most_popular_ships":
        if ranking != "femslash":
            fig = make_subplots_by_year(3,3)
            max_count = 3
        else:
            fig = make_subplots_by_year(2,2)
            max_count = 2
    else: # retrieving years
        if data_case in [
            "multi_chars", 
            "multi_char_ships", 
            "interracial_ships", 
            "most_popular_ships"
        ]: # dfs
            years = input_item.columns
        elif data_case in [
            "rpf", 
            "gender", 
            "race", 
            "race_combos", 
            "fic_type", 
            "gender_combos",
            "ships_by_country", 
            "ships_by_continent",
            "ships_by_language"
        ]: # dict
            years = input_item.keys()

        num_of_years = len(years)
        fig = make_subplots_by_year(num_of_years) # making appropriate amount of subplots
        max_count = make_max_count(num_of_years)

        if num_of_years == 9:
            title_size = 10
        else: title_size = 12
        min_size = 12

    row_count = 1
    if ranking == "annual" and data_case != "most_popular_ships":
        col_count = 2 # skipping first one due to uneven number of years
    else: col_count = 1

    text_info = 'percent'
    colours = None
    colourway = None

    if data_case == "most_popular_ships": # special non-years case
        title = f"Top 100 most popular ships of all time{suffix}"
        for pie in ["gender_combo", "race_combo", "rpf_or_fic"]:
            if ranking == "femslash" and pie == "gender_combo":
                continue

            data = input_item.copy()
            if pie == "gender_combo": # renaming gender combos
                data = rename_gender_combos(data, column=True)
            elif pie == "race_combo": # renaming race combos
                race_combo_list = get_unique_values_list(data, pie)
                race_combo_rename_dict = sort_race_combos(race_combo_list)
                renamed_values = []
                for combo in data[pie]:
                    if combo in race_combo_rename_dict.keys():
                        renamed_values.append(race_combo_rename_dict[combo])
                    else:
                        renamed_values.append(combo)
                data[pie] = renamed_values

            data = get_label_counts(data, pie)

            labels = list(data.index)
            values = data["count"]
            # assigning colours
            if pie == "gender_combo":
                colours = [colour_palettes.gender_combo_dict[combo] for combo in labels]
                pie_title = "gender<br>combos"
            elif pie == "race_combo":
                racial_group_colour_dict = make_colour_lookup_racial_groups()
                colours = []
                for combo in labels:
                    if combo in racial_group_colour_dict.keys():
                        colours.append(racial_group_colour_dict[combo]) # same race pairings
                    elif "White" in combo:
                        colours.append(colour_palettes.non_white_colours[0]) # white involved
                    elif combo[:7] == "E Asian" or " E Asian" in combo:
                        colours.append(colour_palettes.non_white_colours[1]) # east asian involved
                    elif "Ambig" in combo:
                        colours.append("khaki") # ambig involved
                    else:
                        colours.append("blue") # idk
                pie_title = "race<br>combo"
            elif pie == "rpf_or_fic":
                colours = ["deeppink", "darkred"]
                pie_title = "rpf<br>or fic"
            
            fig.add_trace(go.Pie(
                labels=labels, 
                values=values,
                hole=0.3, # determines hole size
                title=pie_title, # text that goes in the middle of the hole
                titlefont_size=18, # to format title text
                marker_colors=colours,
                automargin=False,
                textposition="inside", 
                textinfo="label",
                marker_line=dict(color='white', width=1)
            ), row_count, col_count)
            
            if col_count == max_count:
                col_count = 1
                row_count += 1
            else:
                col_count += 1


        # adding title, uniform text, and colourway if any
        fig.update_layout(
            title=title, 
            uniformtext_minsize=12,
            uniformtext_mode="hide",
            showlegend=False
        )

    else: # any case with year plots
        # most titles & colours & any static labels
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
        elif data_case in ["race", "race_combos"]:
            if ranking == "femslash":
                title_size = 25
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
        elif data_case == "fic_type":
            title = f"General vs slash ships by year{suffix}"
            colours = ["hotpink", "yellowgreen"]
            labels = ["slash", "gen"]
        elif data_case == "gender_combos":
            title = f"Gender combos by year{suffix}"
        elif data_case in ["ships_by_country", "ships_by_continent","ships_by_language"]:
            if data_case == "ships_by_country": 
                by_what = "country"
            elif data_case == "ships_by_continent":
                by_what = "continent"
            elif data_case == "ships_by_language":
                by_what = "language"
            title = f"Number of ships by {by_what}{suffix}"
            text_info = "label"
            min_size = 8
        else: print(input_item)

        for year in years:
            # retrieving year data
            if data_case == "gender":
                year_df = input_item[year].copy().reset_index()
                year_series = year_df["count"]
            elif data_case == "race_combos":
                year_series = input_item[year].copy()
                rename_dict = sort_race_combos(year_series.index)
                year_series = year_series.rename(index=rename_dict)
                year_series = year_series.groupby(
                    year_series.index
                ).aggregate("sum")
                if type(year_series) == pd.DataFrame:
                    year_series = year_series.sort_values(
                        by="count", ascending=False
                    )
                else: year_series = year_series.sort_values(ascending=False)
            else:    
                year_series = input_item[year].copy()

            # defaults to replace for certain cases
            values = year_series.values
            # replacing values where needed
            if data_case in [
                "interracial_ships",
                "ships_by_country",
                "ships_by_continent",
                "ships_by_language"
            ]:
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
                values = year_series.values
            elif data_case == "gender_combos":
                labels = year_series.index
                colours = [colour_palettes.gender_combo_dict[combo] for combo in labels]

            # adding pie
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

        # adding text info
        fig.update_traces(
            textinfo=text_info,
        )
        # adding title, uniform text, and colourway if any
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
    visualise the most popular fandoms each year by number of ships 
    (must contain column "no_of_ships" in every year's dataframe) or weighted by ranks 
    (must contain column "rank_sum" in every year's dataframe value)
    as pie charts

    fandom colour lookup dictionary can be made using make_colour_lookup helper from 
    visualisation/vis_utils/make_colour_lookup.py
    """
    #making input case insensitive
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    num_of_years = len(input_dict.keys())
    fig = make_subplots_by_year(num_of_years)
    max_count = make_max_count(num_of_years)

    row_count = 1
    if ranking == "annual":
        col_count = 2 # skipping first one due to uneven number of years
    else: col_count = 1

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
    visualises
    - characters' gender distribution (data_case="gender", ranking="total")
    - racial groups (data_case="racial_groups", ranking="total")
    - fandoms with only one or multiple racial groups (data_case="racial_diversity", ranking="total")
    - fandoms with most ships (data_case="market_share", ranking="total")
    - number of interracial, non-interracial and ambiguous pairings 
    (data_case="interracial_ships", ranking="total")
    - number of RPF and fictional ships (data_case="rpf", ranking="total")
    
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
