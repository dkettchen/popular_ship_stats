import pandas as pd
import plotly.graph_objects as go
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
import visualisation.vis_utils.diagram_utils.labels as lbls
import plotly.express as px
from visualisation.ao3_all_data_2013_2023.vis_characters_file import make_all_groupings_dict


def visualise_non_white_counts(input_df:pd.DataFrame, ranking:str):
    """
    visualises the output from count_non_white_ships (ranking=(currently implemented:)"femslash") 
    as a grouped bar chart
    """
    #making input case insensitive
    ranking = ranking.lower()

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


# stacked bars

def visualise_gender_minorities(total_gender_percentages:pd.DataFrame):
    """
    takes output dataframe from all_characters_gender_df

    returns a stacked bar chart of gender tag numbers excluding M and F blocks
    """

    gender_list = [
        "M | Other",
        "F | Other",
        "Other",
        "M | F | Other",
        "Ambig",
    ]
    colours = [
        "darkturquoise",
        "red",
        "yellow",
        "gold",
        "green",
    ]
    values = [total_gender_percentages["count"].loc[tag] for tag in gender_list]
    bar_text = [
        "Crowley (Good Omens)<br>Dream (Sandman)<br>Loki (Marvel)<br>Gerard Way<br>Ranboo",
        "Crystal Gems x9<br>Sailor Uranus",
        "Venom Symbiote<br>Raine Whispers",
        "Drag Queens x4",
        "Player Character x6<br>Y/N | Reader x6"
    ]

    gender_minority_fig = px.bar(
        x=gender_list,
        y=values,
        title="Characters' gender distribution excluding M and F (AO3 2013-2023)",
        text=bar_text,
        labels={
            "x": "", # you can rename the axis titles
            "y": "",
        },
        color=gender_list,
        color_discrete_sequence=colours
    )

    gender_minority_fig.update_layout(
        showlegend=False,
    )

    return gender_minority_fig

def visualise_racial_minority_totals(total_race_percentages:pd.DataFrame):
    """
    takes output dataframe from all_characters_racial_groups_df

    returns a stacked bar diagram visualising all racial groups other than white people, 
    east asians, and ambiguous, unknown and non-human characters
    """
    all_groupings = make_all_groupings_dict()

    other_racial_group_stacks=go.Figure()

    for index in total_race_percentages.index:
        if "White" in index or (
            "E Asian" in index and "Ind" not in index
        ) or index in all_groupings["other"].keys():
            continue

        for group in all_groupings:
            if index in all_groupings[group]:
                if group == "north, west, middle and eastern europe":
                    stack_label = "romani & european indigenous"
                else:
                    stack_label = group


        # add trace to figure
        other_racial_group_stacks.add_trace(
            go.Bar(
                x=[stack_label], 
                    # stack_label needs to be an array/series/etc of some kind
                    # should only be one value per stack, this is what groups the stacks!
                y=total_race_percentages.loc[index], 
                    # value you want to portray in each portion of the stack
                text=index,
                textposition="inside",
                    # what you want this value to be labelled as
                #marker_color=portion_colour
                    # what colour you want this value to be
            )
        )

    other_racial_group_stacks.update_layout(
        barmode='stack', 
        showlegend=False, 
        title="Racial groups excl. white people, east asians, and ambiguous, unknown and non-human characters (AO3 2013-2023)",
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        xaxis_tickangle=10,
    )

    return other_racial_group_stacks

def visualise_gender_combo_total(total_gender_percentages:pd.DataFrame):
    """
    takes output dataframe from total_gender_combo_percent_df

    returns a stacked bar chart of gender combos grouped by mlm, wlw, non-same-sex and ambiguous
    """
    gender_combo_fig=go.Figure()

    wlw_count = 0
    mlm_count = 0
    het_count = 0
    ambig_count = 0

    combo_dict = {
        "mlm": ["M / M", "M / M | Other","M | Other / M / M",],
        "wlw": ["F / F","F | Other / F | Other", "F / F | Other",],
        "non-same-sex": ["M / F","F / Other","M / Other","F / M / M"],
        "ambiguous": ["M / Ambig","M | Other / Ambig", "F / Ambig","M | F | Other / M | F | Other"]
    }
    for combo_type in combo_dict.keys():
        if combo_type == "mlm":
            colours = ["azure", "turquoise", "steelblue"]
        elif combo_type == "wlw":
            colours = ["red", "orange", "tomato"]
        elif combo_type == "non-same-sex":
            colours = ["silver", "grey", "gainsboro", "black"]
        elif combo_type == "ambiguous":
            colours = ["darkolivegreen", "limegreen", "mediumseagreen", "olive"]

        for combo in reversed(combo_dict[combo_type]):
            if combo_type == "mlm":
                colour = colours[mlm_count]
                mlm_count += 1
            elif combo_type == "wlw":
                colour = colours[wlw_count]
                wlw_count += 1
            elif combo_type == "non-same-sex":
                colour = colours[het_count]
                het_count += 1
            elif combo_type == "ambiguous":
                colour = colours[ambig_count]
                ambig_count += 1

            gender_combo_fig.add_trace(
                go.Bar(
                    x=[combo_type],
                    y=total_gender_percentages.loc[combo],
                    text=combo,
                    marker_color=colour
                )
            )

    gender_combo_fig.update_layout(
        barmode='stack', 
        showlegend=False, 
        title="Ship gender combinations (AO3 2013-2023)",
        uniformtext_minsize=8, 
        uniformtext_mode='hide'
    )

    return gender_combo_fig

