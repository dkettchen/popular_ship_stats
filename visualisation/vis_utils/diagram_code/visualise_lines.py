import pandas as pd
import plotly.graph_objects as go

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

# no multi plots cause line
def visualise_interracial_lines(input_df:pd.DataFrame):
    """
    visualise the femslash output from total_interracial_ratio as a line chart
    """
    fig = go.Figure(
        data=go.Scatter(
            x=input_df.columns, 
            y=input_df.loc["interracial_ships"],
            text=input_df.loc["interracial_ships"],
            textposition="top center",
            mode="lines+text+markers",
            line={"color": "orangered"},
            name="interracial ships"
        ),
        layout={
            "title": 'Interracial ships by year (AO3 femslash ranking 2014-2023)',
            "plot_bgcolor": "papayawhip",
            "yaxis_rangemode": "tozero",
            "xaxis_tickmode": "linear"
        }
    )
    fig.add_trace(go.Scatter(
        x=input_df.columns, 
        y=input_df.loc["ambiguous_ships"],
        text=input_df.loc["ambiguous_ships"],
        textposition="top center",
        mode="lines+text+markers",
        line={"color": "gold"},
        name="ambiguous ships"
    ))
    fig.add_trace(go.Scatter(
        x=input_df.columns, 
        y=input_df.loc["non-interracial_ships"],
        text=input_df.loc["non-interracial_ships"],
        textposition="top center",
        mode="lines+text+markers",
        line={"color": "orange"},
        name="non-interracial ships"
    ))

    return fig

# no multi plots but needs some adjustments to be reusable
def visualise_average_non_white(input_dict:dict):
    """
    visualise the femslash output from average_non_white_ranking as a line chart
    """

    years = list(input_dict.keys())
    colours = ["skyblue", "lightseagreen", "teal", "darkslategrey"]
    labels = ["white_involved_ship", "e_asian_involved_ship", "non_white_ship", "non_white_or_ea_ship"]

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

    fig = go.Figure(
        data=go.Scatter(
            x=years, 
            y=new_df.loc["white_involved_ship"][:-1],
            mode="lines+markers",
            line={"color": colours[0]},
            name="white_involved_ship"
        ),
        layout={
            "title": 'Average rank by race-combo type by year (AO3 femslash ranking 2014-2023)',
            "plot_bgcolor": "papayawhip",
            "yaxis_autorange": "reversed",
            "yaxis_rangemode": "tozero",
            "xaxis_tickmode": "linear"
        }
    )

    counter = 0
    for label in labels:
        if counter > 0:
            fig.add_trace(go.Scatter(
                x=years, 
                y=new_df.loc[label][:-1],
                mode="lines+markers",
                line={"color": colours[counter]},
                name=label
            ))

        fig.add_trace(go.Scatter(
            x=years, 
            y=[new_df["average"].loc[label] for year in years],
            mode="lines",
            line={"color": colours[counter]},
            opacity=0.5,
            name=label + " (average)"
        ))

        counter += 1

    fig.add_annotation(
        x=2020, y=47,
        text="Single ship that <br>ranked 47th that year",
        showarrow=True,
        arrowhead=1)

    return fig
