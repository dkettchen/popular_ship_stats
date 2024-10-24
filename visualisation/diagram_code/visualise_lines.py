import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import visualisation.vis_utils.diagram_utils.labels as lbls
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
from visualisation.vis_utils.df_utils.retrieve_numbers import get_unique_values_list
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup_racial_groups
from visualisation.vis_utils.diagram_utils.calculate_trendline import calculate_trendline

def visualise_line(input_item:dict|pd.Series, data_case:str, ranking:str):
    """
    visualise the output (ranking=(currently implemented:)"femslash") from 
    - total_multi_nos_by_year ("race" (data_case="multi_chars") 
    & "race_combo" (data_case="multi_char_ships") version), 
    - total_racial_groups (data_case="total_racial_groups")
    
    as single line charts
    """
    #making input case insensitive
    data_case = data_case.lower()
    ranking = ranking.lower()

    suffix = lbls.suffixes[ranking]

    # setting colours
    if ranking == "femslash":
        bg_colour = colour_palettes.bg_colours["femslash"][0]
    elif ranking == "overall":
        bg_colour = colour_palettes.bg_colours["overall"][0]
    colour = colour_palettes.oranges[0]

    if data_case == "multi_chars":
        x = [str(column) for column in input_item.columns]
        y = input_item.loc["multi_chars"]
        title = f'Multiracial characters by year{suffix}'
    elif data_case == "total_racial_groups":
        x = [str(index) for index in input_item.index]
        y = input_item.values
        title = f'Number of racial groups over the years{suffix}'
    elif data_case == "multi_char_ships":
        x = [str(column) for column in input_item.columns]
        y = input_item.loc["with_multi_chars"]
        title = f"Ships with multiracial characters by year{suffix}"

    # making figure
    fig = go.Figure(
        data=go.Scatter(
            x=x, 
            y=y,
            text=y,
            textposition="top center",
            mode="lines+text+markers",
            line={"color": colour}
        ),
        layout={
            "title": title,
            "plot_bgcolor": bg_colour,
            "yaxis_rangemode": "tozero",
            "yaxis_tickmode": "linear",
            "xaxis_tickmode": "linear",
            "showlegend": False
        }
    )

    # adding trendline
    trendline_y = calculate_trendline(list(range(1, len(x)+1)), list(y))
    fig.add_trace(go.Scatter(
        x=x, 
        y=trendline_y,
        mode="lines",
        line={"color": colour},
        opacity=0.5,
    ))

    return fig


def make_average_non_white_df(input_dict:dict): # util
    """
    takes input from average_non_white_ranking, turns it into a dataframe ready for visualisation
    """

    years = list(input_dict.keys())
    labels = lbls.non_white_categories

    values = []
    for ship_type in labels:
        temp_list = []
        for year in input_dict:
            if ship_type in input_dict[year].index:
                temp_list.append(input_dict[year]["rank_no"].loc[ship_type])
            else: temp_list.append(None)
        values.append(temp_list)

    new_df = pd.DataFrame(
        columns=years, data=values, index=labels
    )

    new_df["average"] = new_df.mean(axis=1)

    return new_df

