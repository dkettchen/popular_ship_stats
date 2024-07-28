from src.util_functions.retrieve_data_from_csv import read_data_from_csv

def add_missing_columns(data_list: list):
    """
    takes a nested list from any of the second_clean_up_data files

    returns a list of dictionaries with the following keys 
    (and their corresponding values, 
    which will be None if the input didn't have the column in question)
    Rank, Change, Relationship, Fandom, New Works, Total Works, Type, Race, Release Date
    """
    column_dict = {}
    for i in range(len(data_list[0])):
        column_dict[data_list[0][i]] = i 
        #making a dict of our column names + their index position
        # {"Column Name": <index_num>}

    output_list = []
    for row in data_list[1:]:
        temp_dict = {
            "Rank" : None, #always present
            "Change" : [None, None],
            "Relationship" : None, #always present
            "Fandom" : None, #always present
            "New Works" : None,
            "Total Works" : None, #always present
            "Type" : ["F", "F"],
            "Race" : [None, None],
            "Release Date" : None
        }  #adding default values

        #we want:
        # {
        # "Rank" : <rank_list>
        # "Change" : <change_list> (add [none, none] one if it doesn't have one yet)
        # "Relationship" : <pairing_list>
        # "Fandom" : <fandom_string>
        # "New Works" : <new_works_num> or None if no info
        # "Total Works" : <total_num>
        # "Type" : <type_str> or <type_list> (add [F, F] for all femslash ones that are missing them)
        # "Race" : <race_str> or <race_list> or [None, None] if no such column
        # }

        for key in column_dict:
            # for each name in the columns
                                 # we use its index
            temp_dict[key] = row[column_dict[key]]
                            # to find the corresponding value in the current row
            # to update the default dict's key-value
                            # with the new value
            # -> leaving non-present values at default! (I think!)
        
        output_list.append(temp_dict)

    return output_list

if __name__ == "__main__":
    print(add_missing_columns(
        read_data_from_csv("data/second_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
    ))
    pass