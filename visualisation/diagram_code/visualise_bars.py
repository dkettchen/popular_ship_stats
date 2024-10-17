import pandas as pd
import plotly.graph_objects as go
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
import visualisation.vis_utils.diagram_utils.labels as lbls
import plotly.express as px
from visualisation.vis_utils.remove_translation import remove_translation


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
def visualise_stacked_bars(input_df:pd.DataFrame, data_case:str, ranking:str):
    """
    visualises output (ranking=(currently implemented:)"total") from 
    - all_characters_racial_groups_df (data_case="minority_racial_groups")
    - total_gender_combo_percent_df (data_case="gender_combos")
    - total_gender_combo_percent_df (data_case="minority_gender_combos") #TODO

    as grouped bar charts with 3 bars in each group
    """
    #making input case insensitive
    data_case = data_case.lower()
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    # defaults to replace
    uniformtext_minsize = 8
    uniformtext_mode = 'hide'
    text_position = None
    x_ticks = None
    marker_color = None

    if data_case == "minority_racial_groups":
        title = f"Racial groups excl. white people, east asians, and ambiguous, unknown and non-human characters{suffix}"
        x_ticks = 10
        text_position = "inside"

        iterable_1 = input_df.index
        iterable_2 = lbls.racial_group_umbrellas
    elif data_case in ["gender_combos", "minority_gender_combos"]:
        if data_case == "gender_combos":
            title = f"Ship gender combinations{suffix}"
            iterable_1 = lbls.gender_combo_umbrellas
        elif data_case == "minority_gender_combos":
            title = f"Ship gender combinations excluding M/M, W/W, and M/F blocks{suffix}"
            uniformtext_minsize = None 
            uniformtext_mode = None
            text_position = "inside"

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

            combo_dict = lbls.gender_combo_umbrellas
            # removing majority labels
            combo_dict["mlm"] = combo_dict["mlm"][1:]
            combo_dict["wlw"] = combo_dict["wlw"][1:]
            combo_dict["non-same-sex"] = combo_dict["non-same-sex"][1:]

            iterable_1 = combo_dict
        iterable_2 = [reversed(iterable_1[item]) for item in iterable_1]
        wlw_count = 0
        mlm_count = 0
        het_count = 0
        ambig_count = 0

    stacked_bars = go.Figure()

    for item in iterable_1:
        if data_case == "minority_racial_groups":

            if "White" in item or \
            ("E Asian" in item and "Ind" not in item) \
            or item in iterable_2["other"].keys():
                continue

        for instance in iterable_2:
            if data_case == "minority_racial_groups":
                # instance is umbrella group
                # item is specific group

                if item in iterable_2[instance]:
                    if instance == "north, west, middle and eastern europe":
                        stack_label = "romani & european indigenous"
                    else:
                        stack_label = instance

                    x = [stack_label]
                    y = input_df.loc[item]
                    text = item
                else: continue # if the group is not in the umbrella group, we check the next one
            elif data_case in ["gender_combos", "minority_gender_combos"]:
            # item is umbrella type
            # instance is specific combo

                colours = colour_palettes.gender_combo_colours[item]

                # setting colours & ticking up counters
                if item == "mlm":
                    colour = colours[mlm_count]
                    mlm_count += 1
                elif item == "wlw":
                    colour = colours[wlw_count]
                    wlw_count += 1
                elif item == "non-same-sex":
                    colour = colours[het_count]
                    het_count += 1
                elif item == "ambiguous":
                    colour = colours[ambig_count]
                    ambig_count += 1

                if data_case == "minority_gender_combos":
                    if instance in gender_combos_we_recognise:
                        text = gender_combos_we_recognise[instance] + f"({instance})"
                    else: text = instance
                else: text = instance

                x = [item]
                y = input_df.loc[instance]

                marker_color = colour

            # add trace to figure
            stacked_bars.add_trace(
                go.Bar(
                    x=x, 
                    y=y, 
                    text=text,
                    marker_color=marker_color # this one varies, so how to make the other one do default?
                )
            )

    stacked_bars.update_layout(
        barmode='stack', 
        showlegend=False, 
        title=title,
    )

    if uniformtext_minsize: # setting uniform text
        stacked_bars.update_layout(
            uniformtext_minsize=uniformtext_minsize, 
            uniformtext_mode=uniformtext_mode,
        )
    if x_ticks: # setting tick angle
        stacked_bars.update_layout(
            xaxis_tickangle=x_ticks,
        )
    if text_position: # setting text position
        stacked_bars.update_traces(
            textposition=text_position,
        )

    return stacked_bars

