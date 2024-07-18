from re import split

# function to extract file paths into a list we can cycle through

# function that splits rows into individual values
def split_raw_data_2020_to_2023(filepath: str):
    """
    takes the filepath to a .txt file of lines of rows with values separated by \\t characters
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
    for string in read_data:
        split_list = split(r"\t", string[:-1]) # splitting at the tabs
        data_list.append(split_list) # nesting list

    return data_list

# a variant of the above function that works for the remaining data sets' formatting

# a function that takes the data_list format_raw_data func spits out and separates the pairings
    # find the values that contain slashes & ampercents -> split at those items
def separate_pairings(data_list):
    """
    takes a list of row lists containing values at the relationship/pairing/ship \
        and type index positions that are separated by "/" or "&" characters
    separates those values into a list at same index position and returns new list of row lists
    """
    output_nested_list = [data_list[0]]
    pairing_index = 0
    type_index = 0

    for index in range(len(data_list[0])):

        #figure out pairing index 
            # "Relationship" (2021 onward) or "Pairing" (2014-2020) or "Ship" (2013 only)
        if data_list[0][index] == "Relationship " \
            or data_list[0][index] == "Pairing " \
            or data_list[0][index] == "Ship ":
            pairing_index = index

        #figure out pairing tag index if any 
            # "Type"
        elif data_list[0][index] == "Type ":
            type_index = index

    for row in data_list[1:]:
        #temp list with prior values, excluding relevant item
        temp_list = row[:pairing_index]

        #split pairing item at relevant character
        pairing_list = split(r"[\/&]", row[pairing_index])
        #append to temp list
        temp_list.append(pairing_list)

        #if pairing tag has a /
        if "Type " in data_list[0] and "/" in row[type_index]:
            #append middle values to temp list
            for value in row[pairing_index + 1 : type_index]:
                temp_list.append(value)

            #split pairing tag item at /
            type_list = split(r"\/", row[type_index])

            #append to temp list
            temp_list.append(type_list)
            #append remaining values
            for value in row[type_index + 1 :]:
                temp_list.append(value)

        else:
            #append remaining list
            for value in row[pairing_index + 1 :]:
                temp_list.append(value)

        output_nested_list.append(temp_list)

    return output_nested_list

# a function that takes output_nested_list spit out by separate_pairings func & removes trailing whitespaces
    # find all values that end in " " and remove last whitespace character




#finally:
        # this seems to be the format since 2020, so we can reuse this specific code for 
        # all of those files! 2023 filepath = "data/raw_data/ao3_2023/raw_ao3_2023_data.txt"
        # cycle through a list of file path strings, to insert into our open() context manager
# print cleaned data into a new file for reading (csv?)
