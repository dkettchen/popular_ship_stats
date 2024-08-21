from src.fourth_stage_fixing_values_code.separate_names_into_parts import (
    gather_all_raw_characters, 
    remove_brackets, 
    separate_name_parts
)
from src.util_functions.add_full_name import add_full_name
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
    with open("data/reference_and_test_files/cleaning_characters/full_characters_per_fandom.json") as char_per_fandom_file:
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
                "given_name": str | None,
                "middle_name": str | None,
                "maiden_name": str | None,
                "surname": str | None,
                "alias": str | None,
                "nickname": str | None,
                "title (prefix)": str | None,
                "title (suffix)": str | None,
                "name_order": str | None,
                "full_name": str,
                "fandom": str,
                "op_versions": [str]
            }, ...
        ], ...
    }

    duplicates have not yet been eliminated and relevant names have not been completed
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

    # setting up so many name categories to use in a bit:

    # various lengths
    player_characters = [
        'Hawke',
        'Inquisitor',
        'Traveler',
        'Shepard',
        "Warden",
        'Persona 5 Protagonist',
        ['My Unit', 'Byleth'],
    ]

    # single names
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
        "Iron Bull",
        "Wilbur Soot",
    ]
    single_nicknames = [
        'Spike',
        'Kon-El',
        'Vaggie',
        'Spock',
    ] # I'm including alien names where other names exist here, eg kryptonians
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

    # 2 part names
    eastern_order_folks = [ # these should all already be in the surname - given name order
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
        ['Vash', 'the Stampede'],
        ["Clay", "Dream"],
        ["Madame", "Vastra"],
        ["Alexis", "Quackity"],
        ["Charles", "Grian"],
        ['Xiao', 'Alatus'],
        ["Tartaglia", "Childe"],
    ]
    given_suffix = [
        ['Ymir', 'of the 104th'],
        ['Dream', 'of the Endless'],
        ['Vash', 'the Stampede'],
        ['Kya', 'II'],
    ]
    given_alias = [
        ['Ryan', 'GoodTimesWithScar'],
        ['Jaskier', 'Dandelion'],
        ['Rose Quartz', 'Pink Diamond'],
        ["Clay", "Dream"],
        ["Alexis", "Quackity"],
        ["Charles", "Grian"],
        ["Tartaglia", "Childe"],
    ]

    # 3 part names
    surname_given_alias_E = [
        ['Jung', 'Hoseok', 'J-Hope'],
        ['Kim', 'Namjoon', 'Rap Monster/RM'],
        ['Kim', 'Seokjin', 'Jin'],
        ['Kim', 'Taehyung', 'V'],
        ['Min', 'Yoongi', 'Suga'],
        ['Sun', 'Wukong', 'Monkey King'], # is this given-sur in the right order already?
        ['Aizawa', 'Shouta', 'Eraserhead'],
        ['Takami', 'Keigo', 'Hawks'],
        ['Yagi', 'Toshinori', 'All Might'],
        ['Yamada', 'Hizashi', 'Present Mic'],
        ['Sakurayashiki', 'Kaoru', 'Cherry Blossom'],
        ['Lee', 'Donghyuck', 'Haechan'],
        ['Bae', 'Joohyun', 'Irene'],
        ['Han', 'Jisung', 'Han'],
        ['Do', 'Kyungsoo', 'D.O'],
        ['Kim', 'Jongin', 'Kai'],
        ['Nanjo', 'Kojiro', 'Joe'],
    ]
    first_last_alias_W = [
        ['Phil', 'Watson', 'Philza'],
        ['Toby', 'Smith', 'Tubbo'],
        ['Tom', 'Riddle', 'Voldemort'],
        ['Adrien', 'Agreste', 'Chat Noir'],
        ['Marinette', 'Dupain-Cheng', 'Ladybug'],
    ]
    first_nick_last_W = [
        ['Evan', "'Buck'", 'Buckley'],
        ['Aemond', "'One-Eye'", 'Targaryen'],
        ['John', "'Soap'", 'MacTavish'],
        ['Simon', "'Ghost'", 'Riley'],
        ['Jennifer', "'JJ'", 'Jareau'],
        ['Samantha', "'Sam'", 'Arias'],
        ['Calliope', "'Callie'", 'Torres'],
        ['Elizabeth', "'Eliza'", 'Schuyler'],
        ['Danny', "'Danno'", 'Williams'],
        ['Charles', "'Charlie'", 'Spring'],
        ['Nicholas', "'Nick'", 'Nelson'],
        ['Gary', "'Eggsy'", 'Unwin'],
        ['Maxine', "'Max'", 'Caulfield'],
        ['Atsuko', "'Akko'", 'Kagari'],
        ['James', "'Bucky'", 'Barnes'],
        ['Leonard', "'Bones'", 'McCoy'],
        ['Jim', "'Chief'", 'Hopper'],
        ['Maxine', "'Max'", 'Mayfield'],
        ['Bradley', "'Rooster'", 'Bradshaw'], # what fandom are these ones from?
        ['Jake', "'Hangman'", 'Seresin'], #
        ['Pete', "'Maverick'", 'Mitchell'], #
        ['Tom', "'Iceman'", 'Kazansky'], # alias
        ['Helena', "'H. G.'", 'Wells'],
    ]
    first_middle_last_W = [
        ['Brittany', 'S.', 'Pierce'],
        ['Mobius', 'M.', 'Mobius'],
        ['James', 'T.', 'Kirk'],
        ['Nicholas', 'D.', 'Wolfwood'],
        ['Brooke', 'Lynn', 'Hytes'],
        ['Dimitri', 'Alexandre', 'Blaiddyd'],
        ['Felix', 'Hugo', 'Fraldarius'],
        ['Sylvain', 'Jose', 'Gautier'],
        ['Brenda', 'Leigh', 'Johnson'],
        ['Clara', 'Oswin', 'Oswald'],
        ['Kinn', 'Anakinn', 'Theerapanyakun'],
        ['Vegas', 'Kornwit', 'Theerapanyakun'],
        ['Pete', 'Phongsakorn', 'Saengtham'],
        ['Porchay', 'Pichaya', 'Kittisawat'],
        ['Porsche', 'Pachara', 'Kittisawat'],
        ['Even', 'Bech', 'Næsheim'],
    ]
    alias_first_last_W = [
        ['Skye', 'Daisy', 'Johnson'], # iirc -> look up
        ['Evil Queen', 'Regina', 'Mills'],
        ['Blackbeard', 'Edward', 'Teach'],
        ['Reaper', 'Gabriel', 'Reyes'],
        ['Soldier: 76', 'Jack', 'Morrison'],
        ['Widowmaker', 'Amélie', 'Lacroix'],
        ['Root', 'Samantha', 'Groves'],
        ['The Darkling', 'Aleksander', 'Morozova'],
        ['Eleven', 'Jane', 'Hopper'],
        ['Anxiety', 'Virgil', 'Sanders'],
        ['Logic', 'Logan', 'Sanders'],
        ['Morality', 'Patton', 'Sanders'],
    ]
    first_maiden_last_W = [
        ['Kristin', 'Rosales', 'Watson'],
        ['Bellatrix', 'Black', 'Lestrange'],
        ['Lily', 'Evans', 'Potter'],
    ]
    nick_first_last_W = [
        ['Andy', 'Andromache', 'of Scythia'],
        ['Joe', 'Yusuf', 'Al-Kaysani'],
    ]
    nick_sur_given_E = [
        ['Mikey', 'Sano', 'Manjirou'],
        ['Takemitchy', 'Hanagaki', 'Takemichi'],
    ]
    first_alias_sur_W = [
        ['Angela', "'Mercy'", 'Ziegler'], # these are more like aliases
        ['Fareeha', "'Pharah'", 'Amari'], #
        ['Lena', "'Tracer'", 'Oxton'], #
    ]

    # 4 part names
    sur_given_alias_alias = [
        ['Lo', 'Hon-ting', 'Anson', 'Lo'], # sur given alias alias (concat) E
        ['Lui', 'Cheuk-on', 'Edan', 'Lui'], # ""
        ['Lee', 'Minho', 'Lee', 'Know'], # "" is minho stray kids
    ]
    sur_given_courtesy = [
        ['Jiāng', 'Chéng', 'Jiāng', 'Wǎnyín'], # sur given sur given, the latter is courtesy name E
        ['Lán', 'Huàn', 'Lán', 'Xīchén'], # ""
        ['Lán', 'Zhàn', 'Lán', 'Wàngjī'], # ""
        ['Wèi', 'Yīng', 'Wèi', 'Wúxiàn'], # ""
    ]

    for category in ["RPF", "fictional"]:
        current_dict = char_by_fandom_dict[category]
        for fandom in current_dict:
            for name in current_dict[fandom]: # fandom key's value is a list of dicts

                split_name = name["split_name"]
                given_name = None
                middle_name = None
                maiden_name = None
                surname = None
                alias = None
                nickname = None
                title_prefix = None
                title_suffix = None
                order = None
                og_name = name["og_name"]
                
                if len(split_name) == 2 \
                and split_name not in player_characters:
                    if split_name not in non_double_names: 
                        # if there is only two names
                        if split_name in eastern_order_folks: 
                            # if they're already in eastern order & should stay that way
                            surname = split_name[0]
                            given_name = split_name[1]
                            order = "E"
                        elif split_name in [
                            ['Lee', 'Felix'], # man's australian, if we have mark in western order, felix should be too
                            ["Vinsmoke", "Sanji"], # man's literally white
                        ]:
                            surname = split_name[0]
                            given_name = split_name[1]
                            order = "W"
                        elif split_name == ["Hanzo","Shimada"]:
                            surname = split_name[1]
                            given_name = split_name[0]
                            order = "E"
                        else: 
                            # they're in western order
                            given_name = split_name[0]
                            surname = split_name[1]
                            order = "W"
                    elif split_name in given_alias:
                        given_name = split_name[0]
                        alias = split_name[1]
                    elif split_name in given_suffix:
                        given_name = split_name[0]
                        title_suffix = split_name[1]
                    elif split_name == ['Princess', 'Bubblegum']:
                        title_prefix = split_name[0]
                        given_name = split_name[1]
                        order = "W"
                    elif split_name == ['Red Riding Hood', 'Ruby']:
                        alias = split_name[0]
                        given_name = split_name[1]
                    elif split_name == ['Upgraded Connor', 'RK900']: # add (RK800) to regular connor
                        given_name = "Connor (RK900)" 
                    elif split_name == ["Madame", "Vastra"]:
                        title_prefix = split_name[0]
                        surname = split_name[1]
                    elif split_name == ['Xiao', 'Alatus']:
                        alias = split_name[0]
                        given_name = split_name[1]

                elif len(split_name) == 1 \
                and split_name[0] != "Reader" \
                and "Doctor" not in split_name[0] \
                and split_name[0] not in player_characters:
                    # if there's only one name part
                    if split_name[0] == "Connor" and "Detroit" in fandom:
                        given_name = "Connor (RK800)"
                    elif split_name[0] in single_first_names:
                        given_name = split_name[0]
                    elif split_name[0] in single_aliases:
                        alias = split_name[0]
                    elif split_name[0] in single_nicknames:
                        nickname = split_name[0]
                    elif split_name[0] in single_surnames:
                        surname = split_name[0]
                    elif "Venom" in split_name[0]:
                        alias = "Venom (Symbiote)"
                    

                elif len(split_name) == 3:
                    if split_name in surname_given_alias_E:
                        surname = split_name[0]
                        given_name = split_name[1]
                        alias = split_name[2]
                        order = "E"
                    elif split_name in first_last_alias_W:
                        given_name = split_name[0]
                        surname = split_name[1]
                        alias = split_name[2]
                        order = "W"
                    elif split_name in first_nick_last_W:
                        given_name = split_name[0]
                        nickname = split_name[1]
                        surname = split_name[2]
                        order = "W"
                    elif split_name in first_middle_last_W:
                        given_name = split_name[0]
                        middle_name = split_name[1]
                        surname = split_name[2]
                        order = "W"
                    elif split_name in alias_first_last_W:
                        alias = split_name[0]
                        given_name = split_name[1]
                        surname = split_name[2]
                        order = "W"
                    elif split_name in first_maiden_last_W:
                        given_name = split_name[0]
                        maiden_name = split_name[1] 
                        surname = split_name[2]
                        order = "W"
                    elif split_name in nick_first_last_W:
                        nickname = split_name[0]
                        given_name = split_name[1]
                        surname = split_name[2]
                        order = "W"
                    elif split_name in nick_sur_given_E:
                        nickname = split_name[0]
                        surname = split_name[1]
                        given_name = split_name[2]
                        order = "E"
                    elif split_name in first_alias_sur_W:
                        given_name = split_name[0]
                        alias = split_name[1][1:-1]
                        surname = split_name[2]
                        order = "W"

                    elif split_name == ['Xiao', 'Zhan', 'Sean']:
                        surname = split_name[0]
                        given_name = split_name[1]
                        alias = split_name[2] + " " + split_name[0] # Sean Xiao
                        order = "E"
                    elif split_name == ['Original', 'Percival', 'Graves']: # what is this original business, first, last, W
                        given_name = split_name[1]
                        surname = split_name[2]
                        order = "W"
                    elif split_name == ['Barty', 'Crouch', 'Jr.']: # first, last, junior suffix, W
                        given_name = split_name[0]
                        surname = split_name[1]
                        title_suffix = split_name[2]
                        order = "W"
                    elif split_name == ['Rumpelstiltskin', 'Mr.', 'Gold']: # alias, title, surname W
                        alias = split_name[0]
                        title_prefix = split_name[1]
                        surname = split_name[2]
                        order = "W"
                    elif split_name == ['Dabi', 'Todoroki', 'Touya']: # alias, surname, given E
                        alias = split_name[0]
                        surname = split_name[1]
                        given_name = split_name[2]
                        order = "W"
                    elif split_name == ['Nicky', 'Nicolò', 'di Genova']: # assuming nick first last W
                        nickname = split_name[0]
                        given_name = split_name[1]
                        surname = split_name[2]
                        order = "W"
                    elif split_name == ['Wang', 'Yi', 'Bo']: # sur given given, E
                        surname = split_name[0]
                        given_name = split_name[1] + " " + split_name[2]
                        order = "E"
                    elif split_name == ['Yang', 'Xiao', 'Long']: # given, sur sur E
                        given_name = split_name[0]
                        surname = split_name[1] + " " + split_name[2]
                        order = "E"
                    elif split_name == ['Oerba', 'Yun', 'Fang']: # surname-sur, given E
                        surname = split_name[0] + "-" + split_name[1]
                        given_name = split_name[2]
                        order = "E"
                    elif split_name == ['Raiden', 'Ei', 'Baal']: # two fucking different characters, to be investigated!
                        surname = split_name[0]
                        given_name = split_name[1]
                        order = "E"
                    elif split_name == ['Vanessa', 'Vanjie', 'Mateo']: # drag name, so I guess first middle last or alias as a whole W
                        given_name = split_name[0]
                        middle_name = split_name[1]
                        surname = split_name[2]
                        order = "W"
                    elif split_name == ['Noctis', 'Lucis', 'Caelum']: # first KINGDOM HE'S THE PRINCE OF last W
                        given_name = split_name[0]
                        middle_name = split_name[1] # I GUESS
                        surname = split_name[2]
                        order = "W"
                    elif split_name == ['Villanelle', 'Oksana', 'Astankova']: # alias, Oksana Anatolyevna Astankova first middle last W
                        alias = split_name[0]
                        given_name = split_name[1]
                        middle_name = "Anatolyevna"
                        surname = split_name[2]
                        order = "W"
                    elif split_name == ['Kim', 'Khimhant', 'Theerapanyakun']: # still no evidence of this middle name :l
                        given_name = split_name[0]
                        surname = split_name[2]
                        alias = "Wik"
                        order = "W"

                elif len(split_name) == 4:
                    if split_name in sur_given_alias_alias:
                        surname = split_name[0]
                        given_name = split_name[1]
                        alias = split_name[2] + " " + split_name[3]
                        order = "E"
                    elif split_name in sur_given_courtesy:
                        surname = split_name[0]
                        given_name = split_name[1]
                        alias = split_name[2] + " " + split_name[3] # courtesy given name (as surname is same)
                        order = "E"
                    elif split_name == ['Cordelia', 'Foxx', 'Cordelia', 'Goode']:
                        given_name = split_name[0]
                        surname = split_name[1] + "/" + split_name[3]
                        order = "W"
                    elif split_name == ['Krista', 'Lenz', 'Historia', 'Reiss']: 
                        alias = split_name[0] + " " + split_name[1]
                        given_name = split_name[2]
                        surname = split_name[3]
                        order = "W"
                    elif split_name == ['Kate', 'Sheffield', 'Kate', 'Sharma']: # both maiden names, married name is bridgerton
                        given_name = split_name[0]
                        maiden_name = split_name[1] + "/" + split_name[3]
                        surname = "Bridgerton"
                        order = "W"
                    elif split_name == ['Tyrannus', 'Basilton', "'Baz'", 'Pitch']: # Tyrannus "Baz" Basilton Grimm-Pitch
                        given_name = split_name[0]
                        middle_name = split_name[1]
                        nickname = split_name[2]
                        surname = "Grimm-" + split_name[3]
                        order = "W"
                    elif split_name == ['Liu', 'Er', 'Mihou', 'Six-eared Macaque']: # gotta rename this fandom
                        surname = split_name[0] + "'" + split_name[1]
                        given_name = split_name[2]
                        alias = split_name[3]
                        order = "E"
                    elif split_name == ['Yang', 'Jian', 'Erlang', 'Shen']: 
                        alias = split_name[0] + " " + split_name[1]
                        surname = split_name[2]
                        given_name = split_name[3]
                        order = "E"
                    elif split_name == ['Captain', 'Hook', 'Killian', 'Jones']:
                        title_prefix = split_name[0]
                        alias = split_name[1]
                        given_name = split_name[2]
                        surname = split_name[3]
                        order = "W"
                    elif split_name == ['Creativity', 'Roman', "'Princey'", 'Sanders']:
                        alias = split_name[0]
                        given_name = split_name[1]
                        nickname = split_name[2]
                        surname = split_name[3]
                        order = "W"
                    elif split_name == ['Anakin', 'Skywalker', 'Darth', 'Vader']: # first last prefix alias
                        given_name = split_name[0]
                        surname = split_name[1]
                        title_prefix = split_name[2]
                        alias = split_name[3]
                        order = "W"
                    elif split_name == ['Ben', 'Solo', 'Kylo', 'Ren']: # first last alias suffix
                        given_name = split_name[0]
                        surname = split_name[1]
                        alias = split_name[2]
                        title_suffix = split_name[3]
                        order = "W"
                    elif split_name == ['Jonathan', "'Jon'", 'Sims', 'The Archivist']: # first nick last alias
                        given_name = split_name[0]
                        nickname = split_name[1]
                        surname = split_name[2]
                        alias = split_name[3]
                        order = "W"
                    elif split_name == ['Geralt', 'z Rivii', 'Geralt', 'of Rivia']: # I'm not keeping the translation sorry first suffix
                        given_name = split_name[0]
                        title_suffix = split_name[3]
                        order = "W"

                elif len(split_name) > 4:
                    if split_name == ['Mary', 'Wardwell', 'Madam', 'Satan', 'Lilith']:
                        given_name = split_name[0]
                        surname = split_name[1]
                        alias = split_name[2] + " " + split_name[3] + " / " + split_name[4]
                
                elif "Doctor" in split_name[0] or "Doctor" in split_name:
                    alias = "Doctor"
                    if split_name == ['Ninth Doctor']:
                        title_prefix = "The Ninth"
                    elif split_name == ['Tenth Doctor']:
                        title_prefix = "The Tenth"
                    elif split_name == ['Eleventh Doctor']:
                        title_prefix = "The Eleventh"
                    elif split_name == ['Twelfth Doctor']:
                        title_prefix = "The Twelfth"
                    elif split_name == ['Thirteenth Doctor']:
                        title_prefix = "The Thirteenth"
                    elif split_name == ['The Doctor']:
                        title_prefix = "The"
                elif "Reader" in split_name[0] or "Reader" in split_name:
                    alias = "Reader"
                    given_name = "Y/N"
                else: alias = "Player Character"

                default_dict = {
                    "given_name": given_name,
                    "middle_name": middle_name,
                    "maiden_name": maiden_name,
                    "surname": surname,
                    "alias": alias,
                    "nickname": nickname,
                    "title (prefix)": title_prefix,
                    "title (suffix)": title_suffix,
                    "name_order": order,
                    "full_name": None,
                    "fandom": fandom,
                    "op_versions": [og_name]
                }
                default_dict = add_full_name(default_dict)

                categorised_characters[category][fandom].append(default_dict) # appending to current fandom list

    return categorised_characters


if __name__ == "__main__":
    all_unformatted_characters = gather_all_raw_characters()
    bracketless_characters = remove_brackets(all_unformatted_characters)
    split_name_characters = separate_name_parts(bracketless_characters)
    grouped_by_fandom = group_split_names_by_fandom(split_name_characters)

    categorised_names = categorise_names(grouped_by_fandom)
    character_dict = {"categorised_name_characters": categorised_names}
    with open("data/reference_and_test_files/cleaning_characters/cleaned_characters_list_3_categorised_names.json", "w") as file:
        dump(character_dict, file, indent=4)