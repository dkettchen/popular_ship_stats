from visualisation.vis_utils.read_csv_to_df import df_from_csv
from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from re import split


def total_ships_df(ships_df): # util
    """
    takes read-in dataframe from ships file

    returns a dataframe with the total number of ships in the file
    """
    total_ships = ships_df.copy().get(["slash_ship"]).count().rename(
        index={"slash_ship":"total_num_of_ships"}
    )

    return total_ships


def total_gender_combo_percent_df(ships_df):
    """
    takes read-in dataframe from ships file

    returns a dataframe with the total numbers of ships of each gender combo
    """
    total_gender_percentages = ships_df.copy().get(
        ["slash_ship","gender_combo"]
    ).groupby("gender_combo").count().rename(index={
        "F / M": "M / F",
        "Ambig / M": "M / Ambig",
        "Ambig / F": "F / Ambig",
        "M | Other / M": "M / M | Other"
    })
    total_gender_percentages = total_gender_percentages.groupby(
        total_gender_percentages.index
    ).aggregate("sum").rename(columns={"slash_ship": "count"}).sort_values(by="count")

    return total_gender_percentages

def visualise_gender_combo_total(total_gender_percentages):
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

def visualise_gender_combo_minorities(total_gender_percentages):
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


def get_ships_per_fandom(ships_df): # util
    """
    takes read-in dataframe from ships file

    returns a dataframe with only the fandom, slash_ship, gender_combo, and race_combo columns
    """
    ships_per_fandom = ships_df.copy().get(["fandom", "slash_ship", "gender_combo", "race_combo"])
    return ships_per_fandom

def make_ships_per_fandom_df(ships_df): # util
    """
    takes read-in dataframe from ships file

    returns a dataframe with the number of ships per fandom
    """
    ships_per_fandom = get_ships_per_fandom(ships_df)
    ships_per_fandom = ships_per_fandom.join(
        other=ships_per_fandom.copy().groupby("fandom").count()["slash_ship"], 
        on=ships_per_fandom.fandom, 
        how="inner", 
        rsuffix="_count"
    ).rename(
        columns={"slash_ship_count": "total_ships"}
    )
    ships_per_fandom.pop("key_0")

    return ships_per_fandom


def fandom_market_share_srs(ships_df):
    """
    takes read-in dataframe from ships file

    returns a series with the fandoms that account for more than 1% of total ships
    """
    ships_per_fandom = get_ships_per_fandom(ships_df)
    total_ships = total_ships_df(ships_df)

    fandom_market_share = ships_per_fandom.copy().groupby("fandom").count()
    fandom_market_share = fandom_market_share.where(
        (fandom_market_share["slash_ship"] / total_ships["total_num_of_ships"]) >= 0.01
    )["slash_ship"].sort_values(ascending=False)

    values = fandom_market_share.values
    fandoms = clean_fandoms(fandom_market_share.index)

    english_titles_market_share = pd.Series(data=values, index=fandoms)

    return english_titles_market_share

def visualise_fandom_market_share(fandom_market_share):
    """
    takes output series from fandom_market_share_srs

    returns a pie chart of all fandoms that account for more than 1% of total fandoms
    """
    market_share_fig = go.Figure(
        data=[
            go.Pie(
                labels=fandom_market_share.index,
                values=fandom_market_share.values,
                textinfo="label",
                #textposition="outside",
                #insidetextorientation="radial",
                automargin=False,
                marker=dict(
                    colors=[
                        "crimson", "red", "green", "dodgerblue", "orange", "gold"
                    ] + px.colors.qualitative.Bold + px.colors.qualitative.Bold
                )
            )
        ]
    )
    market_share_fig.update_layout(
        title="Fandoms accounting for more than 1% of ships (AO3 2013-2023)",
        showlegend=False,
    )

    return market_share_fig


