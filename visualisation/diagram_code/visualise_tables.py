from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count
import plotly.graph_objects as go
from pandas import DataFrame
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
import visualisation.vis_utils.diagram_utils.ranks as ranks
import visualisation.vis_utils.diagram_utils.labels as lbls

def visualise_top_5(input_dict:dict, data_case:str, ranking:str):
    """
    takes the output (ranking=(currently implemented:)"femslash") from 
    - top_5_ships (data_case="pairings"), 
    - top_5_fandoms_by_year (data_case="fandoms")

    returns a multi-plot figure visualising the data contained in table format

    the table will be in sapphic/lesbian flag colours if ranking is "femslash"
    """
    #making input case insensitive
    data_case = data_case.lower()
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    num_of_years = len(input_dict.keys())
    
    if ranking == "femslash":
        colours = colour_palettes.sapphic_table

    if data_case == "fandoms":
        no_of_columns = None
        title = f"Top 5 fandoms by ship number and popularity by year{suffix}"
        max_count = make_max_count(num_of_years)
        column_width = [0.3,1,1]
    elif data_case == "pairings":
        no_of_columns = 1
        title = f"Top 5 ships by year{suffix}"
        max_count = 1
        column_width = [0.75,6.5,2.4,1.9]

    fig = make_subplots_by_year(num_of_years, no_of_columns)

    line_colour = colours["lines"] # colour of lines
    header_fill_colour = colours["header"] # colour of header row
    body_fill_colour = colours["body"] # colour of remaining rows

    row_counter = 1
    col_counter = 1

    for year in input_dict:
        year_df = input_dict[year].copy()

        if data_case == "fandoms":
            most_ships_fandoms = clean_fandoms(year_df["most_ships"])
            most_pop_fandoms = clean_fandoms(year_df["most_popular"])
            columns = [year, "most_ships", "most_popular"]
            values = [year_df.index, most_ships_fandoms, most_pop_fandoms]
        elif data_case == "pairings":
            year_df["rank"] = ranks.top_10_list[:5]
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
                columnwidth=column_width # sets column width ratios
            ),
            row=row_counter, col=col_counter
        )

        if col_counter == max_count: # this is always true for "pairings" case
            col_counter = 1
            row_counter += 1
        else: col_counter += 1

    fig.update_layout(
        title=title
    )

    return fig

def visualise_longest_running(input_df:DataFrame, ranking:str):
    """
    takes the output from longest_running_top_5_ships (ranking=(currently implemented:)"femslash")

    returns a single-plot figure visualising the data contained in table format

    the table will be in sapphic/lesbian flag colours if ranking is "femslash"
    """
    #making input case insensitive
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    if ranking == "femslash":
        colours = colour_palettes.sapphic_table
        num_of_years = 9
        column_width = [0.1, 0.95, 0.2]

    line_colour = colours["lines"] # colour of lines
    header_fill_colour = colours["header"] # colour of header row
    body_fill_colour = colours["body"] # colour of remaining rows

    headers = ["rank", "ship", "streak"]
    values = [
        ranks.top_10_list[:5], 
        input_df[input_df.columns[0]], 
        [f"{value}/{num_of_years} years" for value in input_df[input_df.columns[1]]]
    ]

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
            columnwidth=column_width, # sets column width ratios
        ),
        layout={"title":f"Longest running top 5 ships{suffix}"}
    )

    return fig

def visualise_top_non_white_ships(input_dict:dict, ranking:str):
    """
    takes the output from top_non_white_ships (ranking=(currently implemented:)"femslash")

    returns a multi-plot figure visualising the data contained in table format
    """
    #making input case insensitive
    ranking = ranking.lower()

    num_of_years = len(input_dict.keys())
    fig = make_subplots_by_year(num_of_years, num_of_columns=4)
    suffix = lbls.suffixes[ranking]

    colours = colour_palettes.non_white_colours
    if ranking == "femslash":
        line_colour = colour_palettes.sapphic_table["lines"] # colour of lines
        body_fill_colour = colour_palettes.sapphic_table["body_2"] # colour of remaining rows
        column_width = [0.35, 3.05, 1.1, 1.5]

    row_counter = 1
    col_counter = 1
    rank_strings = ranks.top_10_list

    for year in input_dict:
        year_df = input_dict[year].copy()
        # print(year_df) # ['year', 'ship', 'fandom', 'rank_no', 'race_combo', 'ship_type']

        year_df["fandom"] = clean_fandoms(year_df["fandom"]) # cleaning/shortening fandoms
        year_df.pop("year")
        year_df.pop("rank_no")

        for ship_type in lbls.non_white_categories:
            type_df = year_df.where(
                year_df["ship_type"] == ship_type
            ).dropna()

            type_df.pop("ship_type")

            length = len(type_df)
            type_df["rank"] = rank_strings[:length]
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
                    columnwidth=column_width # sets column width ratios
                ),
                row=row_counter, col=col_counter
            )
            
            col_counter += 1

        row_counter += 1
        col_counter = 1

    fig.update_layout(
        title=f"Top 3 ships by race-combo type by year{suffix}"
    )

    return fig