def visualise_gender_combo_minorities(total_gender_percentages:pd.DataFrame):
    """
    takes output dataframe from total_gender_combo_percent_df

    returns a stacked bar chart of gender combos excluding standard m/m, f/f, and f/m pairings
    """

    gender_combo_fig=go.Figure()

    gender_combos_we_recognise = {
        "M | Other / M / M" : "Minecraft Youtubers ",
        "F | Other / F | Other" : "Crystal Gems <br>", 
        "F / F | Other" : "Sailor Neptune x Sailor Uranus ",
        "F / Other" : "Eda Clawthorne x Raine Whispers ",
        "M / Other" : "Eddie Brock x Venom ",
        "M | Other / Ambig" : "Loki x Reader ", 
        "M | F | Other / M | F | Other" : "Drag queens <br>",
        "F / M / M": "White Collar characters "
    }

    wlw_count = 0
    mlm_count = 0
    het_count = 0
    ambig_count = 0

    combo_dict = {
        "mlm": ["M / M | Other","M | Other / M / M",],
        "wlw": ["F | Other / F | Other", "F / F | Other",],
        "non-same-sex": ["F / Other","M / Other","F / M / M"],
        "ambiguous": ["M / Ambig","M | Other / Ambig", "F / Ambig","M | F | Other / M | F | Other"]
    }
    for combo_type in combo_dict.keys():
        if combo_type == "mlm":
            colours = ["azure", "turquoise"]
        elif combo_type == "wlw":
            colours = ["red", "orange"]
        elif combo_type == "non-same-sex":
            colours = ["silver", "grey", "gainsboro"]
        elif combo_type == "ambiguous":
            colours = ["darkolivegreen", "limegreen", "mediumseagreen", "olive"]

        for combo in reversed(combo_dict[combo_type]):
            if combo_type == "mlm":
                colour = colours[mlm_count]
                mlm_count += 1
            elif combo_type == "wlw":
                colour = colours[wlw_count]
                wlw_count += 1
            elif combo_type == "non-same-sex":
                colour = colours[het_count]
                het_count += 1
            elif combo_type == "ambiguous":
                colour = colours[ambig_count]
                ambig_count += 1

            if combo in gender_combos_we_recognise:
                label = gender_combos_we_recognise[combo] + f"({combo})"
            else: label = combo

            gender_combo_fig.add_trace(
                go.Bar(
                    x=[combo_type],
                    y=total_gender_percentages.loc[combo],
                    text=label,
                    marker_color=colour,
                    textposition="inside"
                )
            )

    gender_combo_fig.update_layout(
        barmode='stack', 
        showlegend=False, 
        title="Ship gender combinations excluding M/M, W/W, and M/F blocks (AO3 2013-2023)",
        # uniformtext_minsize=8, 
        # uniformtext_mode='hide'
    )

    return gender_combo_fig


# non stacked, non grouped bars

