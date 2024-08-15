from src.fourth_stage_fixing_values_code.separate_names_into_parts import (
    gather_all_raw_characters, 
    remove_brackets, 
    separate_name_parts
)
from json import dump, load

def group_split_names_by_fandom(character_dict):
    """
    takes dict with split name values as output by separate_name_parts_func

    returns a dict with two keys ("RPF" and "fictional"), 
    each holding a nested dict value of the following format:
    {
        <fandom>: {
            {
                "split_name": <split name list from input dict value>,
                "og_name": <non-split name from input dict key>
            }, ...
        }, ...
    }
    """
    with open("data/reference_and_test_files/full_characters_per_fandom.json") as char_per_fandom_file:
        char_per_fandom_data = load(char_per_fandom_file)
    RPF_dict = char_per_fandom_data["RPF"]
    fic_dict = char_per_fandom_data["fictional"]

    # categorise names by fandoms, so we can make sure we're staying within each fandom
    split_names_by_fandoms = {
        "RPF": {},
        "fictional": {}
    }
    for fandom in RPF_dict:
        split_names_by_fandoms["RPF"][fandom] = []
        for character in RPF_dict[fandom]:
            if character in list(character_dict.keys()):
                split_name = character_dict[character]
                temp_dict = {
                    "split_name": split_name,
                    "og_name": character
                }
                split_names_by_fandoms["RPF"][fandom].append(temp_dict)
            else: print(character, "from", fandom, "is missing")
    for fandom in fic_dict:
        split_names_by_fandoms["fictional"][fandom] = []
        for character in fic_dict[fandom]:
            if character in list(character_dict.keys()):
                split_name = character_dict[character]
                temp_dict = {
                    "split_name": split_name,
                    "og_name": character
                }
                split_names_by_fandoms["fictional"][fandom].append(temp_dict)
            elif character == "Baze Malbus Rogue One: A":
                split_name = character_dict["Baze Malbus"]
                temp_dict = {
                    "split_name": split_name,
                    "og_name": character
                }
                split_names_by_fandoms["fictional"][fandom].append(temp_dict)
            elif character == "Jyn Erso Rogue One: A":
                split_name = character_dict["Jyn Erso"]
                temp_dict = {
                    "split_name": split_name,
                    "og_name": character
                }
                split_names_by_fandoms["fictional"][fandom].append(temp_dict)
            else: print(character, "from", fandom, "is missing")

    return split_names_by_fandoms

