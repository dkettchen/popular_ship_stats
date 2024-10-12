from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
import pandas as pd
import plotly.graph_objects as go
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year

# no multi plots but would need title adjusted
def visualise_non_white_counts(input_df:pd.DataFrame):
    """
    visualises the output from count_non_white_ships as a grouped bar chart
    """
    text = ["involve white ppl", "involve east asians", "non-white ships", "non-white & non-EA"]
    colours = ["skyblue", "lightseagreen", "teal", "darkslategrey"]
    fig = go.Figure()
    labels = [str(year)[:-2] for year in input_df.index]
    counter = 0

    for column in input_df.columns:
        values = input_df[column]

        fig.add_trace(
            go.Bar(
                x=labels,
                y=values,
                # text=text[counter],
                marker_color=colours[counter],
                name=text[counter],
            )
        )

        counter += 1

    fig.update_layout(
        barmode='group', 
        # showlegend=False, 
        title="Pairings with and without white and east asian characters (AO3 femslash ranking 2014-2023)",
        plot_bgcolor="papayawhip",
    )
    
    return fig
