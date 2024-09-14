from visualisation.vis_utils.read_csv_to_df import df_from_csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#from plotly.subplots import make_subplots

# read from char file make a df
characters_df = df_from_csv("data/fifth_clean_up_data/stage_5_characters.csv")
# characters_df.columns

def total_chars_df(characters_df):
    total_chars = characters_df.get(
        ["full_name"]
    ).count().rename(
        index={"full_name":"total_num_of_characters"}
    )
    # print(total_chars)
    return total_chars


def all_characters_gender_df(characters_df):
    # all-characters gender percentages (all time, entire set)
    total_gender_percentages = characters_df.get(
        ["full_name","gender"]
    ).groupby("gender").count().rename(
        columns={"full_name": "count"}
    )
    total_gender_percentages.index = pd.Categorical( # to set a custom order!
        total_gender_percentages.index, 
        [
            "M | Other",
            "F | Other",
            "F",
            "Other",
            "M | F | Other",
            "Ambig",
            "M",
        ]
    )
    total_gender_percentages = total_gender_percentages.sort_index()
    # print(total_gender_percentages) # TO VISUALISE
    return total_gender_percentages

def visualise_gender_totals(total_gender_percentages):
    # visualising gender totals
    gender_distr_pie = go.Figure(
        data=[
            go.Pie(
                labels=total_gender_percentages.index,
                values=total_gender_percentages["count"],
                textinfo="label+value",
                textposition="outside",
                sort=False,
                marker=dict(
                    colors=[
                        "darkturquoise",
                        "red",
                        "hotpink",
                        "yellow",
                        "gold",
                        "green",
                        "cornflowerblue",
                    ]
                )
            )
        ]
    )
    gender_distr_pie.update_layout(
        title="Characters' gender distribution (AO3 2013-2023)",
        #showlegend=False, # if you want it to not show the legend
    )
    # gender_distr_pie.show()
    return gender_distr_pie


def average_gender_per_fandom_df(characters_df):
    # how many male vs female vs other characters a fandom has on average
    average_gender_per_fandom = characters_df.copy().get(
        ["full_name","fandom","gender"]
    )
    average_gender_per_fandom.insert(loc=3, column="women", 
        value=(average_gender_per_fandom.gender.where(
            cond=(characters_df.gender == "F") | (characters_df.gender == "F | Other"),
        ))
    )
    average_gender_per_fandom.insert(loc=3, column="men", 
        value=(average_gender_per_fandom.gender.where(
            cond=(characters_df.gender == "M") | (characters_df.gender == "M | Other") ,
        )) 
    )
    average_gender_per_fandom.insert(loc=5, column="characters of other or ambiguous gender", 
        value=(average_gender_per_fandom.gender.where(
            (characters_df.gender != "F") & (characters_df.gender != "F | Other") & (characters_df.gender != "M") & (characters_df.gender != "M | Other")
        ))
    )
    average_gender_per_fandom = average_gender_per_fandom.groupby(by="fandom", dropna=False).count().get(
        ["men","women","characters of other or ambiguous gender"]
    ).mean(0).round(2)
    # print(average_gender_per_fandom) # TO VISUALISE
    return average_gender_per_fandom


def all_characters_racial_groups_df(characters_df):
    # all-characters race percentages (all time, entire set)
    total_race_percentages = characters_df.get(
        ["full_name","race"]
    ).groupby("race").count().rename(
        columns={"full_name": "count"}
    ).sort_values(by="count", ascending=False) 
    # print(total_race_percentages.sort_index().head(10)) # TO VISUALISE
    return total_race_percentages

def visualise_racial_group_totals(total_race_percentages):
    # pie chart
    all_race_percent_pie = go.Figure(
        data=[
            go.Pie(
                labels=total_race_percentages.index,
                values=total_race_percentages["count"],
                textinfo="label",
                insidetextorientation="horizontal",
                automargin=False,
                # marker=dict(
                    # colors=template colours or builtin colour sequence
                # )
            )
        ]
    )
    all_race_percent_pie.update_traces(textposition='inside')
    all_race_percent_pie.update_layout(
        title="Characters' racial groups distribution (AO3 2013-2023)",
        uniformtext_minsize=10, 
        uniformtext_mode='hide'
    )

    # all_race_percent_pie.show()
    return all_race_percent_pie


def make_all_groupings_dict():
    # making all groupings dict
    all_groupings = {
        "north, west, middle and eastern europe": [
            'White', 
            'White (Multi)',
            'Romani', 
            'Eu Ind (Multi)', 
        ],
        "black (incl afro-latin)": [
            'Black', 
            'Black (Multi)',
            'Af Lat', 
        ],
        "south europe and (rest of) latin": [
            'Latin',
            'Latin (Multi)', 
            'SE Eu', 
            'SE Eu (Multi)', 
        ],
        "middle-east and north-africa": [
            'MENA', 
            'MENA (Multi)', 
        ],
        "east asia": [
            'E Asian', 
            'E Asian (Multi)', 
        ],
        "(rest of) asia": [
            'S Asian', 
            'S Asian (Multi)',
            'SE Asian', 
            'SE Asian (Multi)', 
            'As Ind',
            'As Ind / S Asian (Multi)', 
            'Asian (Multi)', 
            'Central As', 
        ],
        "american & polynesian indigenous": [
            'Am Ind', 
            'Am Ind / E Asian (Multi)', 
            'Māori Ind',
            'Māori Ind (Multi)', 
        ],
        "other": {
            'Ambig': "ambiguous or differing casting", 
            'N.H.': "non-human", 
            'Unknown': "unknown",
        },
    }
    return all_groupings