def categorise_names(char_by_fandom_dict):
    """
    takes a dict as put out by group_split_names_by_fandom

    returns a dict with two keys ("RPF" and "fictional"), 
    each holding a dict value of the following format: 
    {
        <fandom>: [
            {
                "given_name": None or str,
                "middle_name(s)": None or str,
                "surname": None or str,
                "alias": None or str,
                "nickname": None or str,
                "title (prefix)": None or str,
                "title (suffix)": None or str,
                "full_name": None or str,
                "fandom": str,
                "op_versions": [str, ...]
            }, ...
        ], ...
    ]
    """

    # setting up useful variables
    rpf_dict = char_by_fandom_dict["RPF"]
    fic_dict = char_by_fandom_dict["fictional"]
    all_rpf_fandoms = list(rpf_dict.keys())
    all_fic_fandoms = list(fic_dict.keys())

    # first layer (rpf vs fictional keys)
    categorised_characters = {
        "RPF": {},
        "fictional": {}
    }

    # second layer (fandom keys)
    for fandom in all_rpf_fandoms:
        categorised_characters["RPF"][fandom] = []
    for fandom in all_fic_fandoms:
        categorised_characters["fictional"][fandom] = []


    # for simple, two-name, obviously first-name-last-name ordered characters, 
    #   categorise them as "given name" and "surname" by order


    # these should all already be in the surname - given name order
    eastern_order_folks = [
        ['Jeon', 'Jungkook'],
        ['Park', 'Jimin'],
        ['Byun', 'Baekhyun'],
        ['Park', 'Chanyeol'],
        ['Boyang', 'Jin'],
        ['Yuzuru', 'Hanyu'],
        ['Xiao', 'Zhan'],
        ['Akanishi', 'Jin'],
        ['Kamenashi', 'Kazuya'],
        ['Lee', 'Jeno'],
        ['Na', 'Jaemin'],
        ['Kang', 'Seulgi'],
        ['Hwang', 'Hyunjin'],
        ['Choi', 'Soobin'],
        ['Choi', 'Yeonjun'],
        ['Asami', 'Sato'],
        ['Lin', 'Beifong'],
        ['Mikage', 'Reo'],
        ['Nagi', 'Seishirou'],
        ['Akutagawa', 'Ryuunosuke'],
        ['Dazai', 'Osamu'],
        ['Nakahara', 'Chuuya'],
        ['Nakajima', 'Atsushi'],
        ['Hinata', 'Hajime'],
        ['Komaeda', 'Nagito'],
        ['Oma', 'Kokichi'],
        ['Saihara', 'Shuichi'],
        ['Matsuoka', 'Rin'],
        ['Nanase', 'Haruka'],
        ['Tachibana', 'Makoto'],
        ['Kaedehara', 'Kazuha'],
        ['Kamisato', 'Ayato'],
        ['Xiao', 'Alatus'],
        ['Yae', 'Miko'],
        ['Akaashi', 'Keiji'],
        ['Bokuto', 'Koutarou'],
        ['Hinata', 'Shouyou'],
        ['Iwaizumi', 'Hajime'],
        ['Kageyama', 'Tobio'],
        ['Kozume', 'Kenma'],
        ['Kuroo', 'Tetsurou'],
        ['Miya', 'Atsumu'],
        ['Oikawa', 'Tooru'],
        ['Sakusa', 'Kiyoomi'],
        ['Sawamura', 'Daichi'],
        ['Shimizu', 'Kiyoko'],
        ['Sugawara', 'Koushi'],
        ['Tsukishima', 'Kei'],
        ['Yachi', 'Hitoka'],
        ['Yamaguchi', 'Tadashi'],
        ['Aoyagi', 'Touya'],
        ['Kamishiro', 'Rui'],
        ['Shinonome', 'Akito'],
        ['Tenma', 'Tsukasa'],
        ['Huā', 'Chéng'],
        ['Xiè', 'Lián'],
        ['Kakyoin', 'Noriaki'],
        ['Kujo', 'Jotaro'],
        ['Getou', 'Suguru'],
        ['Gojo', 'Satoru'],
        ['Kiryuuin', 'Satsuki'],
        ['Matoi', 'Ryuuko'],
        ['Ayase', 'Eli'], # love live, already in eastern order, can stay that way
        ['Nishikino', 'Maki'],
        ['Toujou', 'Nozomi'],
        ['Yazawa', 'Nico'],
        ['Asui', 'Tsuyu'],
        ['Bakugou', 'Katsuki'],
        ['Jirou', 'Kyouka'],
        ['Kaminari', 'Denki'],
        ['Kirishima', 'Eijirou'],
        ['Midoriya', 'Izuku'],
        ['Shinsou', 'Hitoshi'],
        ['Todoroki', 'Shouto'],
        ['Uraraka', 'Ochako'],
        ['Yaoyorozu', 'Momo'],
        ['Haruno', 'Sakura'],
        ['Hatake', 'Kakashi'],
        ['Uchiha', 'Sasuke'],
        ['Umino', 'Iruka'],
        ['Uzumaki', 'Naruto'],
        ['Yamanaka', 'Ino'],
        ['Liu', 'Chenxiang'],
        ['Kim', 'Dokja'],
        ['Yoo', 'Joonghyuk'],
        ['Roronoa', 'Zoro'],
        ['Vinsmoke', 'Sanji'],
        ['Hanzo', 'Shimada'],
        ['Akechi', 'Goro'],
        ['Amagi', 'Yukiko'],
        ['Satonaka', 'Chie'],
        ['Kaiou', 'Michiru'],
        ['Tenoh', 'Haruka'],
        ['Akemi', 'Homura'],
        ['Kaname', 'Madoka'],
        ['Miki', 'Sayaka'],
        ['Sakura', 'Kyouko'],
        ['Hasegawa', 'Langa'],
        ['Kyan', 'Reki'],
        ['Hyakuya', 'Mikaela'],
        ['Hyakuya', 'Yuuichirou'], # seraph of the end, yuuichirou is given name, eastern order
        ['Zhèng', 'Yúnlóng'],
        ['Kira', 'Yukimura'],
        ['Nagachika', 'Hideyoshi'],
        ['Sasaki', 'Haise'],
        ['Penelope', 'Park'], # is this one? ditto as above
        ['Wen', 'Kexing'],
        ['Zhou', 'Zishu'],
        ['Katsuki', 'Yuuri'],
    ]
    non_double_names = [
        ['Ryan', 'GoodTimesWithScar'],
        ['Princess', 'Bubblegum'],
        ['Kya', 'II'],
        ['Ymir', 'of the 104th'],
        ['Upgraded Connor', 'RK900'],
        ['My Unit', 'Byleth'], # this is fire emblem protag/pc
        ['Red Riding Hood', 'Ruby'],
        ['Lapis', 'Lazuli'],
        ['Rose Quartz', 'Pink Diamond'],
        ['Dream', 'of the Endless'],
        ['Jaskier', 'Dandelion'],
        ['Vash', 'the Stampede']
    ]
    single_first_names = [
        'Adam', 
        'Adora', 
        'Alistair', 
        'Allura', 
        'Alphys',  
        'Angel',
        'Anna', 
        'Anya', 
        'Arthur', 
        'Astra', 
        'Aurora', 
        'Axel', 
        'Aziraphale', 
        'Azula',  
        'Belle', 
        'Bo', 
        'Caitlyn', 
        'Calliope', 
        'Carlos', 
        'Castiel', 
        'Catra', 
        'Chloe', 
        'Clara', 
        'Connor', 
        'Costia', 
        'Dina', 
        'Donatello', 
        'Ellie', 
        'Elsa', 
        'Emily', 
        'Evie', 
        'Fenris', 
        'Finn', 
        'Frank', 
        'Fíli', 
        'Gabriel', 
        'Gabrielle', 
        'Gerard', 
        'Gilda', 
        'Glimmer', 
        'Guinevere', 
        'Gwen', 
        'Isabela', 
        'Jean', 
        'Joel', 
        'Katara', 
        'Keith', 
        'Korra', 
        'Kíli', 
        'Lance', 
        'Lauren', 
        'Leliana', 
        'Leonardo', 
        'Levi', 
        'Lexa',
        'Lisa', 
        'Loki', 
        'Lucifer', 
        'Mal', 
        'Maleficent', 
        'Marceline', 
        'Merlin', 
        'Michelangelo', 
        'Morgana', 
        'Morgause', 
        'Mulan',
        'Penny', 
        'Perfuma', 
        'Raphael', 
        'Rey', 
        'Scorpia', 
        'Sera', 
        'Shego', 
        'Shiro', 
        'Skye', 
        'Sokka', 
        'Solas',  
        'Thoma', 
        'Thor', 
        'Undyne', 
        'Vi', 
        'Viktor', 
        'Warden', 
        'Wilhelm', 
        'Willie', 
        'Xena', 
        'Yasha', 
        'Ymir', 
        'Zuko',
        'Jayce',
        'Beauregard',
        'Albedo',
        'Alhaitham',
        'Beidou',
        'Cyno',
        'Diluc',
        'Ganyu',
        'Kaeya',
        'Kaveh',
        'Keqing',
        'Ningguang',
        'Scaramouche',
        'Tighnari',
        'Venti',
        'Zhongli',
        'Methos',
        'Roxas',
        'Tamsin',
        'Genos',
        'Saitama',
        'Trini',
        'Agron',
        'Nasir',
        'Amethyst',
        'Garnet',
        'Jasper',
        'Lapis Lazuli',
        'Pearl',
        'Peridot',
        'Rose Quartz',
        'Ruby',
        'Sapphire',
        'Sans',
    ]
    single_aliases = [
        'Dabi',
        'GeorgeNotFound',
        'Q',
        'Ranboo',
        'Sapnap',
        'Technoblade',
        'TommyInnit',
        'Lightning',
        'America',
        'England',
        'Root',
        'Ayanga',
    ]
    single_nicknames = [
        'Spike',
        'Kon-El',
        'Vaggie',
        'Spock',
    ] # I'm including alien names where other names exist here, eg kryptonians
    player_characters = [
        'Hawke',
        'Inquisitor',
        'Traveler',
        'Shepard',
        'Persona 5 Protagonist',
    ]
    single_surnames = [
        'Crowley',
        'Eames',
        'Courfeyrac',
        'Enjolras',
        'Grantaire',
        'Javert',
        'Uzumaki',
        'Lestrade',
        'Lincoln',
    ]

    


    for category in ["RPF", "fictional"]:
        current_dict = char_by_fandom_dict[category]
        for fandom in current_dict:
            for name in current_dict[fandom]: # fandom key's value is a list of dicts
                default_dict = {
                    "given_name": None,
                    "middle_name(s)": None,
                    "surname": None,
                    "alias": None,
                    "nickname": None,
                    "title (prefix)": None,
                    "title (suffix)": None,
                    "full_name": None,
                    "fandom": fandom,
                    "op_versions": []
                }
                split_name = name["split_name"]
                if len(split_name) == 2 \
                    and split_name not in non_double_names \
                        and "Doctor" not in split_name: 
                    # if there is only two names
                    if split_name in eastern_order_folks: 
                        # if they're already in eastern order & should stay that way
                        surname = split_name[0]
                        given_name = split_name[1]
                        order = "E"
                    elif split_name == ['Lee', 'Felix']: 
                        # man's australian, if we have mark in western order, felix should be too
                        surname = split_name[0]
                        given_name = split_name[1]
                        order = "W"
                    else: 
                        # they're in western order
                        given_name = split_name[0]
                        surname = split_name[1]
                        order = "W"
                elif len(split_name) == 1 \
                    and split_name[0] != "Reader" \
                        and "Doctor" not in split_name[0] \
                            and split_name[0] not in player_characters:
                    # if there's only one name part
                    if split_name[0] in single_first_names:
                        given_name = split_name[0]
                    elif split_name[0] in single_aliases:
                        alias = split_name[0]
                    elif split_name[0] in single_nicknames:
                        nickname = split_name[0]
                    elif split_name[0] in single_surnames:
                        surname = split_name[0]
                    elif "Venom" in split_name[0]:
                        alias = "Venom"
                    else: 
                       print(f"'{split_name[0]}', {category}") 
                    #    # there's a buncha stuff to look up & possibly add to first names & aliases lists
                    








    # for category in split_names_by_fandoms: # aka RPF or fic
    #     for fandom in split_names_by_fandoms[category]:
    #         for name in split_names_by_fandoms[category][fandom]:
    #             if len(name["split_name"]) == 1:
    #                 print(f"({name['split_name']}, '{fandom}'),")
    #                 single_item_name = name["split_name"]
    #                 if (single_item_name, fandom) in 

                # if len(name["split_name"]) == 2 and "Lee" in name["split_name"]: #example, needs more
                #     given_name = name["split_name"][1]
                #     surname = name["split_name"][0]
                #     order = "E"
                    
                # if len(name["split_name"]) == 2:
                #     given_name = name["split_name"][0]
                #     surname = name["split_name"][1]
                #     order = "W"
                #     print(name["split_name"])
                # # elif len(name["split_name"]) == 1: 
                # #     print(f"{fandom}: {name}")
                # temp_dict = {
                #     "given_name" : given_name,
                #     "surname": surname,
                #     "order": order
                # }


    # currently not correctly categorised: (as far as I can tell)
    """


    (this list may not be exhaustive rip)
    q: do we make all anime characters follow eastern order or only the ones w non-western names?
        -I say only non-western ones, 
        bc I think they tend to also use western order for western last-name ppl, idk
        -> check wikis for cases where unsure??

    ['Anne', 'Boonchuy'] # thai american, protag of amphibia, western order
    ['Marcy', 'Wu'] # taiwanese, also amphibia, also western order
    ['Levi', 'Ackerman'] # ackermans are western order on the wiki
    ['Mikasa', 'Ackerman']
    ['Kanaya', 'Maryam'] # fucking homestuck
    ['Karkat', 'Vantas']
    ['Meenah', 'Peixes']
    ['Tavros', 'Nitram']
    ['Terezi', 'Pyrope']
    ['Heero', 'Yuy'] # gundam, hiiro yui, in that order, I'm gonna assume it's western order 
                     # bc neither of his parents share his last name???? 
                     # and both of em have western last names so uhh
    ['Hikaru', 'Sulu'] # order is fine like this, just call it western, 
                       # star trek don't care abt eastern order lmao
    ['Quynh', 'Noriko'] # old guard -> noriko is og, quynh is movie version, both single names
    ['Tori', 'Vega'] # victoria 'tori' vega from victorious
    ['Lucy', 'Chen'] # the rookie protag, western order
    ['Ty', 'Lee'] # avatar, we'll call it western order
    ['Lee', 'Adama'] # Commander Leland "Lee" Joseph Adama from battlestar galactica

        ['Mark', 'Lee']    ['Lee', 'Felix'] how do we handle these two?
    """



    # for eastern names w possibly/likely different order, 
    #   look up which is given name if unsure

    # have a new value that indicates western or eastern name order
    #   eg "W" for first name - last name, "E" for surname - given name, 
    #   and then we can maybe have a null or n/a for single names, etc
    # -> that way we can easily concat the right way around later! :)

    # we should also include titles as a separate value where relevant 
    #   (eg "Mr Gold", various Captains, etc)

    # anything with '' around it gets categorised as nickname/alias for now

    # look for obvious doubles & go with most complete version

    # look up missing bits & add them 
    #   (eg last names, aliases, etc that I know exist, 
    #   look for middle names where initials are present)

    # look up any characters you don't know to make sure

    # we're not fucking with translations, I've decided, 
    #   so remove em where present (eg geralt of rivia)

    # include (clean) fandom value & prior name versions for each character dict
    
    # return resulting collection
    pass



if __name__ == "__main__":
    all_unformatted_characters = gather_all_raw_characters()
    bracketless_characters = remove_brackets(all_unformatted_characters)
    split_name_characters = separate_name_parts(bracketless_characters)
    grouped_by_fandom = group_split_names_by_fandom(split_name_characters)

    categorised_names = categorise_names(grouped_by_fandom)
    # character_dict = {"categorised_name_characters": categorised_names}
    # with open("data/reference_and_test_files/cleaned_characters_list_3_categorised_names.json", "w") as file:
    #     dump(character_dict, file, indent=4)