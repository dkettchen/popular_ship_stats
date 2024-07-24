from csv import reader
from re import split
from string import digits

def read_data_from_csv(filepath: str):
    """
    takes a filepath to a csv file
    
    returns a nested list of its contents, 
    with all useable lists and integers 
    converted back into the correct file type 
    (remaining values are strings)
    """
    with open(filepath, "r", newline="") as csv_file:
        read_data = reader(csv_file)
        data_list = [row for row in read_data] #turns it into a list of lists of string values
        
    output_list = []
    for row in data_list:
        new_row = []
        for item in row:
            print(item, filepath)
            if item[0] == "[": # if it's supposed to be a list
                split_item = split(r"'", item)
                new_item = [bit for bit in split_item if bit not in ["[", "]", ", "]]
                    # we're turning it back into a list
            elif item == "None": #if it's supposed to be a none value
                new_item = None
            else:
                is_integer = True
                for char in item:
                    if char not in digits: # if any character is not a number
                        is_integer = False # it's not a useable number
                        break
                if is_integer:
                    new_item = int(item) # if it's a useable number, we turn it into one
                else: new_item = item # otherwise the string is fine

            #we may add other type cases as need be later if relevant
            
            new_row.append(new_item)
        output_list.append(new_row)
    return output_list




if __name__ == "__main__":
    read_data_from_csv("data/first_clean_up_data/ao3_2016/raw_ao3_2016_data.csv")
    pass