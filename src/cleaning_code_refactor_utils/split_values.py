from re import split

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
                temp_list = split_list[:book_index] + [book] + split_list[book_index + 2:]
                split_list = temp_list

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
