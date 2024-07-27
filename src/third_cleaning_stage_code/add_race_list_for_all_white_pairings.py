from src.util_functions.retrieve_data_from_csv import read_data_from_csv

def add_list_for_white_only_pairings(data_list):
    """
    takes any data_set that has a race column up to 2020 included 
    (overall since 2014, data & femslash since 2016)

    returns it with all "White" values changed to ["White", "White"] to match later sets
    """

    new_list = [data_list[0]]
    if data_list[0][-2] == "Race":
        column_index = -2
    else:
        column_index = -1
    for row in data_list[1:]:
        new_row = row[0:column_index]
        if row[column_index] == "White":
            new_row.append(["White", "White"])
        else: new_row.append(row[column_index])
        if column_index == -2:
            new_row.append(row[-1])
        new_list.append(new_row)

    return new_list

if __name__ == "__main__":
    print(add_list_for_white_only_pairings(
        read_data_from_csv("data/second_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
    ))
    pass
        