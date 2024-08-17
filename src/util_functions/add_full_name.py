from copy import deepcopy

def add_full_name(name_dict):
    """
    Takes a name dictionary with (at least) the following keys: ["given_name", 
    "middle_name", "maiden_name", "surname", "alias", "nickname", "title (prefix)", 
    "title (suffix)", "name_order", "full_name", "fandom] which should be set to None 
    or a string value.
    
    Returns that a new version of that same dictionary with a full name string 
    assembled from the remaining name part keys where present.
    Any keys not mentionned above will remain unchanged, nicknames will have single 
    quotes removed where present, and any prior full_name value will be overwritten.
    """

    copy_dict = deepcopy(name_dict)

    given_name = copy_dict["given_name"]
    middle_name = copy_dict["middle_name"]
    maiden_name = copy_dict["maiden_name"]
    surname = copy_dict["surname"]
    alias = copy_dict["alias"]
    nickname = copy_dict["nickname"]
    title_prefix = copy_dict["title (prefix)"]
    title_suffix = copy_dict["title (suffix)"]
    order = copy_dict["name_order"]
    fandom = copy_dict["fandom"]

    full_name = ""

    if nickname and nickname[0] == "'":
        nickname = nickname[1:-1] # removing quotes for consistency
        copy_dict["nickname"] = nickname

    if title_prefix:
        full_name += " " + title_prefix
    if order == "E":
        if surname: 
            full_name += " " + surname
        if middle_name:
            full_name += " " + middle_name
        if nickname:
            full_name += " " + "'" + nickname + "'"
        if given_name:
            full_name += " " + given_name
    else: # if W or no order indicated
        if given_name:
            full_name += " " + given_name
        if middle_name:
            full_name += " " + middle_name
        if nickname:
            full_name += " " + "'" + nickname + "'"
        if surname: 
            full_name += " " + surname
        if maiden_name:
            full_name += ", née " + maiden_name
    if title_suffix:
        full_name += " " + title_suffix
    if alias:
        if (alias in [
            "Player Character", 
            "Root", 
            "Dabi", 
            "Venom (Symbiote)",
            "Q", 
            "America",
            "England", 
            "Lightning",
            "Iron Bull", 
            "TommyInnit",
            "Technoblade",
            "Sapnap",
            "Ranboo",
            "GeorgeNotFound",
            "Ayanga",
            "Wilbur Soot",
        ] and not given_name) or alias == "Doctor":
            full_name += " " + alias
        else: full_name += " | " + alias

    if full_name in [
        " 'Spock'", 
        " 'Vaggie'",
        " 'Spike'",
    ]: # removing quotes
        full_name = full_name[1:-1]
    elif full_name == " Ben Solo Ren | Kylo":
        full_name = " Ben Solo | Kylo Ren"
    elif full_name == " Darth Anakin Skywalker | Vader":
        full_name = " Anakin Skywalker | Darth Vader"
    elif full_name == " Captain Killian Jones | Hook":
        full_name = " Killian Jones | Captain Hook"
    elif "One Piece" in fandom:
        if order == "E":
            full_name = f" {surname} {given_name}"
        else:
            full_name = f" {given_name} {surname}"
        if alias:
            full_name += f" | {alias} {given_name}"

    full_name = full_name[1:] # removing leading white space

    copy_dict["full_name"] = full_name

    return copy_dict

