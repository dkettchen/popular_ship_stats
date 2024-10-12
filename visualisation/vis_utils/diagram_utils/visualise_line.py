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
