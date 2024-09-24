from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def visualise_total_multi_chars(input_df):
    """
    visualise the femslash output from total_multi_chars as pie charts
    """
    year_donuts_fig = make_subplots(rows=3, cols=3, specs=[
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}], 
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}],
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]
    ],)

    row_count = 1
    col_count = 1

    for year in input_df.columns:
        year_series = input_df[year]

        colours = ["orangered", "orange"]

        year_donuts_fig.add_trace(go.Pie(
            labels=["multiracial characters", "non-multiracial characters"], 
            values=year_series.values, 
            hole=0.3, # determines hole size
            title=year, # text that goes in the middle of the hole
            sort=False, # if you want to keep it in its original order rather than sorting by size
            titlefont_size=10, # to format title text
            marker_colors=colours,
            automargin=False,
            textposition="inside"
        ), row_count, col_count)

        if col_count == 3:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    year_donuts_fig.update_traces(
        textinfo='percent',
    )
    year_donuts_fig.update_layout(
        title="Multiracial characters by year (AO3 femslash ranking 2014-2023)", 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        #showlegend=False,
    )

    return year_donuts_fig

def visualise_total_groups(input_srs):
    """
    visualise the femslash output from total_racial_groups as a line chart
    """

    fig = go.Figure(
        data=go.Scatter(
            x=input_srs.index, 
            y=input_srs.values,
            text=input_srs.values,
            textposition="top center",
            mode="lines+text+markers",
            line={"color": "orangered"}
        ),
        layout={
            "title": 'Number of racial groups over the years (AO3 femslash ranking 2014-2023)',
            "plot_bgcolor": "navajowhite",
            "yaxis_rangemode": "tozero",
            "yaxis_tickmode": "linear",
            "xaxis_tickmode": "linear"
        }
    )

    return fig


