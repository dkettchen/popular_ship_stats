from csv import writer

# a function that takes cleaned data, formats it (eg json or csv) 
# and prints it into a new file for reading
    # should take desired file name & cleaned data nested list as arguments
def make_csv_file(clean_data: list, file_name: str):
    """
    takes a list of lists of values and a string with the desired \
    name/filepath for the output file (must end in .csv)

    creates a csv file where the rows are the nested lists of values
        the values are comma separated and any values that contained commas \
        (including say lists) will be escaped with double quotation marks (")
    """
    strings_list = []
    for item in clean_data:
        temp_list = [str(value) for value in item]
        strings_list.append(temp_list)

    with open(file_name, "w", newline="") as csv_file:
        clean_writer = writer(csv_file, quotechar="`")
        clean_writer.writerows(strings_list)

if __name__ == "__main__":

    pass