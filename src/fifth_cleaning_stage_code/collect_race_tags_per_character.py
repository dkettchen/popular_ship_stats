from json import load, dump

def collect_race_tags():
    """
    reads from fourth_clean_up_data files and assigning_gender_2_assigning_gender

    returns a nested dict with "RPF" and "fictional" keys, ordered by fandoms and characters, with 
    new race tag keys (latest tag, latest same race tag, all tags) added to the versions from gender_2
    """
    
    all_ordered_paths = { 
        2023: [
            'data/fourth_clean_up_data/ao3_2023/raw_ao3_2023_data.json', 
            'data/fourth_clean_up_data/ao3_2023/raw_ao3_2023_overall_ranking.json',
            'data/fourth_clean_up_data/ao3_2023/raw_ao3_2023_femslash_ranking.json', 
        ],
        2022: [
            'data/fourth_clean_up_data/ao3_2022/raw_ao3_2022_data.json', 
            'data/fourth_clean_up_data/ao3_2022/raw_ao3_2022_overall_ranking.json',
            'data/fourth_clean_up_data/ao3_2022/raw_ao3_2022_femslash_ranking.json', 
        ],
        2021: [
            'data/fourth_clean_up_data/ao3_2021/raw_ao3_2021_femslash_ranking.json', 
            'data/fourth_clean_up_data/ao3_2021/raw_ao3_2021_data.json', 
            'data/fourth_clean_up_data/ao3_2021/raw_ao3_2021_overall_ranking.json',
        ],
        2020: [
            'data/fourth_clean_up_data/ao3_2020/raw_ao3_2020_data.json',  
            'data/fourth_clean_up_data/ao3_2020/raw_ao3_2020_overall_ranking.json',
            'data/fourth_clean_up_data/ao3_2020/raw_ao3_2020_femslash_ranking.json',
        ], 
        2019: [
            'data/fourth_clean_up_data/ao3_2019/raw_ao3_2017-2019_data.json', 
            'data/fourth_clean_up_data/ao3_2019/raw_ao3_2019_overall_ranking.json',
            'data/fourth_clean_up_data/ao3_2019/raw_ao3_2019_femslash_ranking.json', 
        ], 
        2017: [
            'data/fourth_clean_up_data/ao3_2017/raw_ao3_2017_data.json', 
            'data/fourth_clean_up_data/ao3_2017/raw_ao3_2017_overall_ranking.json',
            'data/fourth_clean_up_data/ao3_2017/raw_ao3_2017_femslash_ranking.json', 
        ], 
        2016: [
            'data/fourth_clean_up_data/ao3_2016/raw_ao3_2016_data.json', 
            'data/fourth_clean_up_data/ao3_2016/raw_ao3_2016_overall_ranking.json',
            'data/fourth_clean_up_data/ao3_2016/raw_ao3_2016_femslash_ranking.json', 
        ], 
        2015: [
            'data/fourth_clean_up_data/ao3_2015/raw_ao3_2015_overall_ranking.json',
            'data/fourth_clean_up_data/ao3_2015/raw_ao3_2015_femslash_ranking.json', 
        ], 
        2014: [
            'data/fourth_clean_up_data/ao3_2014/raw_ao3_2014_overall_ranking.json',
            'data/fourth_clean_up_data/ao3_2014/raw_ao3_2014_femslash_ranking.json', 
        ], 
        2013: [
            'data/fourth_clean_up_data/ao3_2013/raw_ao3_2013_overall_ranking.json',
            ],
    }

    char_path = "data/reference_and_test_files/assigning_demographic_info/assigning_gender_2_assigning_gender.json"
    with open(char_path, "r") as char_file:
        all_characters = load(char_file)
        # dict w rpf & fictional keys, fandom keys in those, char name keys in those, lotsa name bits etc in there

    rpf_dict = all_characters["RPF"] # we don't need to deepcopy this bc we're reading from the file
    fic_dict = all_characters["fictional"] # -> it can be mutated, cause the file won't be changed
    # {<fandom>:{<char>:{<stuff>}}}

    untagged_white_characters = [
        'Aaron Hotchner', 
        "Abigail Beethoven 'Abby' Sciuto",
        'Agron', 
        'Alex Kingston', 
        'Alison Hendrix', 
        'Angel', 
        'Anna Milton', 
        'Aurora', 
        'Bella Swan', 
        'Beth Childs', 
        "William 'Billy' Kaplan | Wiccan",
        'Brad Colbert', 
        'Bradley James', 
        'Bruce Wayne | Batman', 
        'Colin Morgan', 
        "Connor 'Kon-El' Kent | Superboy", 
        'Courfeyrac', 
        'Chris Pine', 
        'David Karofsky', 
        'David Starsky', 
        'Duncan MacLeod', # actor is half italian but character is scottish
        'Duo Maxwell', 
        'Edward Cullen', 
        'Edward Elric', 
        'Elizabeth Weir', 
        'Emily Fitch', 
        'Erica Davidson',
        'Finn Hudson', 
        'Frodo Baggins', 
        'Gene Hunt', 
        'Harold Finch', 
        'Heero Yuy', # his mom's name is Aoi, but I can't find info on or pics of her, 
                     # so we're going with the remaining white coding
        'Javert', 
        'Jean Prouvaire', 
        'Jean Valjean', 
        'John Reese', 
        'Kara Thrace', 
        'Kate Beckett', 
        "Kenneth 'Ken' Hutchinson",
        'Kim Possible', 
        'Laura Roslin', 
        "Lee 'Apollo' Adama",
        'Lightning', 
        'Lizzie Bennet', 
        'Lois Lane', 
        'Maleficent', 
        'Marius Pontmercy', 
        'Matt Smith', 
        'Methos', # char doesn't remember where he's from but actor is white
        'Naomi Campbell', 
        'Nate Fick', 
        'Neal Caffrey', 
        'Noah Puckerman', 
        'Pavel Chekov', 
        "Penny", # she wasn't married to leonard yet here I think, so no last name
        'Peter Burke', 
        'Qui-Gon Jinn', 
        'Richard Castle', 
        'Ruby', 
        'Ryan Ross', 
        'Sam Gamgee', 
        'Sam Tyler', 
        'Sandor Clegane | The Hound', 
        'Sauli Koskinen', 
        'Sean Bean', 
        'Sebastian Smythe', 
        'Sheldon Cooper', 
        'Shego', 
        'Spencer Reid', 
        'Spencer Smith', 
        'Tamsin', 
        'The Doctor', 
        'The Ninth Doctor', 
        'Viggo Mortensen', 
        'William Darcy', 
        'Winry Rockbell', 
        "Elizabeth Burke, née Mitchell", # will retag these later
        'Brendon Urie', # will retag these later
    ]
    untagged_asian_character = [
        'Amagi Yukiko', 
        'Miki Sayaka',
        'Oerba-Yun Fang', 
        'Sakura Kyouko', 
        'Satonaka Chie', 
        'Kiryuuin Satsuki', 
        'Matoi Ryuuko', 
        'Hatake Kakashi', 
        'Umino Iruka', 
        'Akanishi Jin', 
        'Kamenashi Kazuya', 
        'Hikaru Sulu', 
    ]
    untagged_latin_characters = [
        'Gilda', 
        'Franky Doyle', 
        'Zachary Quinto', # italian which acc to oxford dict & my european understanding is latin
        'William Adama', 
    ]
    untagged_NH_characters = [
        'Calliope', 
        'Gamzee Makara', 
        'Garrus Vakarian', 
        'Tavros Nitram', 
        'Teddy Altman | Hulkling', 
        'Eridan Ampora', 
        'Sollux Captor', 
    ]
    untagged_other_characters = {
        'Ziva David': "MENA",
        'Clara': "Unknown",
        "Harriet 'Harry' Watson": "Unknown",
        'Piper McLean': "Indig",
        'Nasir': "MENA", 
        'Derek Morgan': "Black", 
        "Nicholas 'Dick' Grayson | Robin/Nightwing": "Romani", 
    }
    untagged_amb_characters = [ # dude idk
        'Roy Mustang',
        'Axel',
        'Roxas',
    ]

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
                    if "most_recent_race_tag" not in character_dict.keys():
                        character_dict["most_recent_race_tag"] = None
                    if "most_recent_same_race_tag" not in character_dict.keys():
                        character_dict["most_recent_same_race_tag"] = None
                    if "all_race_tags" not in character_dict.keys():
                        character_dict["all_race_tags"] = set()

                    if row["Race"] != [None, None]: # if there is a race tag in the row (cause some sets don't have one)
                        # if we don't have a tag yet
                        if not character_dict["most_recent_race_tag"]: 
                            character_dict["most_recent_race_tag"] = row["Race"]

                        # if we don't have a same race tag yet, and it is a same race tag
                        if not character_dict["most_recent_same_race_tag"] \
                        and row["Race"][0] == row["Race"][1]:  
                            character_dict["most_recent_same_race_tag"] = row["Race"]

                        if type(row["Race"]) == list:
                            tag_string = row["Race"][0] + "/" + row["Race"][1]
                        elif type(row["Race"]) == str:
                            tag_string = row["Race"]
                        character_dict["all_race_tags"].add(tag_string)
                    
                    elif not character_dict["most_recent_race_tag"]: # if it still hasn't been assigned
                        if character in untagged_white_characters:
                            character_dict["most_recent_race_tag"] = "White"
                        elif character in untagged_asian_character:
                            character_dict["most_recent_race_tag"] = "Asian"
                        elif character in untagged_latin_characters:
                            character_dict["most_recent_race_tag"] = "Latino"
                        elif character in untagged_NH_characters:
                            character_dict["most_recent_race_tag"] = "N.H."
                        elif character in untagged_other_characters:
                            character_dict["most_recent_race_tag"] = untagged_other_characters[character]
                        elif character in untagged_amb_characters:
                            character_dict["most_recent_race_tag"] = "Ambig"

    for fandom in rpf_dict:
        for character in rpf_dict[fandom]:
            rpf_dict[fandom][character]["all_race_tags"] = sorted(list(rpf_dict[fandom][character]["all_race_tags"]))
    for fandom in fic_dict:
        for character in fic_dict[fandom]:
            fic_dict[fandom][character]["all_race_tags"] = sorted(list(fic_dict[fandom][character]["all_race_tags"]))
            
    output_dict = {
        "RPF": rpf_dict,
        "fictional": fic_dict
    }
    return output_dict
    

if __name__ == "__main__":
    collected_race_tags = collect_race_tags()
    filepath = "data/reference_and_test_files/assigning_demographic_info/assigning_race_3_raw_tag_collection.json"
    with open(filepath, "w") as file_3:
        dump(collected_race_tags, file_3, indent=4)