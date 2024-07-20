from re import split

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

        else:
            split_list = split(r" \t", string[:-1]) # splitting at the tabs
        data_list.append(split_list) # nesting list

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
        new_list.append(data_list[0])
        for row in data_list[1:]:
            temp_list = []
            temp_list.extend(row[:2])

            pairings_and_fandoms = ""
            for item in row[2:-2]:
                pairings_and_fandoms += " " + item
            temp_list.append(pairings_and_fandoms[1:])

            temp_list.extend(row[-2:])
            new_list.append(temp_list)
    elif "overall" in filepath:

        column_list = []
        column_list.extend(data_list[0][:2])

        pairing_tag = ""
        for item in data_list[0][2:4]:
            pairing_tag += " " + item
        column_list.append(pairing_tag[1:])

        column_list.extend(data_list[0][-4:])
        new_list.append(column_list)

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


#TODO: implement splitting pairings from their fandoms!
# a function to comb through the pairing-fandom values and split them apart appropriately
    #I'm seeing a highly unfortunate scenario where we have to manually copy out all the fandoms 
    # and put em in a variable to check against rip
def split_pairings_from_fandoms(data_list):
    # make fandom list
        #we made a function for it! so we can access the files we get out of that!

    # make new list
    # append first row to new list

    # for each row (except first)
        # make new row list

        # append first x values until pairing/fandom value to new row list

        # separate & append pairing & fandom value
            # iterate through fandom list
            # if fandom in value, split it at relevant spot
            # otherwise print row so I can see which fandom is missing or misspellt & fix
                #this means we'll have to check through ALL the relevant data sets until 
                # we've got the full list smh
                #-> get starting values from newer data sets & add & change as needed
            # append correctly split values to new row list
        
        # append remaining values to new row list

        # append new row list to new list


    pass


# a function that takes the data_list format_raw_data func spits out and separates the pairings
    # find the values that contain slashes & ampercents -> split at those items
def separate_pairings(data_list):
    """
    takes a list of row lists containing values at the relationship/pairing/ship \
        and type index positions that are separated by "/" or "&" characters, \
            and ending in two race values
    separates each of the former values into a list at same index position, \
        gathers the latter two into one list in original order at last index position \
            and returns new list of row lists
    """
    output_nested_list = [data_list[0]]
    pairing_index = 0
    type_index = 0

    for index in range(len(data_list[0])):

        #figure out pairing index 
            # "Relationship" (2021 onward) or "Pairing" (2014-2020) or "Ship" (2013 only)
        if data_list[0][index] == "Relationship" \
            or data_list[0][index] == "Pairing" \
            or data_list[0][index] == "Ship":
            pairing_index = index

        #figure out pairing tag index if any 
            # "Type"
        elif data_list[0][index] == "Type":
            type_index = index

    for row in data_list[1:]:
        #temp list with prior values, excluding relevant item
        temp_list = row[:pairing_index]

        #split pairing item at relevant character
        pairing_list = split(r"[\/&]", row[pairing_index])
        #append to temp list
        temp_list.append(pairing_list)

        up_to_pairing = True

        #if type tag has a /
        if "Type" in data_list[0] and "/" in row[type_index]:
            #append middle values to temp list
            temp_list.extend(row[pairing_index + 1 : type_index])

            #split type tag item at /
            type_list = split(r"\/", row[type_index])

            #append to temp list
            temp_list.append(type_list)
        
            up_to_pairing = False
        
        if data_list[0][-2] == "Race" or "Race" not in data_list[0]: #append remaining values
            if up_to_pairing:
                temp_list.extend(row[pairing_index + 1 :])
            else: # if up to type
                temp_list.extend(row[type_index + 1 :])
        else: #gather race values into a list
            if up_to_pairing:
                temp_list.extend(row[pairing_index + 1 : -2])
                temp_list.append(row[-2 :])
            else: # if up to type            
                temp_list.append(row[-2 :])

        output_nested_list.append(temp_list)

    return output_nested_list


if __name__ == "__main__":
    pass

    # make_csv_file(
    #     separate_pairings(
    #         split_raw_data_2013_2014_and_2020_to_2023("data/raw_data/ao3_2023/raw_ao3_2023_data.txt")
    #     ),
    #     "data/clean_data_test.csv"
    #  )