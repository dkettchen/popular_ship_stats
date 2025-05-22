from re import split

def separate_pairings(data_list):
    """
    separates pairing members into a list value

    returns a new list
    """

    columns = data_list[0]

    output_list = [columns]

    # find indexes?
    pairing_index = None
    type_index = None
    for i in range(len(columns)):
        if columns[i] in ["Relationship", "Pairing", "Pairing Tag", "Ship"]:
            pairing_index = i
        elif columns[i] in ["Type"]:
            type_index = i
    if not pairing_index:
        print("Why no pairing index?", columns)

    for row in data_list[1:]:
        # up to pairing item
        new_row = row[:pairing_index]

        # separate pairing at & or / and strip off leading/trailing white spaces
        pairing_item = row[pairing_index]
        pairing_list = [item.strip() for item in split(r"[\/&]", pairing_item)]
        new_row.append(pairing_list)

        # append remaining values
        if type_index: # if there's a type column
            # append type first
            if "/" in pairing_item: # type item is smth other than "other" & "gen"
                # add values between pairing & type column
                new_row += row[pairing_index + 1 : type_index]

                # split type item
                type_list = split(r"\/", row[type_index])

                new_row.append(type_list)
            else: # type item is "other" or "gen"
                new_row += row[pairing_index + 1 : type_index + 1]

            # then rest
            new_row += row[type_index + 1:]
        else:
            # append all other values
            new_row += row[pairing_index + 1:]

        output_list.append(new_row)

    return output_list


