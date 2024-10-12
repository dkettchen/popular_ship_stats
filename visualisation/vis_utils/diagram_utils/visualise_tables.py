from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count
import plotly.graph_objects as go
from pandas import DataFrame

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

#
def visualise_top_5_pairings(input_dict:dict):
    """
    takes the output from top_5_wlw

    returns a figure visualising the data contained in lesbian flag coloured table format
    """
    num_of_years = len(input_dict.keys)
    fig = make_subplots_by_year(num_of_years, 1)

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

# so many multi plots oh god but hopefully salvageable o.o
def visualise_top_non_white(input_dict:dict):
    """
    takes the output from top_non_white_ships

    returns a figure visualising the data contained in table format
    """
    num_of_years = len(input_dict.keys)
    fig = make_subplots_by_year(num_of_years, num_of_columns=4)

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