def ship_per_fandom_by_type_df(ships_df):
    """
    takes read-in dataframe from ships file

    returns a dataframe with various stats on ships of different types by fandom
    (total number per fandom, % of fandom's ships, etc)
    """
    ships_per_fandom = make_ships_per_fandom_df(ships_df)
    ships_per_fandom_by_type = ships_per_fandom.copy().get(
        ["fandom", "total_ships", "gender_combo"]
    )

    # how many ships of type by fandom
    ships_per_fandom_by_type["wlw_ships"] = ships_per_fandom_by_type.gender_combo.where(
        (ships_per_fandom_by_type.gender_combo == "F / F"
        ) | (ships_per_fandom_by_type.gender_combo == "F | Other / F | Other"
        ) | (ships_per_fandom_by_type.gender_combo == "F / F | Other")
    )
    ships_per_fandom_by_type["mlm_ships"] = ships_per_fandom_by_type.gender_combo.where(
        (ships_per_fandom_by_type.gender_combo == "M / M"
        ) | (ships_per_fandom_by_type.gender_combo == "M | Other / M / M"
        ) | (ships_per_fandom_by_type.gender_combo == "M / M | Other"
        ) | (ships_per_fandom_by_type.gender_combo == "M | Other / M")
    )
    ships_per_fandom_by_type["het_ships"] = ships_per_fandom_by_type.gender_combo.where(
        (ships_per_fandom_by_type.gender_combo == "F / M"
        ) | (ships_per_fandom_by_type.gender_combo == "M / F")
    )
    ships_per_fandom_by_type.pop("gender_combo")
    ships_per_fandom_by_type = ships_per_fandom_by_type.groupby(["fandom"]).count() 
        # this makes fandom the index/columns -> no longer counted for length

    for ship_type in ["mlm", "wlw", "het"]:
        # percent of total that is
        ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] = (
            ships_per_fandom_by_type[f"{ship_type}_ships"] / ships_per_fandom_by_type["total_ships"] * 100
        ).round(2)

        # diff conditions it fulfills
        ships_per_fandom_by_type[f"no_{ship_type}"] = ships_per_fandom_by_type["total_ships"].where(
            ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] == 0
        )
        ships_per_fandom_by_type[f"all_{ship_type}"] = ships_per_fandom_by_type["total_ships"].where(
            ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] == 100
        )
        ships_per_fandom_by_type[f"more_than_50%_{ship_type}"] = ships_per_fandom_by_type[f"%_of_{ship_type}_ships"].where(
            (ships_per_fandom_by_type[f"{ship_type}_ships"] > 1
            ) & (ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] < 100
            ) & (ships_per_fandom_by_type[f"%_of_{ship_type}_ships"] >= 50)
        )

    return ships_per_fandom_by_type


def total_gender_combos_srs(ships_per_fandom_by_type):
    """
    takes output dataframe from ship_per_fandom_by_type_df

    returns a series with how many fandoms contained no, only, or over 50% of each ship type
    """
    total_gender_combos_dict = {
        "no_mlm_ship_fandoms": ships_per_fandom_by_type["no_mlm"].count(),
        "more_than_50%_mlm": ships_per_fandom_by_type["more_than_50%_mlm"].count(),
        "only_mlm_ship_fandoms": ships_per_fandom_by_type["all_mlm"].count(),
        "no_wlw_ship_fandoms": ships_per_fandom_by_type["no_wlw"].count(),
        "more_than_50%_wlw": ships_per_fandom_by_type["more_than_50%_wlw"].count(),
        "only_wlw_ship_fandoms": ships_per_fandom_by_type["all_wlw"].count(),
        "no_het_ship_fandoms": ships_per_fandom_by_type["no_het"].count(),
        "more_than_50%_het": ships_per_fandom_by_type["more_than_50%_het"].count(),
        "only_het_ship_fandoms": ships_per_fandom_by_type["all_het"].count(),
    }
    total_gender_combos_series = pd.Series(total_gender_combos_dict)

    return total_gender_combos_series

def visualise_no_half_only(total_gender_combos_series):
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


def highest_of_this_type_df(ships_per_fandom_by_type):
    """
    takes output dataframe from ship_per_fandom_by_type_df

    returns a dataframe with the top 3 fandoms for number of ships of each type
    """
    most_wlw = ships_per_fandom_by_type["wlw_ships"].where(ships_per_fandom_by_type["wlw_ships"] > 1).sort_values(ascending=False).dropna()
    most_mlm = ships_per_fandom_by_type["mlm_ships"].where(ships_per_fandom_by_type["mlm_ships"] > 1).sort_values(ascending=False).dropna()
    most_het = ships_per_fandom_by_type["het_ships"].where(ships_per_fandom_by_type["het_ships"] > 1).sort_values(ascending=False).dropna()

    highest_of_type = {
        "highest num of mlm ships": [most_mlm.head(3).values[num] for num in [0,1,2]],
        "highest num of wlw ships": [most_wlw.head(3).values[num] for num in [0,1,2]],
        "highest num of het ships": [most_het.head(3).values[num] for num in [0,1,2]],
        "highest mlm fandom": [list(most_mlm.head(3).index)[num] for num in [0,1,2]],
        "highest wlw fandom": [list(most_wlw.head(3).index)[num] for num in [0,1,2]],
        "highest het fandom": [list(most_het.head(3).index)[num] for num in [0,1,2]],
    }
    highest_index = ["1st", "2nd", "3rd"]

    highest_of_type_df = pd.DataFrame(
        highest_of_type, 
        index=highest_index
    )

    return highest_of_type_df

def visualise_top_3_per_fandom_df(highest_of_type_df):
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


