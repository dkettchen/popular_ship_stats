import pandas as pd
import plotly.graph_objects as go
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count

# multi plots and currently only accounting for two inputs
def visualise_pies(input_df:pd.DataFrame):
    """
    visualise the femslash output from total_multi_nos_by_year ("race" version), 
    total_interracial_ratio as pie charts
    """
    num_of_years = len(input_df.columns)
    fig = make_subplots_by_year(num_of_years) # making appropriate amount of subplots
    max_count = make_max_count(num_of_years)

    row_count = 1
    col_count = 1

    for year in input_df.columns:
        year_series = input_df[year]

        if "multi_chars" in year_series.index:
            labels = ["multiracial characters", "non-multiracial characters"]
            title = "Multiracial characters by year (AO3 femslash ranking 2014-2023)"
            items = 2
        elif "interracial_ships" in year_series.index:
            labels = year_series.index
            title = "Interracial ships by year (AO3 femslash ranking 2014-2023)"
            items = 3
        elif "with_multi_chars" in year_series.index:
            labels = ["with multiracial characters", "w/out multiracial characters"]
            title = "Ships with multiracial characters by year (AO3 femslash ranking 2014-2023)"
            items = 2
        else: print(input_df)

        if items == 2:
            colours = ["orangered", "orange"]
        elif items == 3:
            colours = ["orangered", "gold", "orange"]

        fig.add_trace(go.Pie(
            labels=labels, 
            values=year_series.values, 
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
        #showlegend=False,
    )

    return fig
