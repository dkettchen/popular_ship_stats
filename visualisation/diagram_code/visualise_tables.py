from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count
import plotly.graph_objects as go
import pandas as pd
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
import visualisation.vis_utils.diagram_utils.ranks as ranks
import visualisation.vis_utils.diagram_utils.labels as lbls
from visualisation.vis_utils.rename_gender_combos import rename_gender_combos
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup_racial_groups, make_colour_lookup

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
    elif ranking == "overall":
        colours = colour_palettes.blue_table

    if data_case == "fandoms":
        no_of_columns = None
        title = f"Top 5 fandoms by ship number and popularity by year{suffix}"
        max_count = make_max_count(num_of_years)
        column_width = [0.3,1,1]
    elif data_case == "pairings":
        no_of_columns = 2
        max_count = 2
        if ranking == "femslash":
            title = f"Top 5 ships by year{suffix}"
            rank_nos = ranks.top_10_list[:5]
            column_width = [0.75,6.5,2.4,1.9]
        else:
            title = f"Top 10 ships by year{suffix}"
            rank_nos = ranks.top_10_list
            column_width = [0.75,10.4,2.2,1.7,2.7]

    fig = make_subplots_by_year(num_of_years, no_of_columns)

    line_colour = colours["lines"] # colour of lines
    header_fill_colour = colours["header"] # colour of header row
    body_fill_colour = colours["body"] # colour of remaining rows

    row_counter = 1
    if ranking in ["femslash"]:
        col_counter = 2
    else: col_counter = 1

    for year in input_dict:
        year_df = input_dict[year].copy()

        if data_case == "fandoms":
            most_ships_fandoms = clean_fandoms(year_df["most_ships"])
            most_pop_fandoms = clean_fandoms(year_df["most_popular"])
            columns = [year, "most_ships", "most_popular"]
            values = [year_df.index, most_ships_fandoms, most_pop_fandoms]
        elif data_case == "pairings":
            year_df["rank"] = rank_nos
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

        if col_counter == max_count:
            col_counter = 1
            row_counter += 1
        else: col_counter += 1

    fig.update_layout(
        title=title
    )

    return fig

def visualise_hottest_chars(input_dict:dict, ranking:str):
    """
    takes the output (ranking=(currently implemented:)"femslash") from hottest_char

    creates png files visualising the data contained in table format 
    for each year (ie a file per each year)

    the table will be in sapphic/lesbian flag colours if ranking is "femslash"
    """
    #making input case insensitive
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]
    
    if ranking == "femslash":
        colours = colour_palettes.sapphic_table
        column_width = [1.9,0.7,0.5,0.3,3]
        width = 1350
        height = 350
    elif ranking == "overall":
        colours = colour_palettes.blue_table
        column_width = [1.43,0.4,0.32,0.1,0.1,2.7,0.2]
        width = 1750
        height = 500

    line_colour = colours["lines"] # colour of lines
    header_fill_colour = colours["header"] # colour of header row
    body_fill_colour = colours["body"] # colour of remaining rows

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
                columnwidth=column_width # sets column width ratios
            ),
            layout={
                "title":f"Hottest characters (in 3+ ships) in {year}{suffix}"
            }
        )

        if ranking == "femslash":
            filepath = f"visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/hottest_sapphics_by_year/hottest_femslash_characters_{year}_2014_2023.png"
        elif ranking == "overall":
            filepath = f"visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_hottest_chars/hottest_overall_characters_{year}_2014_2023.png"

        fig.write_image(
            filepath,
            width=width, 
            height=height, 
            scale=2
        )

