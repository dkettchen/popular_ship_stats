from json import loads

def get_json_lines_data(filepath):
    """
    takes a filepath to a json lines formatted file

    returns the contents of the file formatted as a list of dicts
    """
    loaded_dicts_list = []

    with open(filepath, 'r') as file:
        for line in file:
            data_entry = loads(line) # turns the line back into a dict
            loaded_dicts_list.append(data_entry)

    return loaded_dicts_list