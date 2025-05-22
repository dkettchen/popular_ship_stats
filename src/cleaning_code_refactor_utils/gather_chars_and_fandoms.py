def gather_raw_chars_and_fandoms(data_dict:dict):
    """
    takes a nested dictionary from parsing stage

    returns a dictionary containing all raw fandom names (as keys)
    and the raw character names appearing with them (as list values)
    """

    chars_and_fandoms = {}
    
    # iterating over all files
    for year in data_dict:
        for ranking in data_dict[year]: 
            data_df = data_dict[year][ranking]

            # get all fandoms
            unique_fandoms = list(data_df["Fandom"].unique()) 

            # add fandom to dict if new
            for fandom in unique_fandoms: 
                if fandom not in chars_and_fandoms:
                    chars_and_fandoms[fandom] = []
            
            # put characters in relevant fandoms
            for row in data_df.index:
                current_relationship = data_df.loc[row, "Relationship"]
                current_fandom = data_df.loc[row, "Fandom"]

                # iterate over all characters in relationship
                for char in current_relationship:
                    # if they're not in their fandom's list yet, add them
                    if char not in chars_and_fandoms[current_fandom]:
                        chars_and_fandoms[current_fandom].append(char)

    # all fandoms should have characters to go with them
    for key in chars_and_fandoms:
        if len(chars_and_fandoms[key]) == 0:
            print(key)

    return chars_and_fandoms
