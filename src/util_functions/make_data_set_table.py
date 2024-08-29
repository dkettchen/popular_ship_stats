from json import dump
from write_csv_file import make_csv_file

def make_data_set_table(ordered_path_dict):
    """
    takes a dictionary with year number keys and list of strings values 
    containing filepaths to our main datasets

    returns a dictionary with keys labelled after and dict values 
    containing the website (currently only ao3), year, and type
    (currently only femslash, overall and data) of the dataset in question
    """

    all_data_sets = {}
    for year in ordered_path_dict:
        for path in ordered_path_dict[year]:
            set_type = None
            if "femslash" in path:
                set_type = "femslash"
            elif "overall" in path:
                set_type = "overall"
            else:
                set_type = "data"

            website = None
            if "ao3" in path:
                website = "AO3"
            
            data_set_info = {
                "year" : year,
                "type" : set_type,
                "website" : website,
            }

            key_name = f"{website}_{year}_{set_type}"

            all_data_sets[key_name] = data_set_info

    sorted_data_sets = {}
    sorted_keys = sorted(list(all_data_sets.keys()))
    for key in sorted_keys:
        sorted_data_sets[key] = all_data_sets[key]

    return sorted_data_sets

def prep_data_set_table_for_csv(ordered_dict):
    csv_list = [["data_set", "website", "year", "type"]] # adding column names

    for key in ordered_dict:
        website = ordered_dict[key]["website"]
        year = ordered_dict[key]["year"]
        set_type = ordered_dict[key]["type"]
        values_list = [key, website, year, set_type]

        csv_list.append(values_list)
    
    return csv_list
        


if __name__ == "__main__":
    all_ordered_paths = { 
        2023: [
            'data/fourth_clean_up_data/ao3_2023/raw_ao3_2023_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2023/raw_ao3_2023_data.json', 
            'data/fourth_clean_up_data/ao3_2023/raw_ao3_2023_overall_ranking.json',
        ],
        2022: [
            'data/fourth_clean_up_data/ao3_2022/raw_ao3_2022_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2022/raw_ao3_2022_data.json', 
            'data/fourth_clean_up_data/ao3_2022/raw_ao3_2022_overall_ranking.json',
        ],
        2021: [
            'data/fourth_clean_up_data/ao3_2021/raw_ao3_2021_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2021/raw_ao3_2021_data.json', 
            'data/fourth_clean_up_data/ao3_2021/raw_ao3_2021_overall_ranking.json',
        ],
        2020: [
            'data/fourth_clean_up_data/ao3_2020/raw_ao3_2020_femslash_ranking.json',
            'data/fourth_clean_up_data/ao3_2020/raw_ao3_2020_data.json',  
            'data/fourth_clean_up_data/ao3_2020/raw_ao3_2020_overall_ranking.json',
        ], 
        2019: [
            'data/fourth_clean_up_data/ao3_2019/raw_ao3_2019_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2019/raw_ao3_2017-2019_data.json', 
            'data/fourth_clean_up_data/ao3_2019/raw_ao3_2019_overall_ranking.json',
        ], 
        2017: [
            'data/fourth_clean_up_data/ao3_2017/raw_ao3_2017_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2017/raw_ao3_2017_data.json', 
            'data/fourth_clean_up_data/ao3_2017/raw_ao3_2017_overall_ranking.json',
        ], 
        2016: [
            'data/fourth_clean_up_data/ao3_2016/raw_ao3_2016_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2016/raw_ao3_2016_data.json', 
            'data/fourth_clean_up_data/ao3_2016/raw_ao3_2016_overall_ranking.json',
        ], 
        2015: [
            'data/fourth_clean_up_data/ao3_2015/raw_ao3_2015_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2015/raw_ao3_2015_overall_ranking.json',
        ], 
        2014: [
            'data/fourth_clean_up_data/ao3_2014/raw_ao3_2014_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2014/raw_ao3_2014_overall_ranking.json',
        ], 
        2013: [
            'data/fourth_clean_up_data/ao3_2013/raw_ao3_2013_overall_ranking.json',
            ],
    }
    data_set_dict = make_data_set_table(all_ordered_paths)
    filepath = "data/reference_and_test_files/data_sets.json"
    with open(filepath, "w") as file:
        dump(data_set_dict, file, indent=4)
    csv_data = prep_data_set_table_for_csv(data_set_dict)
    csv_path = "data/reference_and_test_files/data_sets.csv"
    make_csv_file(csv_data, csv_path)