def visualise_highest_racial_diversity(highest_racial_div:pd.DataFrame):
    """
    takes output dataframe from highest_racial_diversity_df

    returns a bar chart visualising it
    """
    highest_racial_div_fig = px.bar(
        data_frame=highest_racial_div,
        title="Top fandoms for racial diversity (AO3 2013-2023)",
        text=pd.Series(highest_racial_div.index).mask(
            cond=highest_racial_div.index == 'Genshin Impact | 原神', 
            other="Genshin"
        ),
        labels={
            "index": "", # you can rename the axis titles
            "value": "",
        },
        color=highest_racial_div.index,
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    highest_racial_div_fig.update_layout(
        showlegend=False,
    ).update_xaxes(
        visible=False # to hide bottom axis annotations
    )

    return highest_racial_div_fig

def visualise_average_ship_combos_per_fandom(average_gender_combo_per_fandom_series:pd.Series):
    """
    takes output series from average_gender_combo_srs

    returns a bar chart visualising the average number of ships by type in a fandom
    """
    average_ships_per_fandom_fig = px.bar(
        data_frame=average_gender_combo_per_fandom_series.get(["mlm", "wlw", "hets"]),
        title="Average ships of this type per fandom (AO3 2013-2023)",
        text=[
            f"mlm ({average_gender_combo_per_fandom_series.loc['mlm']})", 
            f"wlw ({average_gender_combo_per_fandom_series.loc['wlw']})", 
            f"het ({average_gender_combo_per_fandom_series.loc['hets']})"
        ],
        labels={
            "index": "",
            "value": "average ships per fandom",
        },
    )
    average_ships_per_fandom_fig.update_xaxes(
        visible=False
    ).update_traces(
        marker_color='indianred'
    ).update_layout(
        showlegend=False,
    )

    return average_ships_per_fandom_fig

def visualise_non_white_ships(non_white_ships_counts:pd.Series):
    """
    takes output series from non_white_ships_srs

    returns a bar chart visualising the number of ships involving white ppl, involving east 
    asian ppl, non-white ships and ships that involve neither white nor east asian ppl
    """
    non_white_ships_fig = px.bar(
        data_frame=non_white_ships_counts,
        title="Pairings with and without white and east asian characters (AO3 2013-2023)",
        text=["involve white ppl", "involve east asians", "non-white ships", "non-white & non-EA"],
        labels={
            "index": "characters involved",
            "value": "no of ships",
        }
    )
    non_white_ships_fig.update_traces(
        marker_color='green' # update colour here -> for all bars tho
    ).update_layout(
        showlegend=False,
    ).update_xaxes(
        visible=False, # to hide bottom axis annotations
    )

    return non_white_ships_fig



# grouped bars

def visualise_no_half_only(total_gender_combos_series:pd.Series):
    """
    takes output series from total_gender_combos_srs

    returns a grouped bar chart with two y axes visualising how many fandoms had no, 
    only, or over 50% ships of each type
    """
    no_half_only_labels = ["mlm ships", "wlw ships", "het ships"]
    no_ships_values = total_gender_combos_series.get([
        "no_mlm_ship_fandoms", 
        "no_wlw_ship_fandoms", 
        "no_het_ship_fandoms"
    ])
    over_half_values = total_gender_combos_series.get([
        "more_than_50%_mlm", 
        "more_than_50%_wlw", 
        "more_than_50%_het"
    ])
    only_ships_values = total_gender_combos_series.get([
        "only_mlm_ship_fandoms", 
        "only_wlw_ship_fandoms", 
        "only_het_ship_fandoms"
    ])

    no_half_only_fig = go.Figure(
        data=[
            go.Bar( #no
                x=no_half_only_labels,
                y=no_ships_values,
                text="no",
                marker_color='darkmagenta',
                yaxis='y', 
                offsetgroup=1,
            ),
            go.Bar( #over half
                x=no_half_only_labels,
                y=over_half_values,
                text="over 50%",
                marker_color='indigo',
                yaxis='y2', 
                offsetgroup=2,
            ),
            go.Bar( #only
                x=no_half_only_labels,
                y=only_ships_values,
                text="only",
                marker_color='darkorchid',
                yaxis='y', 
                offsetgroup=3,
            )
        ],
        layout={
            'yaxis': {'title': 'no/only'},
            'yaxis2': {'title': 'over 50%', 'overlaying': 'y', 'side': 'right'}
        }
    )

    no_half_only_fig.update_layout(
        barmode='group', 
        showlegend=False, 
        title="Fandoms with no, over half, or only ships of this type (AO3 2013-2023)")

    return no_half_only_fig

def visualise_top_3_per_fandom_df(highest_of_type_df:pd.DataFrame):
    """
    takes output dataframe from highest_of_this_type_df

    returns a grouped bar chart of the top 3 fandoms for number of ships of each type
    """
    type_labels = ["mlm", "wlw", "het"] 
    top_3_values_df = highest_of_type_df.copy().get([
        "highest num of mlm ships", 
        "highest num of wlw ships", 
        "highest num of het ships"
    ])
    top_3_fandoms_df = highest_of_type_df.copy().get([
        "highest mlm fandom", 
        "highest wlw fandom", 
        "highest het fandom"
    ])

    top_3_fandoms_for_ships_by_type_fig = go.Figure(
        data=[
            go.Bar(
                x=type_labels,
                y=top_3_values_df.loc["1st"],
                text=top_3_fandoms_df.loc["1st"], # text that goes on each bar
                marker_color='gold',
            ),
            go.Bar(
                x=type_labels,
                y=top_3_values_df.loc["2nd"],
                text=top_3_fandoms_df.loc["2nd"].mask(
                    cond=top_3_fandoms_df.loc["2nd"] == "A Song of Ice and Fire / Game of Thrones Universe", 
                    other="GoT (tied)"
                ),
                marker_color='slategrey',
            ),
            go.Bar(
                x=type_labels,
                y=top_3_values_df.loc["3rd"],
                text=top_3_fandoms_df.loc["3rd"].mask(
                    cond=top_3_fandoms_df.loc["3rd"] == "Bangtan Boys / BTS", 
                    other="BTS"
                ).mask(
                    cond=(top_3_fandoms_df.loc["3rd"] == "Homestuck") | (top_3_fandoms_df.loc["3rd"] == "Steven Universe"), 
                    other="Homestuck <br>& Steven <br>Universe <br>(tied)"
                ).mask(
                    cond=top_3_fandoms_df.loc["3rd"] == "Marvel", 
                    other="Marvel (tied)"
                ),
                marker_color='chocolate',
            )
        ]
    )

    top_3_fandoms_for_ships_by_type_fig.update_layout(
        barmode='group', 
        showlegend=False, 
        title="Top 3 fandoms with most ships of this type (AO3 2013-2023)", 
    )

    return top_3_fandoms_for_ships_by_type_fig