# make single table
def visualise_single_table(input_df:pd.DataFrame, ranking:str, data_case:str=None):
    """
    takes the output from 
    - longest_running_top_5_ships (ranking="femslash")
    - make_hottest_char_df (ranking="total")

    returns a single table visualising the data contained

    the table will be in sapphic/lesbian flag colours if ranking is "femslash"

    it will be in blue colours if ranking is "total"
    """
    #making input case insensitive
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    new_df = input_df.copy()

    # setting column width, title, headers, values
    if ranking == "total":
        column_width = [0.3,0.1,1.4,0.07]
        title = f"Hottest characters (in 3+ ships){suffix}"
        headers = list(new_df.columns)
        values = [
            new_df["fandom"], 
            new_df["rank"], 
            new_df["names"], 
            new_df["no"],
        ]
    elif data_case == "longest_streak":
        if ranking == "femslash":
            column_width = [0.1, 0.95, 0.2]
            top_number = 5
            num_of_years = 9
            rank_nos = ranks.top_10_list[:5]
        elif ranking == "overall":
            column_width = [0.07, 1.1, 0.17]
            top_number = 10
            num_of_years = 10
            rank_nos = ["1st","1st","1st","1st","1st","1st","7th","7th"] + ranks.top_10_list[8:]
        title = f"Longest running top {top_number} ships{suffix}"
        headers = ["rank", "ship", "streak"]
        values = [
            rank_nos,
            new_df[new_df.columns[0]], 
            [f"{value}/{num_of_years} years" for value in new_df[new_df.columns[1]]],
        ]
    elif data_case == "most_popular_characters":
        new_df = new_df.head(100)
        title = f"Top 100 most popular ships of all time{suffix}"
        if ranking == "femslash":
            column_width = [0.1,1.3,0.37,0.45,0.17]
            headers = ["rank", "ship", "fandom", "race combo", "rpf or fic"]
            values = [
                [num for num in range(1, 101)],
                new_df["ship"], 
                clean_fandoms(new_df["fandom"]),
                new_df["race_combo"],
                new_df["rpf_or_fic"],
            ]
        elif ranking == "overall":
            column_width = [0.1,1.6,0.45,0.3,0.45,0.2]
            headers = ["rank", "ship", "fandom", "gender combo", "race combo", "rpf or fic"]
            values = [
                [num for num in range(1, 101)],
                new_df["ship"], 
                clean_fandoms(new_df["fandom"]),
                new_df["gender_combo"],
                new_df["race_combo"],
                new_df["rpf_or_fic"],
            ]

    # colours:
        # setting base colour palette
    if ranking == "femslash":
        colours = colour_palettes.sapphic_table
    else: colours = colour_palettes.blue_table

    line_colour = colours["lines"] # colour of lines
    header_fill_colour = colours["header"] # colour of header row

    if data_case == "most_popular_characters": # setting custom colour coding for body & text!
        if ranking != "femslash": # gender combo column
            clean_gender_combos = rename_gender_combos(new_df, column=True)

            gender_colours = [colour_palettes.gender_combo_dict[combo] for combo in clean_gender_combos["gender_combo"]]
            gender_text_colours = ["white" if combo != "M / M | Other" else "black" for combo in clean_gender_combos["gender_combo"]]

        racial_group_colour_dict = make_colour_lookup_racial_groups()
        
        race_colours = []
        for combo in new_df["race_combo"]:
            if combo in racial_group_colour_dict.keys():
                race_colours.append(racial_group_colour_dict[combo]) # same race pairings
            elif "White" in combo:
                race_colours.append(colour_palettes.non_white_colours[0]) # white involved
            elif combo[:7] == "E Asian" or " E Asian" in combo:
                race_colours.append(colour_palettes.non_white_colours[1]) # east asian involved
            elif "Ambig" in combo:
                race_colours.append("khaki") # ambig involved
            else:
                race_colours.append(colours["body"])

        rpf_colours = ["deeppink" if rpf_type == "RPF" else "darkred" for rpf_type in new_df["rpf_or_fic"]]
        rpf_text_colours = ["black" if rpf_type == "RPF" else "white" for rpf_type in new_df["rpf_or_fic"]]

        fandom_colour_dict = make_colour_lookup(new_df)

        if ranking == "overall":
            notable_fandoms = [ # 18 repeated fandoms in overall (27 non-repeating)
                "Supernatural", 
                "One Direction", 
                "Bangtan Boys / BTS", 
                "Marvel", 
                "Harry Potter Universe",
                "Sherlock", 
                "Teen Wolf",
                "Star Trek", 
                "Star Wars",
                "The 100",
                "Once Upon a Time",
                "DC",
                "My Hero Academia | 僕のヒーローアカデミア",
                "Youtube",
                "Stargate",
                "Haikyuu!! | ハイキュー!!",
                "Attack on Titan | 進撃の巨人",
                "Voltron"
            ]
        elif ranking == "femslash":
            notable_fandoms = [ # 19 repeated fandoms in femslash (42 non-repeating)
                "Marvel", 
                "Harry Potter Universe",
                "Teen Wolf",
                "The 100",
                "Once Upon a Time",
                "DC",
                "My Hero Academia | 僕のヒーローアカデミア",
                "Attack on Titan | 進撃の巨人",
                "RWBY",
                "Buffy Universe",
                "Homestuck",
                "Steven Universe",
                "Riverdale",
                "Carmilla",
                "Women's Soccer",
                "Dragon Age",
                "Doctor Who",
                "Glee",
                "Overwatch"
            ]

        fandom_colours = []
        fandom_text_colours = []
        for fandom in new_df["fandom"]:
            if fandom in notable_fandoms:
                fandom_colours.append(fandom_colour_dict[fandom])
                if fandom not in [
                    "Stargate", 
                    "Star Trek", 
                    "Glee", 
                    "Homestuck", 
                    "Attack on Titan | 進撃の巨人",
                    "The 100",
                    "Voltron"
                ]:
                    fandom_text_colours.append("white")
                else: fandom_text_colours.append("black")
            else:
                fandom_colours.append(colours["body"])
                fandom_text_colours.append("black")

        body_fill_colour = []
        text_colour = []
        for header in headers:
            if header == "gender combo":
                body_fill_colour.append(gender_colours)
                text_colour.append(gender_text_colours)
            elif header == "race combo":
                body_fill_colour.append(race_colours)
                text_colour.append("black")
            elif header == "rpf or fic":
                body_fill_colour.append(rpf_colours)
                text_colour.append(rpf_text_colours)
            elif header == "fandom":
                body_fill_colour.append(fandom_colours)
                text_colour.append(fandom_text_colours)
            else:
                body_fill_colour.append(colours["body"])
                text_colour.append("black")
    else:
        body_fill_colour = colours["body"] # colour of remaining rows
        text_colour = "black"

    # making figure
    fig = go.Figure(
        data=go.Table(
            header=dict(
                values=headers, # column names for header row
                align='left', # aligns header row text
                line_color=line_colour,
                fill_color=header_fill_colour,
                font_color="black"
            ),
            cells=dict(
                values=values, # values ordered by column
                align='left', # aligns body text
                line_color=line_colour,
                fill_color=body_fill_colour,
                font_color=text_colour
            ),
            columnwidth=column_width, # sets column width ratios
        ),
        layout={"title":title}
    )

    return fig

