from copy import deepcopy

def make_full_name(char_dict:dict, fandom:str):

    copy_dict = deepcopy(char_dict)

    given_name = copy_dict["given_name"]
    middle_name = copy_dict["middle_name"]
    maiden_name = copy_dict["maiden_name"]
    surname = copy_dict["surname"]
    alias = copy_dict["alias"]
    nickname = copy_dict["nickname"]
    title_prefix = copy_dict["title (prefix)"]
    title_suffix = copy_dict["title (suffix)"]
    order = copy_dict["order"]

    full_name = ""

    if title_prefix:
        full_name += " " + title_prefix

    # adding first name sur/given
    if order == "E":
        if surname:
            full_name += " " + surname
    else:
        if given_name:
            full_name += " " + given_name

    # middle & nickname
    if middle_name:
        full_name += " " + middle_name
    if nickname:
        full_name += " " + "'" + nickname + "'"

    # adding last name given/sur (and maiden name where applicable)
    if order == "E":
        if given_name:
            full_name += " " + given_name
    else:
        if surname:
            full_name += " " + surname
        if maiden_name:
            full_name += ", née " + maiden_name

    if title_suffix:
        full_name += " " + title_suffix

    if alias:
        if not (full_name == "" or alias == "Doctor"): 
            # add pipe except if there's only an alias or it's one of the doctors
            full_name += " |"
        full_name += " " + alias

    # custom cases
    if full_name in [
        " Darth Anakin Skywalker | Vader",
        " Captain Killian Jones | Hook",
    ]:
        full_name = f"{given_name} {surname} | {title_prefix} {alias}"
    elif full_name in [" Ben Solo Ren | Kylo"]:
        full_name = f"{given_name} {surname} | {alias} {title_suffix}"
    elif "One Piece" in fandom:
        if order == "E": # roronoa zoro
            legal_name = f"{surname} {given_name}"
        else: # sanji vinsmoke
            legal_name = f"{given_name} {surname}"
        if alias:
            full_name = f"{legal_name} | {alias} {given_name}"

    full_name = full_name.strip() # removing leading white space if any

    return full_name