# grouped bars
def visualise_3_grouped_bars(input_item:pd.DataFrame|pd.Series, data_case:str, ranking:str):
    """
    visualises output (ranking=(currently implemented:)"total") from 
    - total_gender_combos_srs (data_case="no_half_only")
    - highest_of_this_type_df (data_case="top_fandoms")

    as grouped bar charts with 3 bars in each group
    """
    #making input case insensitive
    data_case = data_case.lower()
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    if data_case == "no_half_only":
        title = f"Fandoms with no, over half, or only ships of this type{suffix}"

        # no
        values_1 = input_item.get([
            "no_mlm_ship_fandoms", 
            "no_wlw_ship_fandoms", 
            "no_het_ship_fandoms"
        ])
        # half
        values_2 = input_item.get([
            "more_than_50%_mlm", 
            "more_than_50%_wlw", 
            "more_than_50%_het"
        ])
        # only
        values_3 = input_item.get([
            "only_mlm_ship_fandoms", 
            "only_wlw_ship_fandoms", 
            "only_het_ship_fandoms"
        ])

        labels = ["mlm ships", "wlw ships", "het ships"]
        text = ["no", "over 50%", "only"]
        colours = ['darkmagenta', 'indigo', 'darkorchid']

        y_axes = ['y', 'y2', 'y']
        layout = {
            'yaxis': {'title': 'no/only'},
            'yaxis2': {'title': 'over 50%', 'overlaying': 'y', 'side': 'right'}
        }
    elif data_case == "top_fandoms":
        title = f"Top 3 fandoms with most ships of this type{suffix}"
        top_3_values_df = input_item.copy().get([
            "highest num of mlm ships", 
            "highest num of wlw ships", 
            "highest num of het ships"
        ])
        top_3_fandoms_df = input_item.copy().get([
            "highest mlm fandom", 
            "highest wlw fandom", 
            "highest het fandom"
        ])

        # 1st
        values_1 = top_3_values_df.loc["1st"]
        # 2nd
        values_2 = top_3_values_df.loc["2nd"]
        # 3rd
        values_3 = top_3_values_df.loc["3rd"]

        labels = ["mlm", "wlw", "het"] 
        text = [
            top_3_fandoms_df.loc["1st"],
            top_3_fandoms_df.loc["2nd"].mask(
                cond=top_3_fandoms_df.loc["2nd"] == "A Song of Ice and Fire / Game of Thrones Universe", 
                other="GoT (tied)"
            ),
            top_3_fandoms_df.loc["3rd"].mask(
                cond=top_3_fandoms_df.loc["3rd"] == "Bangtan Boys / BTS", 
                other="BTS"
            ).mask(
                cond=(top_3_fandoms_df.loc["3rd"] == "Homestuck") | (
                    top_3_fandoms_df.loc["3rd"] == "Steven Universe"), 
                other="Homestuck <br>& Steven <br>Universe <br>(tied)"
            ).mask(
                cond=top_3_fandoms_df.loc["3rd"] == "Marvel", 
                other="Marvel (tied)"
            )
        ]
        colours = colour_palettes.medals

        y_axes = ['y', 'y', 'y']
        layout = {}

    grouped_bars = go.Figure(
        data=[
            go.Bar( 
                x=labels,
                y=values_1,
                text=text[0],
                marker_color=colours[0],
                yaxis=y_axes[0], 
                offsetgroup=1,
            ),
            go.Bar( 
                x=labels,
                y=values_2,
                text=text[1],
                marker_color=colours[1],
                yaxis=y_axes[1], 
                offsetgroup=2,
            ),
            go.Bar( 
                x=labels,
                y=values_3,
                text=text[2],
                marker_color=colours[2],
                yaxis=y_axes[2], 
                offsetgroup=3,
            )
        ],
        layout=layout
    )

    grouped_bars.update_layout(
        barmode='group', 
        showlegend=False, 
        title=title)

    return grouped_bars