# make columns of table plots with years number of rows
def visualise_column_tables(input_dict:dict, data_case:str, ranking:str):
    """
    takes a dict with year keys

    returns multi-plot figure with columns of tables for each category and rows for each year
    visualising the top 3 ships of each category each year

    - data_case="non_white_ships", ranking="femslash"|"overall"
    - data_case="gender_combos", ranking="overall"
    """
    #making input case insensitive
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    # setting column num, header colours, ship types, title, column width
    if data_case == "non_white_ships":
        num_of_columns = 4
        colours = colour_palettes.non_white_colours
        ship_types = lbls.non_white_categories
        title = f"Top 3 ships by race-combo type by year{suffix}"
        column_width = [0.35, 3.05, 1.1, 1.5]
    elif data_case == "gender_combos":
        num_of_columns = 3
        colours = [
            colour_palettes.gender_combo_dict["M / M"], 
            colour_palettes.gender_combo_dict["F / F"], 
            colour_palettes.gender_combo_dict["M / F"],
        ]
        ship_types = ["mlm", "wlw", "hets"]
        title = f"Top 10 ships by gender-combo by year{suffix}"
        column_width = [0.2, 3.9, 0.9, 1.1]

    # making subplots
    num_of_years = len(input_dict.keys())
    fig = make_subplots_by_year(num_of_years, num_of_columns=num_of_columns, by_years=True)
    
    # setting colours
    if ranking == "femslash":
        line_colour = colour_palettes.sapphic_table["lines"] # colour of lines
    elif ranking == "overall":
        line_colour = colour_palettes.blue_table["lines"]
    body_fill_colour = colour_palettes.bg_colours[ranking][0]

    row_counter = 1
    col_counter = 1
    rank_strings = ranks.top_10_list

    for year in input_dict:
        # making year item
        if data_case == "non_white_ships":
            year_item = input_dict[year].copy() # df

            year_item["fandom"] = clean_fandoms(year_item["fandom"]) # cleaning/shortening fandoms
            year_item.pop("year")
            year_item.pop("rank_no")
        elif data_case == "gender_combos":
            year_item = input_dict[year] # dict

        for ship_type in ship_types: # iterating through ship types
            # making df per type
            if data_case == "non_white_ships":
                type_df = year_item.where(
                    year_item["ship_type"] == ship_type
                ).dropna()

                type_df.pop("ship_type")
            elif data_case == "gender_combos":
                type_df = year_item[ship_type]
                type_df["fandom"] = clean_fandoms(type_df["fandom"]) # cleaning/shortening fandoms
                type_df.pop("year")
                type_df.pop("gender_combo")
                type_df.pop("rpf_or_fic")

            # adding ranks
            length = len(type_df)
            type_df["rank"] = rank_strings[:length]
            new_column_order = list(type_df.columns[-1:]) + list(type_df.columns[:-1])
            type_df = type_df[new_column_order] # putting rank as first column

            type_df = type_df.rename(
                columns={"ship":ship_type}
            )

            # setting text & fill colour for headers
            if col_counter in [1,2] and data_case == "non_white_ships":
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

    # adding title
    fig.update_layout(
        title=title
    )

    return fig