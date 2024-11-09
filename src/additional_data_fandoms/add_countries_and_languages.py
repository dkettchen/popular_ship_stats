from copy import deepcopy

american_fandoms = []
british_fandoms = []
japanese_fandoms = []
korean_fandoms = []
chinese_fandoms = []
other_fandoms = {}

def add_countries_of_origin_and_languages(input_list):

    fandom_list = deepcopy(input_list)

    country_languages = {
        "South Korea": "Korean",
        "Japan": "Japanese",
        "France": "French",
        # do china separately cause of mandarin vs cantonese, 
        # although I'm guessing everything will be mandarin

        # look up if thai show is in thai or if language is called smth else??

        # any other countries left??
    }
    
    new_list = []

    for fandom_dict in fandom_list:
        fandom = fandom_dict["fandom"]

        if fandom in american_fandoms:
            fandom_dict["country_of_origin"] = "USA"
        elif fandom in british_fandoms:
            fandom_dict["country_of_origin"] = "UK"
        elif fandom in japanese_fandoms:
            fandom_dict["country_of_origin"] = "Japan"
        elif fandom in korean_fandoms:
            fandom_dict["country_of_origin"] = "South Korea"
        elif fandom in chinese_fandoms:
            fandom_dict["country_of_origin"] = "China"
        elif fandom in other_fandoms:
            fandom_dict["country_of_origin"] = other_fandoms[fandom]
        else: print(fandom)

        if fandom_dict["country_of_origin"] in ["USA", "UK", "Canada", "Australia"]:
            fandom_dict["original_language"] = "English"
        if fandom_dict["country_of_origin"] in country_languages:
            fandom_dict["original_language"] = country_languages[fandom_dict["country_of_origin"]]
        else: print(fandom_dict["country_of_origin"])

        new_list.append(fandom_dict)
    
    return new_list