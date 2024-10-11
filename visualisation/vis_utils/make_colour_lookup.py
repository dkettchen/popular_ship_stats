import plotly.express as px
from pandas import DataFrame

def make_colour_lookup(input_df:DataFrame):
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

