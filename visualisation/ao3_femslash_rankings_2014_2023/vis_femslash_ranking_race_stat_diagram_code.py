from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def visualise_interracial_lines(input_df):
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


def visualise_pies(input_df):
    """
    visualise the femslash output from total_multi_chars, total_interracial_ratio as pie charts
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

        year_donuts_fig.add_trace(go.Pie(
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

        if col_count == 3:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    year_donuts_fig.update_traces(
        textinfo='percent',
    )
    year_donuts_fig.update_layout(
        title=title, 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        #showlegend=False,
    )

    return year_donuts_fig

def visualise_line(input_item):
    """
    visualise the femslash output from total_multi_chars, total_racial_groups as line charts
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


def visualise_non_white_counts(input_df):
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

def visualise_top_non_white(input_dict):
    """
    takes the output from top_non_white_ships

    returns a figure visualising the data contained in table format
    """

    fig = make_subplots(
        rows=9, cols=4,
        # shared_xaxes=True,
        # vertical_spacing=0.03,
        specs=[
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"},{"type": "table"}],
        ]
    )

    colours = ["skyblue", "lightseagreen", "teal", "darkslategrey"]
    line_colour = 'deeppink' # colour of lines
    body_fill_colour = 'papayawhip' # colour of remaining rows

    row_counter = 1
    col_counter = 1
    ranks = ["1st", "2nd", "3rd"]

    for year in input_dict:
        year_df = input_dict[year].copy()
        # print(year_df) # ['year', 'ship', 'fandom', 'rank_no', 'race_combo', 'ship_type']

        year_df["fandom"] = clean_fandoms(year_df["fandom"]) # cleaning/shortening fandoms
        year_df.pop("year")
        year_df.pop("rank_no")

        for ship_type in [
            "white_involved_ship", 
            "e_asian_involved_ship", 
            "non_white_ship", 
            "non_white_or_ea_ship"
        ]:
            type_df = year_df.where(
                year_df["ship_type"] == ship_type
            ).dropna()

            type_df.pop("ship_type")

            length = len(type_df)
            type_df["rank"] = ranks[:length]
            new_column_order = list(type_df.columns[-1:]) + list(type_df.columns[:-1])
            type_df = type_df[new_column_order] # putting rank as first column

            type_df = type_df.rename(
                columns={"ship":ship_type}
            )


            if col_counter in [1,2]:
                header_font = "black"
            else: header_font = "white"
            header_fill_colour = colours[col_counter -1] # colour of header row
            columns = [year] + list(type_df.columns[1:])
            values = [type_df[column] for column in type_df.columns]

            fig.add_trace(
                go.Table(
                    header=dict(
                        values=columns, # column names for header row
                        align='left', # aligns header row text
                        line_color=line_colour,
                        fill_color=header_fill_colour,
                        font_color=header_font,
                    ),
                    cells=dict(
                        values=values, # values ordered by column
                        align='left', # aligns body text
                        line_color=line_colour,
                        fill_color=body_fill_colour,
                    ),
                    columnwidth=[0.35, 3.05, 1.1, 1.5] # sets column width ratios
                ),
                row=row_counter, col=col_counter
            )
            
            col_counter += 1

        row_counter += 1
        col_counter = 1

    fig.update_layout(
        title="Top 3 ships by race-combo type by year (AO3 femslash ranking 2014-2023)"
    )

    return fig


# line graph for average rank?