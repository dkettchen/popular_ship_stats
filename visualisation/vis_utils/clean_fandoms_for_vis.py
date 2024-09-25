from visualisation.vis_utils.remove_translation import remove_translation

def clean_fandoms(input_list_or_array):
    """
    takes a series, list, or other array thingy containing fandom names

    it removes the translations, shortens "ATLA", "BTS", "GoT", "MHA", "Madoka", "Sailor Moon", "She-Ra", 
    and "The Locked Tomb", and removes the "Universe" suffix from anything other than Steven Universe 
    for easier visualisation

    returns the updated list of fandoms 
    """
    fandoms = []

    for fandom in list(input_list_or_array):
        if " | " in fandom:
            new_fandom = remove_translation(fandom)
            if "Madoka" in new_fandom:
                new_fandom = "Madoka"
            elif new_fandom == "My Hero Academia":
                new_fandom = "MHA"
            elif "Sailor Moon" in new_fandom:
                new_fandom = "Sailor Moon"
        elif "BTS" in fandom:
            new_fandom = "BTS"
        elif "Universe" in fandom and fandom != "Steven Universe":
            new_fandom = fandom[:-9]
            if "Avatar" in new_fandom:
                new_fandom = "ATLA"
            elif "Game of Thrones" in new_fandom:
                new_fandom = "GoT"
        elif "She-Ra" in fandom:
            new_fandom = "She-Ra"
        elif "The Locked Tomb" in fandom:
            new_fandom = "The Locked Tomb"
        else: new_fandom = fandom
        fandoms.append(new_fandom)

    return fandoms