def average_gender_combo_srs(ships_per_fandom_by_type):
    """
    takes output dataframe from ship_per_fandom_by_type_df

    returns a series with the average number of ships of each gender combo in a fandom
    """
    average_gender_combo_dict = {
        "ships": ships_per_fandom_by_type["total_ships"].mean().round(2),
        "mlm": ships_per_fandom_by_type["mlm_ships"].mean().round(2),
        "wlw": ships_per_fandom_by_type["wlw_ships"].mean().round(2),
        "hets": ships_per_fandom_by_type["het_ships"].mean().round(2)
    }
    average_gender_combo_per_fandom_series = pd.Series(average_gender_combo_dict)

    return average_gender_combo_per_fandom_series

def visualise_average_ship_combos_per_fandom(average_gender_combo_per_fandom_series):
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


def total_race_combo_df(ships_df):
    """
    takes read-in dataframe from ships file

    returns a dataframe with the total numbers of ships of each race combo
    """
    total_race_combo_counts = ships_df.get(["slash_ship","race_combo"])

    unique_combos = sorted(list(set(total_race_combo_counts.race_combo)))
    rename_dict = {}
    for combo in unique_combos:
        sorted_split_version = sorted(split(r"\s\/\s", combo))
        reconcat_version = sorted_split_version[0]
        for item in sorted_split_version[1:]:
            reconcat_version += " / " + item
        if reconcat_version != combo:
            rename_dict[combo] = reconcat_version

    total_race_combo_counts = total_race_combo_counts.groupby("race_combo").count().rename(
        index=rename_dict,
        columns={"slash_ship": "count"}
    )
    total_race_combo_counts = total_race_combo_counts.groupby(
        total_race_combo_counts.index
    ).aggregate("sum").sort_values(
        by="count", ascending=False
    )

    return total_race_combo_counts


def interracial_srs(total_race_combo_counts):
    """
    takes output dataframe from total_race_combo_df

    returns a series with the total number of interracial, non-interracial and ambiguous ships
    """
    interracial_ships = total_race_combo_counts.copy()
    interracial_ships["is_interracial_pairing"] = interracial_ships.index.str.contains("/")
    interracial_ships["is_ambig"] = interracial_ships.index.str.contains("Ambig")
    interracial_ships_counts = pd.Series({
        "same_race_pairings": interracial_ships["count"].where(
            (interracial_ships.is_ambig == False) & (interracial_ships.is_interracial_pairing == False)
        ).aggregate("sum"),
        "interracial_pairings": interracial_ships["count"].where(
            (interracial_ships.is_ambig == False) & (interracial_ships.is_interracial_pairing == True)
        ).aggregate("sum"), 
        "ambiguous_pairings": interracial_ships["count"].where(
            interracial_ships.is_ambig == True
        ).aggregate("sum"), 
    })

    return interracial_ships_counts

def visualise_interracial_ships(interracial_ships_counts):
    """
    takes output series from interracial_srs

    returns a pie chart visualising the ratio of interracial, non-interracial and ambiguous ships
    """
    interracial_labels = ["non-interracial", "interracial", "ambiguous"]
    interracial_values = interracial_ships_counts.values

    interracial_pie = go.Figure(
        data=[
            go.Pie(
                labels=interracial_labels,
                values=interracial_values,
                textinfo="label+percent",
                textposition="outside",
                marker=dict(
                    colors=px.colors.qualitative.Prism
                )
            )
        ]
    )
    interracial_pie.update_layout(
        title="Interracial vs other ships (AO3 2013-2023)",
        showlegend=False, # if you want it to not show the legend
    )

    return interracial_pie


def non_white_ships_srs(total_race_combo_counts): 
    """
    takes output dataframe from total_race_combo_df

    returns a series with the total number of ships that involve white ppl, involve east asian ppl, 
    do not involve white ppl, and involve neither white nor east asian people
    """
    # this one's the big oof
    non_white_ships = total_race_combo_counts.copy()
    non_white_ships["contains_white_person"] = non_white_ships.index.str.contains("White|Eu Ind")
    non_white_ships["contains_e_asian_person"] = non_white_ships.index.str.contains("E Asian")
    non_white_ships["contains_ambig_person"] = non_white_ships.index.str.contains("Ambig")
    non_white_ships["contains_non_human"] = non_white_ships.index.str.contains("N.H.")
    non_white_ships["contains_unknown"] = non_white_ships.index.str.contains("Unknown")

    non_white_ships_counts = pd.Series(
        {
            "pairings_with_white_people": non_white_ships["count"].where(
                non_white_ships.contains_white_person == True
            ).aggregate("sum"), 
            "pairings_with_east_asian_people": non_white_ships["count"].where(
                non_white_ships.contains_e_asian_person == True
            ).aggregate("sum"), 
            "non_white_pairings": non_white_ships["count"].where(
                (non_white_ships.contains_ambig_person == False) & (
                non_white_ships.contains_non_human == False) & (
                non_white_ships.contains_unknown == False) & (
                non_white_ships.contains_white_person == False)
            ).aggregate("sum"),
            "non_white_or_east_asian_pairings": non_white_ships["count"].where(
                (non_white_ships.contains_ambig_person == False) & (
                non_white_ships.contains_non_human == False) & (
                non_white_ships.contains_unknown == False) & (
                non_white_ships.contains_white_person == False) & (
                non_white_ships.contains_e_asian_person == False)
            ).aggregate("sum"),
        }
    )

    return non_white_ships_counts

