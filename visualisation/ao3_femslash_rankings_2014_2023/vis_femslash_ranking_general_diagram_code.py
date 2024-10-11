from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas import DataFrame

# multi plots -> not adjustable without a buncha work
def visualise_market_share_and_popularity(input_dict:dict, colour_lookup:dict):
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
        year_df = input_dict[year].copy()
        
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

#
def visualise_top_5_fandoms(input_dict:dict):
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

        if col_counter == 3:
            col_counter = 1
            row_counter += 1
        else: col_counter += 1

    fig.update_layout(
        title="Top 5 fandoms by ship number and popularity by year (AO3 femslash ranking 2014-2023)"
    )

    return fig

#
def visualise_rpf_vs_fic(input_dict:dict):
    """
    visualise the femslash output from rpf_vs_fic as pie charts
    """
    year_donuts_fig = make_subplots(rows=3, cols=3, specs=[
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}], 
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}],
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]
    ],)

    row_count = 1
    col_count = 1

    for year in input_dict:
        year_df = input_dict[year].copy()

        colours = ["deeppink", "darkred"]

        year_donuts_fig.add_trace(go.Pie(
            labels=["RPF", "fictional"], 
            values=[year_df.loc["RPF"]["no_of_ships"], year_df.loc["fictional"]["no_of_ships"]], 
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
        title="Real Person Fic vs fictional ships by year (AO3 femslash ranking 2014-2023)", 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        #showlegend=False,
    )

    return year_donuts_fig

#
def visualise_top_5_pairings(input_dict:dict):
    """
    takes the output from top_5_wlw

    returns a figure visualising the data contained in lesbian flag coloured table format
    """

    fig = make_subplots(
        rows=9, cols=1,
        # shared_xaxes=True,
        # vertical_spacing=0.03,
        specs=[
            [{"type": "table"}],[{"type": "table"}],[{"type": "table"}],
            [{"type": "table"}],[{"type": "table"}],[{"type": "table"}],
            [{"type": "table"}],[{"type": "table"}],[{"type": "table"}],
        ]
    )

    line_colour = 'deeppink' # colour of lines
    header_fill_colour = 'lightsalmon' # colour of header row
    body_fill_colour = 'mistyrose' # colour of remaining rows

    row_counter = 1
    col_counter = 1

    for year in input_dict:
        year_df = input_dict[year].copy()

        year_df["rank"] = ["1st", "2nd", "3rd", "4th", "5th"]
        new_column_order = list(year_df.columns[-1:]) + list(year_df.columns[:-1])
        year_df = year_df[new_column_order] # putting rank as first column

        year_df["fandom"] = clean_fandoms(year_df["fandom"]) # cleaning/shortening fandoms
        year_df.pop("rpf_or_fic") # removing unneeded columns
        year_df.pop("year")

        columns = [year] + list(year_df.columns[1:])
        values = [year_df[column] for column in year_df.columns]

        fig.add_trace(
            go.Table(
                header=dict(
                    values=columns, # column names for header row
                    align='left', # aligns header row text
                    line_color=line_colour,
                    fill_color=header_fill_colour,
                ),
                cells=dict(
                    values=values, # values ordered by column
                    align='left', # aligns body text
                    line_color=line_colour,
                    fill_color=body_fill_colour,
                ),
                columnwidth=[0.75,6.5,2.4,1.9] # sets column width ratios
            ),
            row=row_counter, col=col_counter
        )

        row_counter += 1

    fig.update_layout(
        title="Top 5 ships by year (AO3 femslash ranking 2014-2023)"
    )

    return fig

# no multi plots! but would need colour, title & year number adjusted
def visualise_longest_running(input_df:DataFrame):
    """
    takes the output from longest_running_top_5_ships

    returns a figure visualising the data contained in lesbian flag coloured table format
    """

    line_colour = 'deeppink' # colour of lines
    header_fill_colour = 'lightsalmon' # colour of header row
    body_fill_colour = 'mistyrose' # colour of remaining rows

    headers = ["rank", "ship", "streak"]
    values = [["1st", "2nd", "3rd", "4th", "5th"], input_df[input_df.columns[0]], [f"{value}/9 years" for value in input_df[input_df.columns[1]]]]

    fig = go.Figure(
        data=go.Table(
            header=dict(
                values=headers, # column names for header row
                align='left', # aligns header row text
                line_color=line_colour,
                fill_color=header_fill_colour,
            ),
            cells=dict(
                values=values, # values ordered by column
                align='left', # aligns body text
                line_color=line_colour,
                fill_color=body_fill_colour,
            ),
            columnwidth=[0.1, 0.95, 0.2], # sets column width ratios
        ),
        layout={"title":"Longest running top 5 ships (AO3 femslash ranking 2014-2023)"}
    )

    return fig

# also no multi plots, but would need title & file paths adjusted
def visualise_hottest_sapphic(input_dict:dict):
    """
    takes the femslash output from hottest_char

    creates png files visualising the data contained in lesbian flag coloured table format 
    for each year (ie a file per each year)
    """

    line_colour = 'deeppink' # colour of lines
    header_fill_colour = 'lightsalmon' # colour of header row
    body_fill_colour = 'mistyrose' # colour of remaining rows

    for year in input_dict:
        year_df = input_dict[year]["over_3_ships"].copy()

        year_df["fandom"] = clean_fandoms(year_df["fandom"]) # cleaning/shortening fandoms
        year_df.pop("rpf_or_fic") # removing unneeded columns
        year_df.pop("year")

        columns = year_df.columns
        values = [year_df[column] for column in year_df.columns]

        fig = go.Figure(
            data=go.Table(
                header=dict(
                    values=columns, # column names for header row
                    align='left', # aligns header row text
                    line_color=line_colour,
                    fill_color=header_fill_colour,
                ),
                cells=dict(
                    values=values, # values ordered by column
                    align='left', # aligns body text
                    line_color=line_colour,
                    fill_color=body_fill_colour,
                ),
                columnwidth=[1.9,0.7,0.6,0.2,3] # sets column width ratios
            ),
            layout={
                "title":f"Hottest characters (in 3+ ships) in {year} (AO3 femslash ranking 2014-2023)"
            }
        )

        fig.write_image(
            f"visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/hottest_sapphics_by_year/hottest_femslash_characters_{year}_2014_2023.png", 
            width=1350, 
            height=350, 
            scale=2
        )

# this one has multi plots
def visualise_sapphic_genders(input_dict:dict):
    """
    visualise the femslash output from sapphic_gender_stats as pie charts
    """
    year_donuts_fig = make_subplots(rows=3, cols=3, specs=[
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}], 
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}],
        [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]
    ],)

    row_count = 1
    col_count = 1

    for year in input_dict:
        year_df = input_dict[year].copy().reset_index()

        colours = ["deeppink", "violet", "darkorchid"]

        year_donuts_fig.add_trace(go.Pie(
            labels=year_df["gender"], 
            values=year_df["count"], 
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
        title="Genders by year (AO3 femslash ranking 2014-2023)", 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        #showlegend=False,
    )

    return year_donuts_fig