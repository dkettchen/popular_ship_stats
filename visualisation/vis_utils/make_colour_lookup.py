import plotly.express as px
from pandas import DataFrame
from visualisation.input_data_code.make_file_dfs import make_characters_df
from visualisation.vis_utils.df_utils.retrieve_numbers import get_unique_values_list

def make_colour_lookup(input_df:DataFrame): # for fandoms
    """
    takes a df that contains (at least) a "fandom" column

    returns a dictionary with keys of all fandoms from input_df and colour values assigned to each
    """

    all_fandoms = sorted(list(input_df["fandom"].unique()))

    colour_lookup = {}
    colours = px.colors.qualitative.Bold + px.colors.qualitative.Bold + \
        px.colors.qualitative.Bold + px.colors.qualitative.Bold + \
        px.colors.qualitative.Bold + px.colors.qualitative.Bold + \
        px.colors.qualitative.Bold + px.colors.qualitative.Bold + \
        px.colors.qualitative.Bold + px.colors.qualitative.Bold
    
    colour_counter = 0
    for fandom in all_fandoms:
        colour_lookup[fandom] = colours[colour_counter]
        colour_counter += 1
    colour_lookup["Marvel"] = "crimson"
    colour_lookup["DC"] = "dodgerblue"
    colour_lookup["Harry Potter Universe"] = "green"
    colour_lookup["Homestuck"] = "orange"
    colour_lookup["Genshin Impact | 原神"] = "gold"
    colour_lookup["Steven Universe"] = "deeppink"
    colour_lookup["Once Upon a Time"] = "steelblue"
    colour_lookup["Avatar: The last Airbender Universe"] = "tomato"
    colour_lookup["Teen Wolf"] = "darkslateblue"
    colour_lookup["Buffy Universe"] = "goldenrod"
    colour_lookup["RWBY"] = "darkred"
    colour_lookup["Vampire Diaries Universe"] = "darkmagenta"
    colour_lookup["Stranger Things"] = "red"
    colour_lookup["Amphibia"] = "lightgreen"
    colour_lookup["Women's Soccer"] = "black"
    colour_lookup["Doctor Who"] = "blue"
    colour_lookup["Frozen"] = "paleturquoise"
    colour_lookup["Carmilla"] = "red"


    return colour_lookup

def make_colour_lookup_racial_groups():
    character_df = make_characters_df()
    all_racial_groups = sorted(get_unique_values_list(character_df, "race"))

    base_colours = px.colors.qualitative.Pastel + px.colors.qualitative.Prism + \
    px.colors.qualitative.Vivid + px.colors.qualitative.Bold

    look_up = {}

    # making certain groups specific colours
    look_up["White"] = "deepskyblue"
    look_up["White (Multi)"] = "lightseagreen"
    look_up["E Asian"] = "yellowgreen"
    look_up["E Asian (Multi)"] = "mediumseagreen"
    look_up["Latin"] = "hotpink"
    look_up["Latin (Multi)"] = "pink"
    look_up["Af Lat"] = "mediumvioletred"
    look_up["Māori Ind"] = "firebrick"
    look_up["Māori Ind (Multi)"] = "darkred"
    look_up["Black"] = "rebeccapurple"
    look_up["Black (Multi)"] = "mediumpurple"
    look_up["MENA"] = "darkorange"
    look_up["MENA (Multi)"] = "orange"
    look_up["Ambig"] = "gold"
    look_up["N.H."] = "orangered"
    look_up["SE Asian"] = "darkolivegreen"
    look_up["SE Asian (Multi)"] = "olive"
    look_up["S Asian"] = "seagreen"
    look_up["S Asian (Multi)"] = "olivedrab"
    look_up["Central As"] = "darkgreen"
    look_up["Unknown"] = "slategrey"

    counter = 0
    for item in all_racial_groups:
        if item not in look_up.keys():
            look_up[item] = base_colours[counter]
            counter += 1

    return look_up
