from json import load, dump

def collect_gender_tags():
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

    char_path = "data/reference_and_test_files/cleaning_characters/cleaned_characters_list_5_complete_character_names.json"
    with open(char_path, "r") as char_file:
        all_characters = load(char_file)["complete_characters"]
        # dict w rpf & fictional keys, fandom keys in those, char name keys in those, lotsa name bits etc in there

    rpf_dict = all_characters["RPF"] # we don't need to deepcopy this bc we're reading from the file
    fic_dict = all_characters["fictional"] # -> it can be mutated, cause the file won't be changed
    # {<fandom>:{<char>:{<stuff>}}}


    for year in all_ordered_paths: # going through all the files
        for path in all_ordered_paths[year]:
            if "femslash" in path:
                rank_type = "femslash"
            elif "overall" in path:
                rank_type = "overall"
            elif "data" in path:
                rank_type = "yearly"
            else: print(path)

            # get data set at this file path
            with open(path, "r") as data_file:
                dict_list = load(data_file) # list of dicts
            
            for row in dict_list:
                fandom = row["Fandom"]
                rpf_or_fic = row["RPF or Fic"]
                if rpf_or_fic == "RPF":
                    category_dict = rpf_dict
                elif rpf_or_fic == "fictional":
                    category_dict = fic_dict

                for character in row["Relationship"]:
                    character_dict = category_dict[fandom][character]

                    # if keys don't exist yet, add them (empty) first
                    if "most_recent_gender_tag" not in character_dict.keys():
                        character_dict["most_recent_gender_tag"] = None
                    if "most_recent_same_sex_tag" not in character_dict.keys():
                        character_dict["most_recent_same_sex_tag"] = None
                    if "all_gender_tags" not in character_dict.keys():
                        character_dict["all_gender_tags"] = set()

                    # if we don't have a tag yet
                    if not character_dict["most_recent_gender_tag"]: 
                        character_dict["most_recent_gender_tag"] = row["Type"]

                    # if we don't have a same sex tag yet and it is a same sex tag
                    if not character_dict["most_recent_same_sex_tag"] \
                    and row["Type"] in [["M", "M"], ["F","F"]]:  
                        character_dict["most_recent_same_sex_tag"] = row["Type"]

                    # either way we're adding the tag
                        # set won't like the lists, so we're making strings instead
                    if type(row["Type"]) == str: 
                        character_dict["all_gender_tags"].add(row["Type"]) 
                    elif row["Type"] == ["M", "M"]:
                        character_dict["all_gender_tags"].add("M/M")
                    elif row["Type"] == ["F","F"]:
                        character_dict["all_gender_tags"].add("F/F")
                    elif row["Type"] == ["F", "M"] or row["Type"] == ["M", "F"]:
                        character_dict["all_gender_tags"].add("F/M")
                    else: print(row["Type"])


    # we seem to have some ppl who are only in het ships & gen/other -> don't have a same sex value
        # but everyone has a latest value! :)
    # for fandom in rpf_dict:
    #     for character in rpf_dict[fandom]:
    #         rpf_dict[fandom][character]["all_gender_tags"] = sorted(list(rpf_dict[fandom][character]["all_gender_tags"]))
    #         if not rpf_dict[fandom][character]["most_recent_gender_tag"]:
    #             print("RPF:", rpf_dict[fandom][character], "\n")
    #         #if not rpf_dict[fandom][character]["most_recent_same_sex_tag"]:
    # for fandom in fic_dict:
    #     for character in fic_dict[fandom]:
    #         fic_dict[fandom][character]["all_gender_tags"] = sorted(list(fic_dict[fandom][character]["all_gender_tags"]))
    #         if not fic_dict[fandom][character]["most_recent_gender_tag"]:
    #             print("fic:", fic_dict[fandom][character], "\n")
    #         #if not fic_dict[fandom][character]["most_recent_same_sex_tag"]:
            
    output_dict = {
        "RPF": rpf_dict,
        "fictional": fic_dict
    }
    return output_dict


if __name__ == "__main__":
    gendered_dict = collect_gender_tags()
    filepath = "data/reference_and_test_files/assigning_demographic_info/assigning_gender_1_raw_tag_collection.json"
    with open(filepath, "w") as file_1:
        dump(gendered_dict, file_1, indent=4)