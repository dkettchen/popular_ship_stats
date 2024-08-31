from src.util_functions.make_ship_tag import make_ship_tag

def make_ranking_table(list_of_dicts, data_set):
    """
    takes a list of dicts with main set data and the tag of the data set

    returns a nested list the following columns: ["rank_id","data_set","rank_no","change",
    "ship","members_num","fic_type","new_works","total_works","old_fandom","release_date"]
    Any other columns have been dropped.

    rank_id contains the data_set name and a serial primary key number.
    rank_no has been reduced to its integer value.
    change has been reduced back to a single value (number (positive or negative), or "new")
    ship has been turned into a string of the names,
    ordered alphabetically and separated by " & "/" x " depending on fic type.
    members_num contains the number of characters in the ship.
    fic_type now only differentiates between "gen" and "slash".
    The remaining keys remain the same.
    """

    columns = [
        "rank_id",
        "data_set",
        "rank_no",
        "change",
        "ship",
        "members_num",
        "fic_type",
        "new_works",
        "total_works",
        "old_fandom",
        "release_date",
    ]

    new_list = [columns]
    row_counter = 0

    for row in list_of_dicts:
        rank_no = row["Rank"][0] # we're just dropping the = where present
        new_works = row["New Works"]
        total_works = row["Total Works"]
        old_fandom = row["Old Fandom"]
        release_date = row["Release Date"]
        members_num = len(row["Relationship"])
        fic_type = None
        change = None
        ship = None
        rank_id = None

        if members_num > 4:
            print(data_set, row)

        # tagging fic type
        if row["Type"] == "Gen":
            fic_type = "gen"
        else: 
            fic_type = "slash"

        # reformatting change
        if row["Change"][0] == "New":
            change = "new"
        elif type(row["Change"][1]) == int:
            if row["Change"][0] == "-":
                change = 0 - row["Change"][1]
            else:
                change = row["Change"][1]

        # creating ship tag
        ship = make_ship_tag(row["Relationship"], fic_type)

        # make key and increment counter
        rank_id = f"{data_set}-{row_counter}"
        row_counter += 1

        row_list = [
            rank_id,
            data_set,
            rank_no,
            change,
            ship,
            members_num,
            fic_type,
            new_works,
            total_works,
            old_fandom,
            release_date,
        ]

        new_list.append(row_list)

    return new_list