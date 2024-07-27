from copy import deepcopy

def unify_column_names(data_list : list):
    """
    takes a nested list of data (taken from data/first_clean_up_data/ao3_* folders)

    returns it with relevant column name strings, if present, changed to match this pattern:
    
    Rank, Change, Relationship, Fandom, New Works, Total Works, Type, Race, Release Date
    """

    new_columns = []
    for column in data_list[0]:
        if column == "Rank" or column == "#":
            column = "Rank"
            new_columns.append(column)
        elif column == "Change" or column == "New":
            column = "Change"
            new_columns.append(column)
        elif column == "Relationship" or column == "Pairing" or column == "Pairing Tag" or column == "Ship":
            column = "Relationship"
            new_columns.append(column)
        #all the fandom columns are already called fandom I believe
        #ditto for New Works I think
        elif column == "Works" or column == "Total Works" or column == "Total" or column == "Fics":
            column = "Total Works"
            new_columns.append(column)
        #I think type, race, and release date are all consistently named already too
        else:
            new_columns.append(column)
    new_list = [new_columns]
    new_list.extend(data_list[1:])

    return new_list