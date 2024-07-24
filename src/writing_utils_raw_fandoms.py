from re import split
from json import dump, load
from split_values import split_raw_data_2013_2014_and_2020_to_2023
from separate_values import separate_pairings
from get_file_paths import find_paths

# a function that retrieves lists of fandoms & makes them into json files for easier reference access
def get_2020_to_2023_raw_fandom_data(filepath):
    """
    takes a filepath to a raw data txt in the range of the 2020-2023 ao3 data sets

    writes a json file with a dict with a "fandoms" key and a list value containing unique
    strings of the names of the fandoms/properties featured in that data set's ranking

    it does not consider sub-titles to differentiate between spin-offs of the same franchise (name) 
    (eg 'Law & Order' and 'Law & Order: SVU' will be listed as a single 'Law & Order' value)

    it also removes any indicated property type 
    (eg 'Call of Duty (Video Games)' will be listed as 'Call of Duty'), and
    author name(s) (eg 'Lockwood & Co. - Jonathan Stroud' will be listed as 'Lockwood & Co')
    """
    data_list = separate_pairings(
        split_raw_data_2013_2014_and_2020_to_2023(filepath)
    )
    
    property_list = list(set([row[3] for row in data_list[1:]]))

    new_list = []
    for fandom in property_list:
        if "(" in fandom:
            # getting rid of property type & year info
            split_value_1 = split(r" \(", fandom)
            fandom = split_value_1[0]
        # if " | " in fandom:
        #     # getting rid of as many foreign language characters as possible
        #     split_value_4 = split(r" \| ", fandom) 
        #     fandom = split_value_4[-1]
        if " - " in fandom:
            # getting rid of author names & "all media types"
            split_value_2 = split(r" - ", fandom)
            fandom = split_value_2[0]
        if ":" in fandom:
            # getting rid of sub titles
            split_value_3 = split(r":", fandom)
            fandom = split_value_3[0]
        if fandom == "Supernatural RPF":
            fandom = "Supernatural"
        if fandom == "Thor":
            fandom = "Thor (Movies)"
        if fandom == "Loki":
            fandom = "Loki (TV 2021)"
        if fandom == "James Bond":
            fandom = "James Bond (Craig movies)"
        if fandom == "Mass Effect Trilogy":
            fandom = "Mass Effect"
        if fandom == "Dragon Age II":
            fandom = "Dragon Age"
        if fandom == "Star Wars Sequel Trilogy":
            fandom = "Star Wars"
        if fandom == "RuPaul's Drag Race RPF":
            fandom = "RuPaul's Drag Race"
        if fandom == "Carol":
            fandom = "Carol (2015)"
        if fandom == "魔道祖师" or fandom == "Módào Zǔshī":
            fandom = "魔道祖师"

        # the untamed boys are giving me trouble of all ppl smh
        #           "M\u00f3d\u00e0o Z\u01d4sh\u012b",
        #           "\u9648\u60c5\u4ee4 | The Untamed",
        #           "\u9b54\u9053\u7956\u5e08" <- this is the correct one for the book title
        # 魔道祖师 - 墨香铜臭 |', 'Módào Zǔshī - Mòxiāng Tóngxiù

        # 魔道祖师 - 墨香铜臭 | Módào Zǔshī - Mòxiāng Tóngxiù
        # 陈情令 | The Untamed 
        # WHY IS IT DIFFERENT SYMBOLS AAAAAH -> these are from the same data set also


        new_list.append(fandom)

    file_name = filepath[27:-4]

    output_dict = {"fandoms": sorted(list(set(new_list)))}

    with open(f"data/raw_fandom_lists/fandom_list_{file_name}.json", "w") as json_file:
        dump(output_dict, json_file, indent=4)

# a function to compile those into one master list!
def get_all_2020_to_2023_fandoms():
    """
    writes a json file containing a dict with the key "2020-2023_fandoms" 
    and a list value containing all unique fandom names contained in those data sets, 
    formatted according to get_2020_to_2023_raw_fandom_data function
    """

    all_data_filepaths = find_paths("data/")
    fandom_list_paths = [path for path in all_data_filepaths if "raw_fandom_lists" in path]

    list_of_data = []
    for file in fandom_list_paths:
        with open(file, "r") as json_file:
            content = load(json_file)
        list_of_data.append(content["fandoms"])

    complete_data_list = []
    for data_set in list_of_data:
        complete_data_list.extend(data_set)
    complete_data_list = sorted(list(set(complete_data_list)))

    output_dict = {"2020-2023_fandoms": complete_data_list}

    with open("data/reference_and_test_files/all_fandoms_2020_to_2023.json", "w") as new_file:
        dump(output_dict, new_file, indent=4)

def run_functions_to_get_all_recent_fandoms():
    """
    runs the code necessary to get the complete list of 
    unique fandom names in the ranking between 2020 and 2023
    output as a dictionary into a json file
    """
    file_paths = find_paths("data/raw_data/")
    for path in file_paths:
        if "202" in path:
            get_2020_to_2023_raw_fandom_data(path)
    get_all_2020_to_2023_fandoms()

# a function to make a more complete master list
def update_fandom_list_with_missing_fandoms():
    """
    creates (or updates) an all_fandoms_list json file by 
    combining all_fandoms_2020_to_2023 and missing_fandoms files' contents
    """

    with open("data/reference_and_test_files/all_fandoms_2020_to_2023.json", "r") as recent_fandoms:
        recent_fandoms_dict = load(recent_fandoms)
    with open("data/reference_and_test_files/missing_fandoms.json", "r") as missing_fandoms:
        missing_fandoms_dict = load(missing_fandoms)

    new_list = []
    new_list.extend(recent_fandoms_dict["2020-2023_fandoms"])
    new_list.extend(missing_fandoms_dict["missing_fandoms"])
    #this currently only appends the values as I've put them in, 
    # do I wanna manually format them or write a func?
        #as soon as I typed that I was like fuck writing another function it's fine x'D
        #update: I have manually formatted the ones that were in there so far

    new_list = sorted(list(set(new_list)))
    output_dict = {"all_fandoms": new_list}

    with open("data/reference_and_test_files/all_fandoms_list.json", "w") as new_json_file:
        dump(output_dict, new_json_file, indent=4)

if __name__ == "__main__":
    run_functions_to_get_all_recent_fandoms()
    update_fandom_list_with_missing_fandoms()
    pass