# non stacked, non grouped bars
def visualise_simple_bar(input_item:pd.DataFrame|pd.Series, data_case:str, ranking:str):
    """
    visualises output (ranking=(currently implemented:)"total") from 
    - highest_racial_diversity_df (data_case="racial_diversity")
    - average_gender_combo_srs (data_case="average_ship_combo")
    - non_white_ships_srs (data_case="non_white_ships")
    - all_characters_gender_df (data_case="minority_genders")
    
    as simple bar charts (not stacked or grouped)
    """
    #making input case insensitive
    data_case = data_case.lower()
    ranking = ranking.lower()
    suffix = lbls.suffixes[ranking]

    # defaults to replace
    df = input_item
    labels = {
            "index": "", # you can rename the axis titles
            "value": "",
        }
    show_legend = False
    x_axis_visible = False # to hide bottom axis annotations
    colour_guide = input_item.index
    colours = None
    traces_marker_colour = None
    y_values = None
    x_values = None

    if data_case == "racial_diversity":
        title = f"Top fandoms for racial diversity{suffix}"
        text = pd.Series(input_item.index).apply(remove_translation)
        colours = px.colors.qualitative.Set1

    elif data_case == "average_ship_combo":
        df = input_item.get(["mlm", "wlw", "hets"])
        title = f"Average ships of this type per fandom{suffix}"
        text = [
            f"mlm ({input_item.loc['mlm']})", 
            f"wlw ({input_item.loc['wlw']})", 
            f"het ({input_item.loc['hets']})"
        ]
        labels["value"] = "average ships per fandom"
        traces_marker_colour = 'indianred'

    elif data_case == "non_white_ships":
        title = f"Pairings with and without white and east asian characters{suffix}"
        text = ["involve white ppl", "involve east asians", "non-white ships", "non-white & non-EA"]
        labels = {
            "index": "characters involved",
            "value": "no of ships",
        }
        #traces_marker_colour = 'green' # update colour here -> for all bars tho
            # replace colours w our new ones?
        colours = colour_palettes.non_white_colours

    elif data_case == "minority_genders":
        title = f"Characters' gender distribution excluding M and F{suffix}"

        gender_list = [
            "M | Other",
            "F | Other",
            "Other",
            "M | F | Other",
            "Ambig",
        ]

        text = [
            "Crowley (Good Omens)<br>Dream (Sandman)<br>Loki (Marvel)<br>Gerard Way<br>Ranboo",
            "Crystal Gems x9<br>Sailor Uranus",
            "Venom Symbiote<br>Raine Whispers",
            "Drag Queens x4",
            "Player Character x6<br>Y/N | Reader x6"
        ]
        labels = {
            "x": "", # you can rename the axis titles
            "y": "",
        }
        y_values = [input_item["count"].loc[tag] for tag in gender_list]
        x_values = gender_list
        colour_guide = gender_list
        colours = [colour_palettes.gender_colours[gender] for gender in gender_list]

        x_axis_visible = True # cause we don't want to remove it here

    if y_values: # if we have specified the values separately
        simple_bars = px.bar(
            x=x_values,
            y=y_values,
            title=title,
            text=text,
            labels=labels
        )
    else: # otherwise just use the automatic dataframe one
        simple_bars = px.bar(
            data_frame=df,
            title=title,
            text=text,
            labels=labels
        )

    simple_bars.update_layout( # hiding legend
        showlegend=show_legend,
    )
    
    if not x_axis_visible: # if we want to hide the x_axis
        simple_bars.update_xaxes(
            visible=x_axis_visible
        )

    # adding colours
    if traces_marker_colour: # if it will all be one colour
        simple_bars.update_traces(
            marker_color=traces_marker_colour
        )
    else: # if we have specified a colour sequence
        simple_bars.update_traces(
            color=colour_guide,
            color_discrete_sequence=colours
        )

    return simple_bars