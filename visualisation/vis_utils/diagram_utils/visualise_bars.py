import pandas as pd
import plotly.graph_objects as go
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
import visualisation.vis_utils.diagram_utils.labels as lbls

# no multi plots but would need title adjusted
def visualise_non_white_counts(input_df:pd.DataFrame, ranking:str):
    """
    visualises the output from count_non_white_ships (ranking=(currently implemented:)"femslash") 
    as a grouped bar chart
    """
    fig = go.Figure()

    text = ["involve white ppl", "involve east asians", "non-white ships", "non-white & non-EA"]
    colours = colour_palettes.non_white_colours
    labels = [str(year)[:-2] for year in input_df.index]
    
    counter = 0

    suffix = lbls.suffixes[ranking]
    if ranking == "femslash":
        bg_colour = colour_palettes.sapphic_table["body_2"]

    for column in input_df.columns:
        values = input_df[column]

        fig.add_trace(
            go.Bar(
                x=labels,
                y=values,
                marker_color=colours[counter],
                name=text[counter],
            )
        )

        counter += 1

    fig.update_layout(
        barmode='group', 
        title=f"Pairings with and without white and east asian characters{suffix}",
        plot_bgcolor=bg_colour,
    )
    
    return fig
