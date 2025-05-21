from re import split
from json import load

books = [
    "Harry Potter", 
    "Les Misérables", 
    "The Hobbit", 
    "Hunger Games Trilogy", 
    "Dragon Age", 
    "Twilight Series",
    "The Lord of the Rings", 
    "A Song of Ice and Fire",
    "Good Omens"
] # the books have authors that are " - " separated so we need to re-assemble those for 2013-2014 data

def split_data(data_list:list[str], year:int, ranking:str):
    """
    takes a list of strings of the read-in txt data, the year and ranking contained in the filepath

    returns a new nested list

    each list item is another list with string values for each column item
    """

    counter = 0
    new_list = []

    for string in data_list:
        # set separator
        if year == 2013 and counter == 0: # 2013 single space separators
            separator = r"\s"
        elif year in [2013, 2014]: # 2013 rows & 2014 " - " separators
            separator = r" - "
        elif year >= 2020 and year <= 2022: # 2020-2022 3 space separators
            separator = r"\s{3}"
        elif year >= 2023: # since 2023 space-tab separators
            separator = r" \t"
        
        # split
        split_list = [item.strip() for item in split(separator, string[:-1])]

        if year in [2013, 2014]: # fixing stuff
            # reappending books
            if year == 2013 or (year == 2014 and ranking == "femslash"):
                book_index = 2
            elif year == 2014 and ranking == "overall":
                book_index = 3
            if split_list[book_index] in books:
                book = split_list[book_index] + " - " + split_list[book_index + 1]
                row_list = split_list[:book_index] + [book] + split_list[book_index + 2:]
                split_list = row_list

            # replace 0 with None if there was no change
            if len(split_list[0]) == 0:
                split_list[0] = "None"
        
        if year >= 2021 and counter != 0: # collecting 2 race values into one list value
            race_combo = split_list[-2:]
            split_list[-2] = race_combo
            split_list = split_list[:-1]

        new_list.append(split_list) # adding split rows
        counter += 1

    if new_list[0][-1] == "":
        new_list[0] = new_list[0][:-1]

    # testing it separated correctly
    columns = new_list[0]
    column_no = len(columns)
    for row in new_list:
        if len(row) != column_no:
            print(year, ranking, columns)
            print(f"Incorrect number of items (expected {column_no}, received {len(row)}):", row)

    return new_list

def split_data_2015_to_2019(data_list:list[str], year:int, ranking:str):
    """
    takes a list of strings of the read-in txt data, the year and ranking contained in the filepath

    returns a new nested list

    each list item is another list with string values for each column item,
    except the pairing and fandom values are still concatenated due to single space separators
    """
    
    initial_list = []
    for string in data_list:
        # set separator
        separator = r"\s"

        # split
        split_list = [item.strip() for item in split(separator, string[:-1])]

        # append for now
        initial_list.append(split_list)

    new_list = []

    # make columns

    # special cases:
    if (ranking == "data") \
    or (ranking == "femslash" and year == 2015) \
    or (ranking == "overall" and year in [2015, 2016]):

        if ranking == "data" and year != 2016:
            col_index_1 = 4
        elif ranking == "data": # 2016 didn't have a change column yet
            col_index_1 = 3
        else:
            col_index_1 = 2

        # first few values
        column_list = initial_list[0][:col_index_1]

        # tag that needed combining
        combo_tag = " ".join(initial_list[0][col_index_1: col_index_1 + 2])
        column_list.append(combo_tag)

        if ranking == "femslash":
            # fandom, works
            column_list.extend(initial_list[0][4:-2])

            # release date
            release_date_column = initial_list[0][-2] + " " + initial_list[0][-1]
            column_list.append(release_date_column)
        else:
            if ranking == "data":
                remainder_index = -3
            elif ranking == "overall":
                remainder_index = -4

            column_list.extend(initial_list[0][remainder_index:])

    else:
        column_list = initial_list[0]

    # add column list
    new_list.append(column_list)

    # make rows

    # making index numbers based on cases
    if ranking == "data":
        if year != 2016:
            index_1 = 2
            index_2 = 2
        else:
            index_1 = 1
            index_2 = 1
        index_3 = -4
    else:
        index_1 = 1
        index_2 = 2
        if ranking == "femslash":
            if year == 2015:
                index_3 = -4
            else:
                index_3 = -2
        else:
            index_3 = -3

    for row in initial_list[index_1:]:
        # initial values
        row_list = row[:index_2]

        # combining pairings & fandoms
        pairings_and_fandoms = " ".join(row[index_2:index_3])
        row_list.append(pairings_and_fandoms.strip())

        # remaining values
        if ranking == "femslash" and year == 2015:
            # works
            row_list.append(row[index_3])

            # release date
            release_date = " ".join(row[-3:])
            row_list.append(release_date)
        else:
            row_list.extend(row[index_3:])

        # append row
        new_list.append(row_list)

    # testing it separated correctly
    columns = new_list[0]
    column_no = len(columns)
    for row in new_list[1:]:
        if len(row) != column_no - 1: # rows minus 1 bc pairing & fandom is still concat
            print(year, ranking, columns)
            print(f"Incorrect number of items (expected {column_no - 1}, received {len(row)}):", row)

    return new_list


