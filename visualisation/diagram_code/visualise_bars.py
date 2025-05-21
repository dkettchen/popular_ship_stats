import pandas as pd
import plotly.graph_objects as go
import visualisation.vis_utils.diagram_utils.colour_palettes as colour_palettes
import visualisation.vis_utils.diagram_utils.labels as lbls
import plotly.express as px
from visualisation.vis_utils.df_utils.make_dfs import sort_df
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup_racial_groups
from visualisation.vis_utils.rename_gender_combos import rename_gender_combos
from visualisation.vis_utils.df_utils.retrieve_numbers import sum_label_nums


def visualise_non_white_counts(input_df:pd.DataFrame, ranking:str):
    """
    visualises the counts of ships with and without white and east asian characters
    as a colour-coded, grouped bar chart
    """
    #making input case insensitive
    ranking = ranking.lower()

    fig = go.Figure()

    text = ["involve white ppl", "involve east asians", "non-white ships", "non-white & non-EA"]
    colours = colour_palettes.non_white_colours
    labels = [str(year)[:-2] for year in input_df.index]

    counter = 0

    suffix = lbls.suffixes[ranking]
    bg_colour = colour_palettes.bg_colours[ranking][0]

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
def visualise_stacked_bars(input_item:pd.DataFrame, data_case:str, ranking:str):
    """
    visualises 
    - racial group counts excluding white, east asian, non-human, racially ambiguous 
    and unknown characters (data_case="minority_racial_groups", ranking="total")
    - gender combination counts grouped by mlm, wlw, non-same-sex, & ambiguous pairings
    (data_case="gender_combos", ranking="total")
    - gender combination counts excluding M/M, F/F, and M/F 
    (data_case="minority_gender_combos", ranking="total")
    - canon by ship type (data_case="canon", ranking="total")
    - incest by ship type (data_case="incest", ranking="total")
    - canon orientation alignment by ship type (data_case="orientation_alignment", ranking="total")
    - men & women's orientations (data_case="orientation_labels_by_gender", ranking="total")

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

        iterable_1 = input_item.index
        iterable_2 = lbls.racial_group_umbrellas

        colour_lookup = make_colour_lookup_racial_groups()
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
        
        wlw_count = 0
        mlm_count = 0
        het_count = 0
        ambig_count = 0

    elif data_case in ["canon", "incest", "orientation_alignment", ]:
        if data_case == "canon":
            title = f"Canon ships by gender combo{suffix}"
            colours = colour_palettes.canon_colours
        elif data_case == "incest":
            title = f"Incest ships by gender combo{suffix}"
            colours = colour_palettes.incest_colours
        elif data_case == "orientation_alignment":
            title = f"Conflicts or aligns with canon orientation by gender combo{suffix}"
            colours = colour_palettes.orientation_alignment

        iterable_1 = input_item.columns
        iterable_2 = input_item.index
    
    elif data_case == "orientation_labels_by_gender":
        title = f"Male and female characters' orientations{suffix}"
        colours = colour_palettes.orientations

        iterable_1 = input_item.columns
        iterable_2 = input_item.index

    stacked_bars = go.Figure()

    for item in iterable_1:
        if data_case == "minority_racial_groups":
            if "White" in item or \
            ("E Asian" in item and "Ind" not in item) \
            or item in iterable_2["other"].keys():
                continue
        elif data_case in ["gender_combos", "minority_gender_combos"]:
            iterable_2 = list(reversed(iterable_1[item]))

        elif data_case in ["canon", "incest", "orientation_alignment", "orientation_labels_by_gender"]:
            total_num = input_item[item].sum()

        for instance in iterable_2:
            if data_case == "minority_racial_groups":
                # instance is umbrella group
                # item is specific group

                if item in iterable_2[instance] \
                or type(input_item) == pd.Series \
                or ranking == "femslash":
                    if instance in ["east asia", "other", "north, west, middle and eastern europe"]:
                        if item not in ["Eu Ind (Multi)", "Romani"]:
                            continue
                        elif instance == "north, west, middle and eastern europe":
                            stack_label = "romani & european indigenous"
                    else:
                        stack_label = instance

                    x = [stack_label]
                    if item == "Māori Ind (Multi)":
                        text = "Māori Ind <br>(Multi)"
                    else: text = item
                    marker_color = colour_lookup[item]

                    # setting y
                    if type(input_item) == pd.Series:
                        if item in iterable_2[instance]:
                            value = input_item.loc[item]
                            y = [value]
                        else:
                            y = [0]
                    elif ranking == "femslash" and item not in iterable_2[instance]:
                        y = [0]
                    else: y = input_item.loc[item]

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
                y = input_item.loc[instance]

                marker_color = colour

            elif data_case in ["canon", "incest", "orientation_alignment", "orientation_labels_by_gender"]:
                current_num = input_item.loc[instance, item]
                if data_case == "orientation_labels_by_gender":
                    x = [item]
                else:
                    x = [item[:-5]]

                if data_case == "orientation_labels_by_gender" and instance == "gay":
                    if item == "men":
                        marker_color = colours["mlm"]
                    if item == "women":
                        marker_color = colours["wlw"]
                else:
                    marker_color = colours[instance]

                y = [current_num]

                if data_case == "orientation_alignment":
                    text = instance[6:]
                else: text = instance

                text += f" ({int(round(current_num/total_num, 2) * 100)}%)"

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
    visualises
    - numbers of fandoms with no, only or over half of ships of each gender combo type 
    (data_case="no_half_only", ranking="total")
    - top 3 fandoms for ships of each gender combo type, with medal colours (gold, silver, bronze)
    (data_case="top_fandoms", ranking="total")

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
    visualises 
    - top fandoms for most racial groups represented (data_case="racial_diversity", ranking="total")
    - average amount of ships of each gender combo type in a fandom 
    (data_case="average_ship_combo", ranking="total")
    - ships with and without white and east asian characters 
    (data_case="non_white_ships", ranking="total")
    - characters' genders excluding "F" and "M" (data_case="minority_genders", ranking="total")
    
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
        text = pd.Series(input_item.index).mask(
            cond=input_item.index == 'Genshin Impact | 原神', 
            other="Genshin"
        )
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
        colour_guide = None

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
            labels=labels,
            color=colour_guide,
            color_discrete_sequence=colours,
        )
    else: # otherwise just use the automatic dataframe one
        simple_bars = px.bar(
            data_frame=df,
            title=title,
            text=text,
            labels=labels,
            color=colour_guide,
            color_discrete_sequence=colours,
        )

    simple_bars.update_layout( # hiding legend
        showlegend=show_legend,
    )
    
    if not x_axis_visible: # if we want to hide the x_axis
        simple_bars.update_xaxes(
            visible=x_axis_visible
        )

    # replacing colours where relevant
    if traces_marker_colour: # if it will all be one colour
        simple_bars.update_traces(
            marker_color=traces_marker_colour
        )

    return simple_bars


# could refactor this with non white counts?
def visualise_grouped_bars(input_item:dict, data_case:str, ranking:str, sub_case:str=None):
    """
    visualises
    - gender combos (data_case="gender_combos", ranking="overall"|"annual")
    - minority gender combos (data_case="minority_gender_combos", ranking="overall"|"annual")
    - minority genders (data_case="minority_genders", ranking="overall"|"femslash"|"annual")
    - RPF by gender combo (data_case="rpf", ranking="overall"|"femslash"|"annual")
    - general ships by gender combo (data_case="gen", ranking="overall"|"annual")

    as a grouped bar chart
    """
    #making input case insensitive
    ranking = ranking.lower()
    data_case = data_case.lower()

    suffix = lbls.suffixes[ranking]
    years = list(input_item.keys())

    index_list = []
    for year in years: # getting all index labels
        if data_case in ["rpf", "gen"]:
            item = input_item[year].reset_index()
            item = item.set_index("gender_combo")
        else: item = input_item[year]
        index_list += list(item.index)
    index_list = sorted(list(set(index_list)))

    temp_df = pd.DataFrame(index=index_list)

    # setting values for operation in loop below
    if data_case == "rpf":
        column_name = "rpf_or_fic"
        index_name = "RPF"
    elif data_case == "gen":
        column_name = "fic_type"
        index_name = data_case

    for year in years: # adding a column for each year
        if data_case in ["rpf", "gen"]:
            item = input_item[year].reset_index()
            item = item.set_index(column_name)
            temp_df[year] = item.loc[[index_name]].set_index("gender_combo")
        else:
            temp_df[year] = input_item[year]

    # making sure all index labels are unified
    if data_case == "gender_combos":
        temp_df = rename_gender_combos(temp_df)
        temp_df = sum_label_nums(temp_df, "index")
    
    temp_df = sort_df(temp_df, years[-1]) # sorting values by latest year

    fig = go.Figure()

    # setting title & text size, and removing excluded rows
    if data_case == "gender_combos":
        if sub_case: 
            title = f"Ship gender combinations by year ({sub_case}){suffix}"
        else: 
            title = f"Ship gender combinations by year{suffix}"
        text_size = 8
    elif data_case == "minority_gender_combos":
        title = f"Ship gender combinations excluding M/M and M/F bars by year{suffix}"
        temp_df = temp_df.transpose()
        temp_df.pop("M / M")
        temp_df.pop("M / F")
        temp_df = temp_df.transpose()
        text_size = 15
    elif data_case == "minority_genders":
        title = f"Genders excluding M and F by year{suffix}"
        temp_df = temp_df.transpose()
        if ranking != "femslash":
            title = f"Genders excluding M and F by year{suffix}"
            temp_df.pop("M")
        else:
            title = f"Genders excluding F by year{suffix}"
        temp_df.pop("F")
        temp_df = temp_df.transpose()
        text_size = 15
    elif data_case == "rpf":
        title = f"Real Person Fic ships by gender combo by year{suffix}"
        text_size = 10
    elif data_case == "gen":
        title = f"Non-slash-fic ships by gender combo by year{suffix}"
        text_size = 10

    # setting bg colour
    if data_case in ["minority_gender_combos", "gender_combos", "rpf", "gen"]:
        bg_colour = colour_palettes.bg_colours[ranking][1]
    elif data_case == "minority_genders":
        bg_colour = colour_palettes.bg_colours[ranking][0]

    # dropping empty rows
    temp_df = temp_df.dropna(how="all")

    # setting text labels
    if list(temp_df.index) == ["F / F", "M | F | Other / M | F | Other"]:
        text = ["F / F", "drag queens"]
    else:
        text = temp_df.index
    labels = [str(year) for year in temp_df.columns]

    counter = 0
    for index_label in temp_df.index:
        values = temp_df.loc[index_label]
        if data_case in ["minority_gender_combos", "gender_combos", "rpf", "gen"]:
            colour = colour_palettes.gender_combo_dict[index_label]
        elif data_case == "minority_genders":
            colour = colour_palettes.gender_colours[index_label]

        fig.add_trace(
            go.Bar(
                x=labels,
                y=values,
                text=values,
                textfont={"size": text_size},
                name=text[counter],
                marker_color=colour
            )
        )

        counter += 1

    fig.update_layout(
        barmode='group', 
        title=title,
        plot_bgcolor=bg_colour,
        barcornerradius=5
    )
    
    return fig
