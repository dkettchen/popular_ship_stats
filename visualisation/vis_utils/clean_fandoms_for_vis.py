from visualisation.vis_utils.remove_translation import remove_translation

def iterate_cases_and_replace(input_string:str, input_list:list, replacement_list:list):
    """
    iterates over list of options, 
    if string contains or is one of the options, it returns the replacement, 
    otherwise it returns the original string
    """
    for index in range(len(input_list)):
        item = input_list[index]
        if item in input_string or item == input_string:
            return replacement_list[index]

    return input_string

def clean_fandoms(input_list_or_array):
    """
    takes a series, list, or other array thingy containing fandom names

    it removes the translations, shortens relevant fandoms to recognisable short forms, 
    and removes the "Universe" suffix from anything other than Steven Universe for easier visualisation

    returns the updated list of fandoms 
    """
    fandoms = []

    lookup_dict = { # and then we can simply add to here if we want to add any others! :) 
        "Madoka": "Madoka",
        "Sailor Moon": "Sailor Moon",
        "The Untamed": "The Untamed",
        "Vocaloid": "Vocaloid",
        "Miraculous: Tales of Ladybug & Cat Noir": "Miraculous",
        "Gundam": "Gundam",
        "Hunger Games": "Hunger Games",
        "BTS": "BTS",
        "She-Ra": "She-Ra",
        "The Locked Tomb": "The Locked Tomb",
        "TXT": "TXT",
        "Sabrina": "Sabrina",
        "My Hero Academia": "MHA",
        "JoJo's Bizarre Adventure": "JJBA",
        "Game of Thrones": "GoT",
        "Lord of the Rings": "LotR",
        "Avatar": "ATLA",
        "Teenage Mutant Ninja Turtles": "TMNT",
        "American Horror Story": "AHS",
        "Word of Honor": "Word of Honor",
    }

    for fandom in list(input_list_or_array):
        if " | " in fandom: # remove translation first
            new_fandom = remove_translation(fandom)
        elif "Universe" in fandom and fandom != "Steven Universe": # remove universe
            new_fandom = fandom[:-9]
        else: new_fandom = fandom

        # then we replace relevant fandoms with short forms
        new_fandom = iterate_cases_and_replace(
            new_fandom, 
            list(lookup_dict.keys()), 
            list(lookup_dict.values())
        )
        
        fandoms.append(new_fandom)

    return fandoms