def visualise_non_white_ships(non_white_ships_counts):
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


def rpf_fic_df(ships_df):
    """
    takes read-in dataframe from ships file

    returns a dataframe with the number of rpf and non-rpf ships
    """
    rpf_vs_fic_df = ships_df.get(
        ["slash_ship", "rpf_or_fic"]
    ).groupby("rpf_or_fic").count().rename(columns={"slash_ship": "count"})

    return rpf_vs_fic_df

def visualise_rpf_fic(rpf_vs_fic_df):
    """
    takes output dataframe from rpf_fic_df

    returns a pie chart showing the ratio of rpf to non-rpf ships
    """
    rpf_pie = go.Figure(
        data=[
            go.Pie(
                labels=rpf_vs_fic_df["count"].index,
                values=rpf_vs_fic_df["count"].values,
                textinfo="label+percent",
                textposition="inside",
                marker=dict(
                    colors=["deeppink", "purple", ]
                )
            )
        ]
    )
    rpf_pie.update_layout(
        title="Real Person Fic vs Fictional Ships (AO3 2013-2023)",
        showlegend=False, # if you want it to not show the legend
    )
    return rpf_pie


if __name__ == "__main__":

    # read from ships file make a df
    ships_df = df_from_csv("data/fifth_clean_up_data/stage_5_ships.csv")

    total_gender_percentages = total_gender_combo_percent_df(ships_df)
    total_gender_percent_fig = visualise_gender_combo_total(total_gender_percentages)
    total_gender_percent_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_ranked_ships_gender_combos_2013_2023.png", 
        width=600, 
        height=400, 
        scale=2
    )

    minority_gender_combos_fig = visualise_gender_combo_minorities(total_gender_percentages)
    minority_gender_combos_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_ranked_ships_minority_gender_combos_2013_2023.png", 
        width=1300, 
        height=600, 
        scale=2
    )

    fandom_market_share = fandom_market_share_srs(ships_df)
    fandom_market_share_fig = visualise_fandom_market_share(fandom_market_share)
    fandom_market_share_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/all_ao3_ranked_ships_fandom_market_share_2013_2023.png", 
        width=800, 
        height=650, 
        scale=2
    )

    ships_per_fandom_by_type = ship_per_fandom_by_type_df(ships_df)

    total_gender_combos_series = total_gender_combos_srs(ships_per_fandom_by_type)
    total_gender_combos_fig = visualise_no_half_only(total_gender_combos_series)
    total_gender_combos_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_with_no_over_half_only_by_ship_type_2013_2023.png", 
        width=1200, 
        height=600, 
        scale=2
    )

    highest_of_type_df = highest_of_this_type_df(ships_per_fandom_by_type)
    highest_of_type_fig = visualise_top_3_per_fandom_df(highest_of_type_df)
    highest_of_type_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_top_3_by_ship_type_no_2013_2023.png", 
        width=1200, 
        height=600, 
        scale=2
    )

    average_gender_combo_per_fandom_series = average_gender_combo_srs(ships_per_fandom_by_type)
    average_gender_combo_fig = visualise_average_ship_combos_per_fandom(average_gender_combo_per_fandom_series)
    average_gender_combo_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_average_no_of_ships_by_type_2013_2023.png", 
        width=800, 
        height=400, 
        scale=2
    )

    total_race_combo_counts = total_race_combo_df(ships_df)

    interracial_ships_counts = interracial_srs(total_race_combo_counts)
    interracial_fig = visualise_interracial_ships(interracial_ships_counts)
    interracial_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_ranked_ships_interracial_percent_2013_2023.png", 
        width=800, 
        height=400, 
        scale=2
    )

    non_white_ships_counts = non_white_ships_srs(total_race_combo_counts)
    non_white_fig = visualise_non_white_ships(non_white_ships_counts)
    non_white_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_ranked_ships_non_white_ships_2013_2023.png", 
        width=800, 
        height=500, 
        scale=2
    )

    rpf_vs_fic_df = rpf_fic_df(ships_df)
    rpf_fig = visualise_rpf_fic(rpf_vs_fic_df)
    rpf_fig.write_image(
        "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/all_ao3_ranked_ships_rpf_vs_fic_2013_2023.png", 
        width=600, 
        height=400, 
        scale=2
    )