def visualise_racial_minority_totals(total_race_percentages, all_groupings):
    # bar stack
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
    # other_racial_group_stacks.show()
    return other_racial_group_stacks


def make_racial_diversity_df(characters_df):
    # find fandoms with lowest (aka no) racial diversity
    racial_div_by_fandom = characters_df.copy().get(
        ["full_name","fandom","race"]
    ).groupby(
        ["fandom", "race"]
    ).count().rename(columns={"full_name": "count"})
    return racial_div_by_fandom


def plural_vs_monoracial_fandoms_df(characters_df, racial_div_by_fandom):
    plural_vs_monoracial_fandoms = pd.DataFrame([
        characters_df.get(["fandom"]).nunique().rename(index={"fandom":"total_fandoms"})
        # counting all unique fandom names for total
    ])
    plural_vs_monoracial_fandoms.insert(
        loc=1, 
        column="fandoms_with_only_one_racial_group", 
        value=racial_div_by_fandom.where( # there is only one racial group in the fandom
            racial_div_by_fandom.groupby(racial_div_by_fandom.index.droplevel(1)).count() == 1 
        ).count().rename(
            index={"count": "fandoms_with_only_one_racial_group"}
        )["fandoms_with_only_one_racial_group"]
    )
    plural_vs_monoracial_fandoms.insert(
        loc=2, 
        column="fandoms_with_multiple_racial_groups", 
        value=plural_vs_monoracial_fandoms["total_fandoms"] - plural_vs_monoracial_fandoms["fandoms_with_only_one_racial_group"]
        # total minus monoracial fandoms
    )
    plural_vs_monoracial_fandoms = plural_vs_monoracial_fandoms.rename(index={0: "count"})

    #print(plural_vs_monoracial_fandoms) # TO VISUALISE!
    return plural_vs_monoracial_fandoms

def visualise_racial_diversity(plural_vs_monoracial_fandoms):
    # mono vs multi group fandoms pie 
    # (dunno why this didn't wanna work without prep code in same cell smh)

    plural_vs_monoracial_fandoms = plural_vs_monoracial_fandoms.get(
        ["fandoms_with_only_one_racial_group", "fandoms_with_multiple_racial_groups"]
    ).transpose().rename(index={
        "fandoms_with_only_one_racial_group": "one group", 
        "fandoms_with_multiple_racial_groups": "multiple groups"
    })

    number_of_groups_by_fandom = go.Figure(
        data=[
            go.Pie(
                labels=plural_vs_monoracial_fandoms.index,
                values=plural_vs_monoracial_fandoms["count"],
                textinfo="label+percent",
                insidetextorientation="horizontal",
                automargin=False,
                marker=dict(
                    colors=["turquoise", "teal"]
                )
            )
        ]
    )

    number_of_groups_by_fandom.update_layout(
        title="Fandoms with one vs multiple racial groups (AO3 2013-2023)",
        showlegend=False, # if you want it to not show the legend
    )
    # number_of_groups_by_fandom.show()
    return number_of_groups_by_fandom


def highest_racial_diversity_df(racial_div_by_fandom):
    # find fandoms with highest racial diversity (Genshin would likely be in here)
    highest_racial_div = racial_div_by_fandom.where(
        racial_div_by_fandom.groupby(racial_div_by_fandom.index.droplevel(1)).count() > 1
    ).droplevel(1).dropna()
    highest_racial_div = highest_racial_div.groupby(highest_racial_div.index).count().sort_values(
        by="count", ascending=False
    ).head(6) # everything else was under 5
    # print(highest_racial_div) # TO VISUALISE
    return highest_racial_div

def visualise_highest_racial_diversity(highest_racial_div):
    # top fandoms for racial diversity
    basic_template_bar = px.bar(
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
    basic_template_bar.update_layout(
        showlegend=False,
    ).update_xaxes(
        visible=False # to hide bottom axis annotations
    )
    # basic_template_bar.show()


def average_racial_diversity_df(racial_div_by_fandom):
    # how much racial diversity a fandom has on average 

    average_racial_div = racial_div_by_fandom.groupby(
        racial_div_by_fandom.index.droplevel(1)
    ).count().mean(0).round(2).rename(
        index={"count":"average no of racial groups per fandom overall"}
    )
    # print(average_racial_div) # TO VISUALISE
    return average_racial_div


if __name__ == "__main__":
    # read from char file make a df
    characters_df = df_from_csv("data/fifth_clean_up_data/stage_5_characters.csv")
