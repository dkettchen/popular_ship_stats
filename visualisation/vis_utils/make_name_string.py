def make_name_string(names_list):
    """
    takes a list of names

    if there's more than one name, concatenates them with "&"s and adds a "(tied)" to the end 
    and returns the resulting string

    if there's only one name it returns that name string
    """

    names_str = names_list[0] # getting first name

    if len(names_list) > 1: # if there are more names
        for name in names_list[1:]:
            names_str += " & " + name # add every name
        names_str += " (tied)" # then tag them as tied

    return names_str