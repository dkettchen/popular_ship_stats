import plotly.express as px
from pandas import DataFrame
from visualisation.input_data_code.make_file_dfs import make_characters_df
from visualisation.vis_utils.df_utils.retrieve_numbers import get_unique_values_list
from visualisation.vis_utils.diagram_utils.colour_palettes import oranges

def make_colour_lookup(input_df:DataFrame): # for fandoms
    """
    takes a df that contains (at least) a "fandom" column

    returns a dictionary with keys of all fandoms from input_df and colour values assigned to each
    """

    all_fandoms = sorted(list(input_df["fandom"].unique()))

    # making base colours
    colours = []
    for _ in range(18):
        colours += px.colors.qualitative.Bold

    # making colour lookup
    colour_lookup = {}

    # assigning base colours
    colour_counter = 0
    for fandom in all_fandoms:
        colour_lookup[fandom] = colours[colour_counter]
        colour_counter += 1
    
    # assigning specific fandom colours
    specified_fandoms_lookup = {
        "Marvel":"crimson",
        "DC":"dodgerblue",
        "Harry Potter Universe":"green",
        "Homestuck":"orange",
        "Genshin Impact | 原神":"gold",
        "Steven Universe":"deeppink",
        "Once Upon a Time":"steelblue",
        "Avatar: The last Airbender Universe":"tomato",
        "Teen Wolf":"darkslateblue",
        "Buffy Universe":"goldenrod",
        "RWBY":"darkred",
        "Vampire Diaries Universe":"darkmagenta",
        "Stranger Things":"red",
        "Amphibia":"lightgreen",
        "Women's Soccer":"black",
        "Doctor Who":"blue",
        "Frozen":"paleturquoise",
        "Carmilla":"red",
        "Bangtan Boys / BTS":"violet",
        "Star Trek":"skyblue",
        "My Hero Academia | 僕のヒーローアカデミア":"seagreen",
        "Supernatural":"chocolate",
        "Haikyuu!! | ハイキュー!!":"darkorange",
        "Star Wars":"black",
        "Youtube":"red",
        "One Direction":"mediumorchid",
        "Good Omens":"lemonchiffon",
        "Voltron":"darkturquoise",
        "Dragon Age":"cadetblue",
        "Yuri!!! on ICE | ユーリ!!! on ICE":"mediumblue",
        "Sherlock":"midnightblue",
        "Stargate":"deepskyblue",
        "Free!":"aqua",
        "Merlin":"firebrick",
        "Lord of the Rings Universe":"olivedrab",
        "The 100":"darkkhaki",
        "Glee":"yellow",
        "Adam Lambert":"silver",
        "A Song of Ice and Fire / Game of Thrones Universe":"dimgrey",
        "Miraculous: Tales of Ladybug & Cat Noir | Miraculous: Les Aventures de Ladybug et Chat Noir":"orangered",
        "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令":"aliceblue",
        "Hamilton": "orange",
        "Undertale": "cornflowerblue",
        "The Owl House": "rosybrown",
        "Overwatch": "gold",
        "Attack on Titan | 進撃の巨人": "chocolate",
        "SK8 the Infinity | SK∞ エスケーエイト": "blueviolet",
    }
    for fandom in specified_fandoms_lookup:
        colour_lookup[fandom] = specified_fandoms_lookup[fandom]

    return colour_lookup

def make_colour_lookup_racial_groups():
    """
    returns a dictionary with keys of all racial groups from the characters file 
    (output from make_characters_df) and colour values assigned to each
    """
    character_df = make_characters_df()
    all_racial_groups = sorted(get_unique_values_list(character_df, "race"))

    look_up = {}

    # making certain groups specific colours
    specific_groups_lookup = {
        "White":"deepskyblue",
        "White (Multi)":"lightseagreen",
        "E Asian":"yellowgreen",
        "E Asian (Multi)":"mediumseagreen",
        "Latin":"hotpink",
        "Latin (Multi)":"pink",
        "Af Lat":"mediumvioletred",
        "Māori Ind":"firebrick",
        "Māori Ind (Multi)":"darkred",
        "Black":"rebeccapurple",
        "Black (Multi)":"mediumpurple",
        "MENA":"darkorange",
        "MENA (Multi)":"orange",
        "Ambig":"gold",
        "N.H.":"orangered",
        "SE Asian":"darkolivegreen",
        "SE Asian (Multi)":"olive",
        "S Asian":"seagreen",
        "S Asian (Multi)":"olivedrab",
        "Central As":"darkgreen",
        "Unknown":"slategrey",
    }
    for group in specific_groups_lookup:
        look_up[group] = specific_groups_lookup[group]

    # make remaining groups base colours
    base_colours = px.colors.qualitative.Pastel + px.colors.qualitative.Prism + \
    px.colors.qualitative.Vivid + px.colors.qualitative.Bold
    counter = 0
    for item in all_racial_groups:
        if item not in look_up.keys():
            look_up[item] = base_colours[counter]
            counter += 1

    return look_up

def make_colour_lookup_inter_and_multi():
    """
    creates a dict of the colours for our interracial and multiracial (chars & involved ships) 
    diagrams

    interracial/multiracial/with_multiracial is orangered,
    ambiguous is gold,
    non-interracial/non-multiracial/without_multiracial is orange
    """

    return {
        "interracial": oranges[0],
        "ambiguous": oranges[1],
        "non-interracial": oranges[2],

        "multiracial": oranges[0],
        "ambiguous": oranges[1],
        "non-multiracial": oranges[2],

        "with_multiracial": oranges[0],
        "ambiguous": oranges[1],
        "without_multiracial": oranges[2],
    }


