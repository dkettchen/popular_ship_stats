from re import split

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
            or data_list[0][index] == "Pairing Tag" \
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
        if " & " in row[pairing_index]:
            pairing_list = split(r" & ", row[pairing_index])
        else:
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
        
        if data_list[0][-2] == "Race" \
        or "Race" not in data_list[0] \
        or len(data_list[0]) == len(row): #append remaining values
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