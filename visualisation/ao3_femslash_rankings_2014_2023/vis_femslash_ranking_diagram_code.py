from visualisation.vis_utils.remove_translation import remove_translation
from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualise_market_share_and_popularity(input_dict, colour_lookup):
    """
    visualise the femslash output from fandom_market_share_by_year 
    or fandoms_popularity_by_year as pie charts
    """
    year_donuts_fig = make_subplots(rows=3, cols=3, specs=[
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}], 
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}],
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]
    ],)

    row_count = 1
    col_count = 1

    if "no_of_ships" in input_dict[2023].columns:
        femslash_title = "Fandoms (> 1 ship) by market share by year (AO3 femslash ranking 2014-2023)"
        column_name = "no_of_ships"
    elif "rank_sum" in input_dict[2023].columns:
        femslash_title = "Top 15 fandoms by popularity by year (AO3 femslash ranking 2014-2023)"
        column_name = "rank_sum"

    for year in input_dict:
        year_df = input_dict[year]
        
        fandoms = clean_fandoms(year_df.index)
        ships_no = year_df[column_name]

        colours = list(year_df.reset_index()["fandom"].apply(lambda x: colour_lookup[x]))

        year_donuts_fig.add_trace(go.Pie(
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

        if col_count == 3:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    year_donuts_fig.update_traces(
        textinfo='label',
        # marker=dict(
        #     #colors=px.colors.qualitative.Bold + px.colors.qualitative.Bold, # to use colours
        #     line=dict(color='#000000', width=2) # to add outline
        # )
    )
    year_donuts_fig.update_layout(
        title=femslash_title, 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        showlegend=False,
        # colorway=list(colour_lookup.values())
        # px.colors.qualitative.Bold + \
        #     px.colors.qualitative.Pastel + \
        #     px.colors.qualitative.Prism + \
        #     px.colors.qualitative.Vivid
    )

    return year_donuts_fig

def visualise_top_5_fandoms(input_dict):
    """
    takes the output from top_5_fandoms_by_year

    returns a figure visualising the data contained in lesbian flag coloured table format
    """
    fig = make_subplots(
        rows=3, cols=3,
        # shared_xaxes=True,
        # vertical_spacing=0.03,
        specs=[
            [{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"}],
            [{"type": "table"},{"type": "table"},{"type": "table"}],
        ]
    )

    line_colour = 'deeppink' # colour of lines
    header_fill_colour = 'lightsalmon' # colour of header row
    body_fill_colour = 'mistyrose' # colour of remaining rows

    row_counter = 1
    col_counter = 1

    for year in input_dict:
        year_df = input_dict[year]

        most_ships_fandoms = clean_fandoms(year_df["most_ships"])
        most_pop_fandoms = clean_fandoms(year_df["most_popular"])

        fig.add_trace(
            go.Table(
                header=dict(
                    values=[year, "most_ships", "most_popular"], # column names for header row
                    align='left', # aligns header row text
                    line_color=line_colour,
                    fill_color=header_fill_colour,
                ),
                cells=dict(
                    values=[
                        year_df.index, 
                        most_ships_fandoms, 
                        most_pop_fandoms, 
                    ], # values ordered by column
                    align='left', # aligns body text
                    line_color=line_colour,
                    fill_color=body_fill_colour,
                ),
                columnwidth=[0.3,1,1] # sets column width ratios
            ),
            row=row_counter, col=col_counter
        )

        if col_counter == 3:
            col_counter = 1
            row_counter += 1
        else: col_counter += 1

    fig.update_layout(
        title="Top 5 fandoms by ship number and popularity by year (AO3 femslash ranking 2014-2023)"
    )

    return fig

