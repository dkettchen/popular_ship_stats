from re import split, sub
from json import load
from src.cleaning_code_refactor_utils.separate_pairings import separate_pairings

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
    if year not in [2015, 2016, 2017, 2019]: 
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

    else: # single space separator years
        split_list = split_data_2015_to_2019(data_list, year, ranking)
        new_list = split_pairings_from_fandoms(split_list)

    separated_pairs = separate_pairings(new_list)
    new_list = separated_pairs


    # testing it separated correctly
    columns = new_list[0]
    column_no = len(columns)
    for row in new_list:
        if len(row) != column_no:
            print(year, ranking, columns)
            print(f"Incorrect number of items (expected {column_no}, received {len(row)}):", row)

    return new_list

# helpers for single space separators years
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

def split_pairings_from_fandoms(data_list:list[str]):
    """
    splits pairings from their fandoms

    returns new list with split values
    """

    # reference file for fandoms
    with open("data/reference_and_test_files/cleaning_fandoms/all_fandoms_list.json", "r") as json_file:
        fandom_dict = load(json_file)

    fandom_list = fandom_dict["all_fandoms"]

    # append first row (columns)
    columns = data_list[0]
    separated_list = [columns]

    for i in range(len(data_list[1])):
        if "Release Date" in columns:
            combo_index = 2
            break
        elif " " in data_list[2][i]:
            combo_index = i
            break

    # non-column rows
    for row in data_list[1:]:
        # make new row, same values up to pairing/fandom item
        new_row = row[:combo_index]

        found_fandom = False
        value_to_be_separated = row[combo_index]

        for fandom in fandom_list:
            if fandom in value_to_be_separated:
                # fandoms with same names as characters
                if fandom in [
                    "Thor (Movies)", 
                    "Loki (TV 2021)",
                    "Venom (Movie 2018)", 
                    "Maleficent (2014)",
                    "Kim Possible (Cartoon)",
                    "James Bond (Craig movies)",
                    "Adam Lambert (Musician)",
                    "Carol (2015)",
                ]:
                    fandom_regex = sub("\(", "\\\(", fandom) # replace ( with escaped \(
                    fandom_regex = sub("\)", "\\\)", fandom_regex)
                    split_values = split(r" " + fandom_regex, value_to_be_separated)
                else:
                    split_values = split(r" " + fandom, value_to_be_separated)

                # this should only be pairing now
                white_space_index = len(split_values[0])
                # pairing / white space / fandom
                separated_values = [
                    value_to_be_separated[:white_space_index], 
                    value_to_be_separated[white_space_index + 1:]
                ]
                # append to new row
                new_row += separated_values

                # fandom has been found
                found_fandom = fandom

                break
            
        if not found_fandom: # if not found, print
            new_row += [" ", " "]
            print(value_to_be_separated)

        # append remaining values to new row
        new_row += row[combo_index + 1:]

        # append new row
        separated_list.append(new_row)
    
    return separated_list