def split_pairings_from_fandoms(data_list):
    pass

# TODO v refactor this one

# a function to comb through the pairing-fandom values and split them apart appropriately
    #I'm seeing a highly unfortunate scenario where we have to manually copy out all the fandoms 
    # and put em in a variable to check against rip
        # update: it was fine
def split_pairings_from_fandoms(data_list):
    """
    takes output list of split_raw_data_2015_to_2019 and splits the pairing-fandom value into
    a pairing & a fandom value 

    returns a list that matches the split_raw_data_2013_2014_and_2020_to_2023 output format
    """

    # make fandom list
        #we made a function for it! so we can access the files we get out of that!
    with open("data/reference_and_test_files/all_fandoms_list.json", "r") as json_file:
        fandom_dict = load(json_file)

    fandom_list = fandom_dict["all_fandoms"]

    # make new list
    separated_list = []
    # append first row to new list
    separated_list.append(data_list[0])

    for i in range(len(data_list[1])):
        if "Release Date" in data_list[0]: combo_index = 2
        elif " " in data_list[2][i]:
            combo_index = i

    # for each row (except first)
    for row in data_list[1:]:
        # make new row list
        new_row = []

        # append first x values until pairing/fandom value to new row list
        new_row.extend(row[:combo_index])

        # separate & append pairing & fandom value
        found_fandom = False
        value_to_be_separated = row[combo_index]
            # iterate through fandom list
        for fandom in fandom_list:
            # if fandom in value, split it at relevant spot
            if fandom in value_to_be_separated:
                if fandom == "Thor (Movies)":
                    split_values = split(r" Thor \(Movies\)", value_to_be_separated)
                elif fandom == "Loki (TV 2021)":
                    split_values = split(r" Loki \(TV 2021\)", value_to_be_separated)
                elif fandom == "Venom (Movie 2018)":
                    split_values = split(r" Venom \(Movie 2018\)", value_to_be_separated)
                elif fandom == "Maleficent (2014)":
                    split_values = split(r" Maleficent \(2014\)", value_to_be_separated)
                elif fandom == "Kim Possible (Cartoon)":
                    split_values = split(r" Kim Possible \(Cartoon\)", value_to_be_separated)
                elif fandom == "James Bond (Craig movies)":
                    split_values = split(r" James Bond \(Craig movies\)", value_to_be_separated)
                elif fandom == "Adam Lambert (Musician)":
                    split_values = split(r" Adam Lambert \(Musician\)", value_to_be_separated)
                elif fandom == "Carol (2015)":
                    split_values = split(r" Carol \(2015\)", value_to_be_separated)
                else: split_values = split(r" " + fandom, value_to_be_separated)
                white_space_index = len(split_values[0])
                separated_values = [
                    value_to_be_separated[:white_space_index], 
                    value_to_be_separated[white_space_index + 1:]
                    ]
                # append correctly split values to new row list
                new_row.extend(separated_values)
                found_fandom = fandom

            # otherwise print row so I can see which fandom is missing or misspellt & fix
        if not found_fandom:
            new_row.extend([" ", " "])
            print(value_to_be_separated)
                #this means we'll have to check through ALL the relevant data sets until 
                # we've got the full list smh
                #-> get starting values from newer data sets & add & change as needed

        # append remaining values to new row list
        new_row.extend(row[combo_index + 1:])

        # append new row list to new list
        separated_list.append(new_row)

    return separated_list
