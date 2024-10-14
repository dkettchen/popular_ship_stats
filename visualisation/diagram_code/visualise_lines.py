import pandas as pd
import plotly.graph_objects as go
import visualisation.vis_utils.diagram_utils.labels as lbls
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes

# no multi plots but "" -> would need titles etc adjusted
def visualise_line(input_item:dict|pd.Series):
    """
    visualise the femslash output from total_multi_nos_by_year ("race" version), 
    total_racial_groups as line charts
    """

    if "multi_chars" in input_item.index: # total_multi_chars
        x = input_item.columns
        y = input_item.loc["multi_chars"]
        title = 'Multiracial characters by year (AO3 femslash ranking 2014-2023)'
    elif type(input_item) == pd.Series: # total_racial_groups
        x = input_item.index
        y = input_item.values
        title = 'Number of racial groups over the years (AO3 femslash ranking 2014-2023)'
    elif "with_multi_chars" in input_item.index:
        x = input_item.columns
        y = input_item.loc["with_multi_chars"]
        title = "Ships with multiracial characters by year (AO3 femslash ranking 2014-2023)"

    fig = go.Figure(
        data=go.Scatter(
            x=x, 
            y=y,
            text=y,
            textposition="top center",
            mode="lines+text+markers",
            line={"color": "orangered"}
        ),
        layout={
            "title": title,
            "plot_bgcolor": "papayawhip",
            "yaxis_rangemode": "tozero",
            "yaxis_tickmode": "linear",
            "xaxis_tickmode": "linear"
        }
    )

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

def visualise_multi_lines(input_item:pd.DataFrame|dict, ranking:str):
    """
    visualise the output (ranking=(currently implemented:)"femslash") from 
    - total_interracial_ratio (line for interracial, ambig, & non-interracial pairings)
    - average_non_white_ranking (actual values + average line per each category)
    
    as a line chart with multiple lines
    """

    suffix = lbls.suffixes[ranking]
    if ranking == "femslash":
        bg_colour = colour_palettes.sapphic_table["body_2"]

    if type(input_item) == pd.DataFrame: # if it's interracial ships case
        new_df = input_item.copy()
        years = new_df.columns

        data_case = "interracial_ships"

        categories = lbls.interracial_categories
        labels = ["interracial ships", "ambiguous ships", "non-interracial ships"]
        colours = colour_palettes.oranges
        title = f'Interracial ships by year{suffix}'

        mode = "lines+text+markers"
        auto_range = "reversed"
    elif type(input_item) == dict: # if it's non-white ships case
        years = list(input_item.keys())
        new_df = make_average_non_white_df(input_item)

        data_case = "non_white_ships"

        labels = lbls.non_white_categories
        colours = colour_palettes.non_white_colours
        title =  f'Average rank by race-combo type by year{suffix}'

        mode = "lines+markers"
        auto_range = True

    counter = 0
    for label in labels:
        # determining y values
        if data_case == "non_white_ships":
            y = new_df.loc[label][:-1]
        elif data_case == "interracial_ships":
            y = new_df.loc[categories[0]] # also text

        if counter == 0: # starting figure on first label
            fig = go.Figure(
                data=go.Scatter(
                    x=years, 
                    y=y,
                    text=y,
                    mode=mode,
                    line={"color": colours[counter]},
                    name=label
                ),
                layout={
                    "title": title,
                    "plot_bgcolor": bg_colour,
                    "yaxis_autorange": auto_range,
                    "yaxis_rangemode": "tozero",
                    "xaxis_tickmode": "linear"
                }
            )
        elif counter > 0: # adding traces for each subsequent label
            fig.add_trace(go.Scatter(
                x=years, 
                y=y,
                text=y,
                textposition="top center",
                mode=mode,
                line={"color": colours[counter]},
                name=label
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

        counter += 1

    if data_case == "non_white_ships": # adding custom annotation for this case
        fig.add_annotation(
            x=2020, y=47,
            text="Single ship that <br>ranked 47th that year",
            showarrow=True,
            arrowhead=1)

    return fig