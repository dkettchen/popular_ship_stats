from re import split
from json import load

# function that splits rows into individual values
def split_raw_data_2013_2014_and_2020_to_2023(filepath: str):
    """
    takes the filepath to a .txt file of lines of rows with values separated by "\\t"  or " - "
    returns a list of row lists of separated value strings
    """
    # how to access txt files?
    # take one of the files    
    with open(filepath, "r", encoding="utf-8") as raw_data:

        # separate out lines as list of strings first
        read_data = raw_data.readlines() # this is a list of strings with each line!

    # separate out all the items without the spaces/formatting etc, list of lists
        # separate on " \t" and remove "\n" (every item in this set is separated by the former 
        # & ends on the latter (with exception of last entry))
    data_list = []
    read_data[-1] += "\n" # adding the missing last newline character
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
    for string in read_data:
        #we could add the regex for 2013 & 2014 here 👀 
            # we'd just need to "change all instances" on our tests etc to adjust the func name
        if "2013" in filepath:
            if "2013" in filepath and string == read_data[0]:
                split_list = split(r"\s", string[:-1])
            else:
                split_list = split(r" - ", string[:-1]) # splitting at the " - " separators
            if  "2013" in filepath and split_list[2] in books:
                book = split_list[2] + split_list[3]
                temp_list = []
                temp_list.extend(split_list[:2])
                temp_list.append(book)
                temp_list.extend(split_list[4:])
                split_list = temp_list

        elif "2014" in filepath:
            split_list = split(r" - ", string[:-1]) # splitting at the " - " separators
            if "2014_overall" in filepath and split_list[3] in books:
                book = split_list[3] + split_list[4]
                temp_list = []
                temp_list.extend(split_list[:3])
                temp_list.append(book)
                temp_list.extend(split_list[5:])
                split_list = temp_list
            elif "2014_femslash" in filepath and split_list[2] in books:
                book = split_list[2] + split_list[3]
                temp_list = []
                temp_list.extend(split_list[:2])
                temp_list.append(book)
                temp_list.extend(split_list[4:])
                split_list = temp_list

        elif "2023" in filepath:
            split_list = split(r" \t", string[:-1]) # splitting at the tabs

        else:       
            split_list = split(r"\s{3}", string[:-1])

        data_list.append(split_list) # nesting list
    if data_list[0][-1] == "":
        data_list[0] = data_list[0][:-1]
    return data_list

# a variant of the above function that works for the remaining data sets' formatting:
#   -2015-2019 is just separated by white spaces which is inconvenient 
#   & will require extra steps to separate the pairings from the fandoms
def split_raw_data_2015_to_2019(filepath: str):
    """
    takes the filepath to a .txt file of lines of rows with values separated by single whitespaces

    returns a list of row lists of separated value strings except for pairing & fandom values \
    (as they contain whitespaces)
    """
    with open(filepath, "r", encoding="utf-8") as raw_data:
        read_data = raw_data.readlines()
    #each line string ends in \n, but the values are separated by a single whitespace ToT

    data_list = []
    read_data[-1] += "\n" # adding the missing last newline character
    for string in read_data:
        split_list = split(r"\s", string[:-1]) # splitting at the white spaces (all of em)
        data_list.append(split_list) # nesting list
    
    new_list = [] # separating out columns & everything other than pairing & fandom values
    if "data.txt" in filepath and "2016" not in filepath: 
        #2016 was the first year of yearly data, so it doesn't have a "change" column yet

        column_list = []
        column_list.extend(data_list[0][:4])

        new_works = ""
        for item in data_list[0][4:6]:
            new_works += " " + item
        column_list.append(new_works[1:])

        column_list.extend(data_list[0][-3:])
        new_list.append(column_list)

        for row in data_list[1:]:
            temp_list = []
            temp_list.extend(row[:2])

            pairings_and_fandoms = ""
            for item in row[2:-4]:
                pairings_and_fandoms += " " + item
            temp_list.append(pairings_and_fandoms[1:])

            temp_list.extend(row[-4:])
            new_list.append(temp_list)
    elif "data.txt" in filepath and "2016" in filepath:
        #doesn't have a change column yet
        column_list = []
        column_list.extend(data_list[0][:3])

        new_works = ""
        for item in data_list[0][3:5]:
            new_works += " " + item
        column_list.append(new_works[1:])

        column_list.extend(data_list[0][-3:])
        new_list.append(column_list)

        for row in data_list[1:]:
            temp_list = []
            temp_list.append(row[0])

            pairings_and_fandoms = ""
            for item in row[1:-4]:
                pairings_and_fandoms += " " + item
            temp_list.append(pairings_and_fandoms[1:])

            temp_list.extend(row[-4:])
            new_list.append(temp_list)
    elif "femslash" in filepath:
        if "2015" in filepath:
            new_list.append(data_list[0][:2])

            pairing_tag_column = data_list[0][2] + " " + data_list[0][3]
            new_list[0].append(pairing_tag_column)

            new_list[0].extend(data_list[0][4:-2])

            release_date_column = data_list[0][-2] + " " + data_list[0][-1]
            new_list[0].append(release_date_column)
            
        else: new_list.append(data_list[0])

        for row in data_list[1:]:
            temp_list = []
            temp_list.extend(row[:2])

            pairings_and_fandoms = ""
            if "2015" in filepath:
                for item in row[2:-4]:
                    pairings_and_fandoms += " " + item

                temp_list.append(pairings_and_fandoms[1:])
                temp_list.append(row[-4])
                
                release_date = row[-3] + " " + row[-2] + " " + row[-1]
                temp_list.append(release_date)

            else:
                for item in row[2:-2]:
                    pairings_and_fandoms += " " + item
                temp_list.append(pairings_and_fandoms[1:])
                temp_list.extend(row[-2:])

            new_list.append(temp_list)
    elif "overall" in filepath:
        if "2016" in filepath or "2015" in filepath:
            column_list = []
            column_list.extend(data_list[0][:2])

            pairing_tag = ""
            for item in data_list[0][2:4]:
                pairing_tag += " " + item
            column_list.append(pairing_tag[1:])

            column_list.extend(data_list[0][-4:])
            new_list.append(column_list)

        else: new_list.append(data_list[0])

        for row in data_list[1:]:
            temp_list = []
            temp_list.extend(row[:2])

            pairings_and_fandoms = ""
            for item in row[2:-3]:
                pairings_and_fandoms += " " + item
            temp_list.append(pairings_and_fandoms[1:])

            temp_list.extend(row[-3:])
            new_list.append(temp_list)

    return new_list

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

if __name__ == "__main__":
    pass