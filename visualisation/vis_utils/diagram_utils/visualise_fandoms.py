from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count
import plotly.graph_objects as go

# multi plots -> not adjustable without a buncha work
def visualise_market_share_and_popularity(input_dict:dict, colour_lookup:dict):
    """
    visualise the femslash output from fandom_market_share_by_year 
    or fandoms_popularity_by_year as pie charts
    """
    num_of_years = len(input_dict.keys)
    fig = make_subplots_by_year(num_of_years)
    max_count = make_max_count(num_of_years)

    row_count = 1
    col_count = 1

    if "no_of_ships" in input_dict[2023].columns:
        femslash_title = "Fandoms (> 1 ship) by market share by year (AO3 femslash ranking 2014-2023)"
        column_name = "no_of_ships"
    elif "rank_sum" in input_dict[2023].columns:
        femslash_title = "Top 15 fandoms by popularity by year (AO3 femslash ranking 2014-2023)"
        column_name = "rank_sum"

    for year in input_dict:
        year_df = input_dict[year].copy()
        
        fandoms = clean_fandoms(year_df.index)
        ships_no = year_df[column_name]

        colours = list(year_df.reset_index()["fandom"].apply(lambda x: colour_lookup[x]))

        fig.add_trace(go.Pie(
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

        if col_count == max_count:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    fig.update_traces(
        textinfo='label',
    )
    fig.update_layout(
        title=femslash_title, 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        showlegend=False,
    )

    return fig

#
def visualise_top_5_fandoms(input_dict:dict):
    """
    takes the output from top_5_fandoms_by_year

    returns a figure visualising the data contained in lesbian flag coloured table format
    """
    num_of_years = len(input_dict.keys)
    fig = make_subplots_by_year(num_of_years)
    max_count = make_max_count(num_of_years)

    line_colour = 'deeppink' # colour of lines
    header_fill_colour = 'lightsalmon' # colour of header row
    body_fill_colour = 'mistyrose' # colour of remaining rows

    row_counter = 1
    col_counter = 1

    for year in input_dict:
        year_df = input_dict[year].copy()

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

        if col_counter == max_count:
            col_counter = 1
            row_counter += 1
        else: col_counter += 1

    fig.update_layout(
        title="Top 5 fandoms by ship number and popularity by year (AO3 femslash ranking 2014-2023)"
    )

    return fig
