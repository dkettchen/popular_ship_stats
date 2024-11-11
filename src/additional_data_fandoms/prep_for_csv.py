def list_of_dicts_to_list_of_lists(input_list, key_list):
    """
    takes a list of dicts and a list of the keys of the dicts within in the order one wants them

    returns a list of lists where the nested lists contain the values of the keys in the given order
    """
    
    prepped_list = [key_list]
    for item in input_list:
        temp_list = []
        for key in key_list:
            temp_list.append(item[key])
        prepped_list.append(temp_list)

    return prepped_list