def visualise_multi_lines(input_item:pd.DataFrame|dict, data_case:str, ranking:str):
    """
    visualise the output (ranking=(currently implemented:)"femslash") from 
    - total_interracial_ratio (line for interracial, ambig, & non-interracial pairings)
    - average_non_white_ranking (actual values + average line per each category)
    
    as a line chart with multiple lines
    """
    #making input case insensitive
    ranking = ranking.lower()

    suffix = lbls.suffixes[ranking]
    if ranking == "femslash":
        bg_colour = colour_palettes.bg_colours["femslash"][0]
    elif ranking == "overall":
        bg_colour = colour_palettes.bg_colours["overall"][0]
    else:
        bg_colour = "white"

    # making years
    if type(input_item) == dict:
        years = list(input_item.keys())
    elif type(input_item) == pd.DataFrame:
        new_df = input_item.copy()
        years = new_df.columns

    x = years
    if data_case == "interracial_ships":
        categories = lbls.interracial_categories
        labels = ["interracial ships", "ambiguous ships", "non-interracial ships"]
        colours = colour_palettes.oranges
        title = f'Interracial ships by year{suffix}'

        mode = "lines+text+markers"
    elif data_case == "non_white_ships":
        new_df = make_average_non_white_df(input_item)

        labels = lbls.non_white_categories
        colours = colour_palettes.non_white_colours
        title =  f'Average rank by race-combo type by year{suffix}'

        mode = "lines+markers"
    elif data_case == "minority_racial_groups":
        label_list = get_unique_values_list(input_item)
        new_df = pd.DataFrame(index=label_list) # making an index of all racial groups present
        x = [str(year) for year in years]

        # adding all years' values to df
        for year in years:
            year_srs = input_item[year].copy()
            new_df[year] = year_srs
        
        new_df = new_df.transpose()
        for group in ["White","White (Multi)","E Asian","E Asian (Multi)","Unknown","Ambig","N.H."]:
            if group in list(new_df.columns):
                new_df.pop(group)
        new_df = new_df.transpose()
        new_df = new_df.fillna(0)

        # let's make a df that has the categories added up rather than the specifics separate!
        category_df = pd.DataFrame()
        for umbrella in lbls.racial_group_umbrellas:
            if umbrella == "other":
                continue
            umbrella_df = pd.DataFrame()
            for item in lbls.racial_group_umbrellas[umbrella]:
                if item in ["White","White (Multi)","E Asian","E Asian (Multi)"]:
                    continue
                elif umbrella == 'north, west, middle and eastern europe':
                    umbrella = "romani and european indigenous"
                if item in new_df.index:
                    umbrella_df[item] = new_df.loc[item]
            umbrella_df = umbrella_df.transpose()
            umbrella_srs = umbrella_df.agg("sum")
            category_df[umbrella] = umbrella_srs

        category_df = category_df.transpose()
        category_df = category_df.dropna(how="all")
        category_df = category_df.fillna(0)
        new_df = category_df

        labels = list(category_df.index)
        colours = colour_palettes.racial_group_umbrella_colours
        title =  f"Minority racial groups by year{suffix}"

        mode = "lines+markers"

    counter = 0
    for label in labels:
        # determining y values
        if data_case == "non_white_ships":
            y = new_df.loc[label][:-1]
        elif data_case == "interracial_ships":
            y = new_df.loc[categories[counter]] # also text
        elif data_case == "minority_racial_groups":
            y = new_df.loc[label]

        # determining this trace's colour
        if data_case == "minority_racial_groups":
                colour = colours[label]
        else: colour = colours[counter]

        if counter == 0: # starting figure on first label
            fig = go.Figure(
                data=go.Scatter(
                    x=x, 
                    y=y,
                    text=y,
                    textposition="top center",
                    mode=mode,
                    line={"color": colour},
                    name=label,
                ),
                layout={
                    "title": title,
                    "plot_bgcolor": bg_colour,
                    #"yaxis_autorange": auto_range,
                    "yaxis_rangemode": "tozero",
                    "xaxis_tickmode": "linear"
                }
            )
        elif counter > 0: # adding traces for each subsequent label
            fig.add_trace(go.Scatter(
                x=x, 
                y=y,
                text=y,
                textposition="top center",
                mode=mode,
                line={"color": colour},
                name=label,
            ))

        if data_case == "non_white_ships": # adding the average line for each label
            fig.add_trace(go.Scatter(
                x=years, 
                y=[new_df["average"].loc[label] for year in years],
                mode="lines",
                line={"color": colours[counter]},
                opacity=0.5,
                name=label + " (average)"
            ))
        elif data_case in ["minority_racial_groups", "interracial_ships"]:
            
            trendline_y = calculate_trendline(list(range(1, len(years)+1)), list(y))

            fig.add_trace(go.Scatter(
                x=x, 
                y=trendline_y,
                mode="lines",
                line={"color": colour},
                opacity=0.5,
                name=label + " (trendline)",
            ))

        counter += 1

    if data_case == "non_white_ships": # adding custom annotation for this case
        fig.update_layout(
            yaxis_autorange = "reversed"
        )
        fig.add_annotation(
            x=2020, y=47,
            text="Single ship that <br>ranked 47th that year",
            showarrow=True,
            arrowhead=1)

    return fig
