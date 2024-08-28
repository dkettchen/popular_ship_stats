from src.fifth_cleaning_stage_code.collect_race_tags_per_character import collect_race_tags
from json import dump
from copy import deepcopy

def assign_race_tag(data_dict):
    """
    takes a data dict as output by collect_race_tags

    outputs a new data dict of the same format except with the race collection 
    keys replaced with a single assigned race key

    some people/characters have yet to be reassigned for specificity
    """

    new_dict = {"RPF":{}, "fictional":{}}

    old_tags = [
        "Whi/POC", 
        "POC", 
        "Whi/Amb", 
        "Ambig", 
        "Amb/POC", 
        "Amb/Whi", 
        "POC/Whi", 
        "POC/Amb"
    ]
    tag_order_exceptions = {
        'Anne Boonchuy': "Asian",
        'Marcy Wu': "Asian",
        'Sasha Waybright': "White",
        "Kimberly Ann 'Kim' Hart | Pink Ranger": "Latino",
        'Trini Kwan | Yellow Ranger': "Asian",
    }
    asian_folks = [
        "Do Kyungsoo | D.O",
        "Kim Jongin | Kai",
        "Lee Donghyuck | Haechan",
        "Lee Jeno | Jeno",
        "Mark Lee | Mark",
        "Na Jaemin | Jaemin",
        "Ayanga",
        "Zhèng Yúnlóng",
        "Matsuoka Rin",
        "Nanase Haruka",
        "Tachibana Makoto",
        "Jiāng Chéng | Jiāng Wǎnyín",
        "Lán Huàn | Lán Xīchén",
        "Kakyoin Noriaki",
        "Kujo 'Jojo' Jotaro",
        "Ayase Eli",
        "Nishikino Maki",
        "Toujou Nozomi",
        "Yazawa Nico",
        "Genos | Demon Cyborg",
        "Saitama | One Punch Man/Caped Baldy",
        "Akemi Homura",
        "Kaname Madoka",
        "Hyakuya Mikaela",
        "Hyakuya Yuuichirou",
        "Nagachika Hideyoshi",
        "Sasaki Haise",
        "Baze Malbus", # chinese actor
        "Chirrut Îmwe", # actor is from hong-kong
        "Mark Fischbach | Markiplier",
        "Mulan",
        "Shimada Hanzo",
        "Otabek Altin", # kazakh -> central asian! we did have one after all!!
        "Kalinda Sharma", # south asian
        "Jessika Pava", # mother is singaporean-chinese of teochew descent
        "Noctis Lucis Caelum",
    ]
    latin_folks = [
        "Camila Cabello",
        "Lauren Jauregui",
        "Alexander Hamilton",
        "John Laurens",
        "Tori Vega",
        "Scott McCall",
        "Cassian Andor",
        "Calliope 'Callie' Torres", # canon bisexual, actor uses they/them pronouns but character uses she/her
        "Carlos", # we love an explicit wiki mention thank you
            # Carlos Robles is his full name
    ]
    black_folks = [
        "Thomas Jefferson",
        "Lincoln", # oldham lad let's fucking go
        "Vernon Boyd",
        "Pete Wentz", # half afro-jamaican
        "Nyota Uhura",
    ]
    white_folks = [
        "Sean McLoughlin | Jacksepticeye",
        "Jesse McCree | McCree", #?
        "Jack Morrison | Soldier: 76", #?
        "Aurora",
        "Jyn Erso",
        "Yuri Plisetsky",
        "Jade West",
        "Alicia Florrick",
        "Liam Dunbar",
        "Isaac Lahey",
        "Erica Reyes",
        "Alex Manes",
        "Grant Ward",
        "Arizona Robbins", # callie torres' canon ex wife
        "Prompto Argentum",
        "Barry Allen | The Flash",
        "Simon Snow", # baz's canon boyfriend
        "Jeremy Heere",
        "Josh Dun", # from wikipedia: "His great-great-great-grandparents were the 
        # American rancher Edwin Dun, who was the United States Ambassador to Japan, 
        # and his second Japanese wife, Yama." I'm making the executive decision that 
        # 3x great grandparent is too far removed to count as mention-worthy in the data set
        "Patrick Stump",
        "Eddie Brock | Venom",
        "Cosette Fauchelevent",
        "Peeta Mellark",
        "Johanna Mason",
        "Dipper Pines",
        "Sera",
        "Solas",
        "Jenny Flint", # madame vastra's wife
        "Alistair", # this is a ginger white man voiced by another white man, 
                    # idk why he was tagged as ambig/POC
        "Fenris", # basing this on op's decision to tag the other elves as white
        "Kaidan Alenko",
    ]
    other_folks = {
        "Allura": "Ambig", # girl's a alien with brown skin, 
                           # so not non-human skin tone but no specific human race
        "America Chavez | Ms. America": "Af Lat",
        "Octavia Blake": "SE Eu", # she's greek I haven't figured out how to label that yet
        "Theo Raeken": "Am Ind", # actor's mom is penobscot & he grew up on a reservation
        "Michael Guerin": "Ambig", # there are two versions of the show, og actor is white, 
                                   # new actor is greek, serbian (SE eu) & lebanese (MENA)
        "Gabriel Reyes | Reaper": "Af Lat",
        "Leonard Snart | Captain Cold": "White (mixed)", # looking at actor's heritage & 
        # man has a lot going on, idk what to categorise him as under my & op's systems 
        # so uhh we're just go with this for now (if we wanna add specifics: black & MENA, he's 
        # described his dad as black & mom as white, but both have white & non-white heritage)
        "Tyrannus Basilton 'Baz' Grimm-Pitch": "MENA", # wiki says "Mixed white & arab"
        "Michael Mell": "Ambig", # differing casts, also I'm not counting understudies 
                                 # bc some of em literally understudied both of these characters
        "Tyler Joseph": "White (mixed)", # of 1/4 lebanese descent
        "Venom (Symbiote)": "N.H.",
        "Éponine Thénardier": "Ambig", # op tagged as ambig bc of diff casting 
        "Katniss Everdeen": "Ambig", # she is described with black hair and olive skin 
                                     # in the book but white in the movie
        "Bill Cipher": "N.H.", # mf's a triangle
        "Costia": "Unknown", # not appearing in the show, lexa's ex-gf
        "Madame Vastra": "N.H.", # that's a lizard woman
        "Dorian Pavus": "Asian", # actor is SEA (Indo-Fijian & Malay)
        "Iron Bull": "N.H.", # that's a bull man
        "Isabela": "Ambig", # voice actors seem to be white women but she isn't
        "Josephine Montilyet": "Ambig", # no info on VA's background, 
                                        # so we're going with a character-visual idk
        "Adam": "Ambig", # VA is POC but no info on details
        "Cecil Palmer": "Ambig", # I don't think there's a canon race & this is audio only 
            # canon husband of carlos
            # full name is Cecil Gershwin Palmer

    }
    characters_to_retag = {
        # "Sanji Vinsmoke | Black-Leg Sanji": "White", # Taz is british-arab but playing a white char
            # is already tagged correctly cause op doesn't follow their own method
        "Elizabeth Burke, née Mitchell": "White (mixed)", # turkish & greek in there
        "Hob Gadling": "White", # actor is 3/4 white and the character is a random medieval white man
        'Brendon Urie': "White (mixed)", # 3/4 white, 1/4 polynesian/hawaiian
        "Anna": "Eu Ind", # same format as "As Ind"
        "Elsa": "Eu Ind", # ""
        "Wanda Maximoff | Scarlet Witch": "Romani", # explicit comics take priority over 
                                                    # non-explicit MCU & actress
        'Maggie Sawyer': "Ambig", # bc of latino casting vs comic original being a white woman
        'Pamela Isley | Poison Ivy': "Ambig", # bc sometimes she's green, 
                                              # sometimes she's just a ginger white woman
        'Willie': "Asian | Am Ind", # man's east asian AND native american, 
                                      # not asian indigenous
    }

    for category in ["RPF", "fictional"]:
        for fandom in data_dict[category]:
            if fandom not in new_dict[category].keys():
                new_dict[category][fandom] = {}
            for character in data_dict[category][fandom]:
                race_tag = None

                if character not in new_dict[category][fandom].keys():
                    new_dict[category][fandom][character] = {}
                input_character_dict = data_dict[category][fandom][character]

                if not race_tag and input_character_dict["most_recent_race_tag"]:

                    if input_character_dict["most_recent_same_race_tag"] \
                    and input_character_dict["most_recent_race_tag"] \
                    == input_character_dict["most_recent_same_race_tag"]:
                        # if the latest tag is also a same race tag
                        race_tag = input_character_dict["most_recent_race_tag"][0]

                    elif type(input_character_dict["most_recent_race_tag"]) == str \
                    and "/" not in input_character_dict["most_recent_race_tag"] \
                    and input_character_dict["most_recent_race_tag"] != "POC":
                        # if it is one of our manually assigned ones
                        race_tag = input_character_dict["most_recent_race_tag"]
                    
                    elif type(input_character_dict["most_recent_race_tag"]) == list:
                        if character not in tag_order_exceptions:
                            # if the characters are in the correct order
                            index = input_character_dict['most_recent_pairing_index']
                            race_tag = input_character_dict["most_recent_race_tag"][index]
                        else:
                            # if they were not in the right order/order was ambiguous
                            race_tag = tag_order_exceptions[character]

                    #for any leftover old values:
                    elif input_character_dict["full_name"] in asian_folks:
                        race_tag = "Asian"
                    elif input_character_dict["full_name"] in latin_folks:
                        race_tag = "Latino"
                    elif input_character_dict["full_name"] in black_folks:
                        race_tag = "Black"
                    elif input_character_dict["full_name"] in white_folks:
                        race_tag = "White"
                    elif input_character_dict["full_name"] in other_folks:
                        race_tag = other_folks[input_character_dict["full_name"]]
                
                if input_character_dict["full_name"] in characters_to_retag:
                    race_tag = characters_to_retag[input_character_dict["full_name"]]
                
                if race_tag == "Latino":
                    race_tag = "Latin" # making gender neutral
                if race_tag == "M.E.":
                    race_tag = "MENA" # unifying with rest
                if race_tag == "White (mixed)":
                    race_tag = "White (Multi)" 
                    # easier than going back through all previous mentions
                
                new_character = new_dict[category][fandom][character]
                for key in [
                    "given_name",
                    "middle_name",
                    "maiden_name",
                    "surname",
                    "alias",
                    "nickname",
                    "title (prefix)",
                    "title (suffix)",
                    "name_order",
                    "full_name",
                    "fandom",
                    "op_versions",
                    "gender",
                ]:
                    new_character[key] = input_character_dict[key]
                new_character["race"] = race_tag

    return new_dict

def retag_for_specificity(data_dict):

    new_dict = deepcopy(data_dict)

    #TODO: retagging section

    multiracial_folks = {

    }
    south_asian_folks = {

    }
    east_asian_folks = {

    }
    sea_folks = {

    }
    asian_indig_folks = {

    }
    american_indig_folks = {

    }
    other_folks_to_be_retagged = {

    }
    east_asian_fandoms = [
        
    ]

    for category in ["RPF", "fictional"]:
        for fandom in new_dict[category]:
            for character in new_dict[category][fandom]:
                # if we know whole fandom will be one thing (ex anime being east-asian)
                # we can reassign it by that

                # otherwise we can have our specific cases
                pass


    # retag all indig characters w continent/region specification pls 
        # bc we have "As Ind" & "Eu Ind" now
    # retag all asian characters w cardinal direction specification 
        # ("S Asian", "SEA", "E Asian", "Central As")
    # verify any "Ambig" tagged characters
    # if we do end up making multiracial tags to use 
        # (maybe as a stat outside of their main grouping??)
        # we should also go through all, at least POC, again 
            # (we'll have to comb through the asians anyway for specificity)
        # I think a multiracial tag would be useful:
            # bc we got some very light-skinned mixed-black folks that it seems silly to 
            # equate with their more obviously-identifiable-as-black peers
                # like Christen Press and Pete Wentz
            # and to highlight diverse rep in non-white-majority countries like asian ones
                # like for asian-white characters in those media properties who are Different 
                # BECAUSE they're part white 
                # -> I'm not gonna make asian media's ethnic diversity out to be worse than 
                # it is just cause anime needs everyone to also be half-japanese
                # (as I plan on visualising the diversity by media's country or origin 
                # and all that later)
        # how to determine who qualifies?
            # only tryna determine this where we have available info 
                # (eg established for character, real person's wikipedia, etc)
            # do we want to specify details? or just tag as multiracial/mixed/smth along those lines?
                # we likely want to be able to query by specifics tho, so should include them
            # put tags in alphabetical order to avoid having to figure out an order individually
            # I'm only including shit that can be traced to grandparental ancestry -> 1/4 min
                # nothing further back than that
            # maybe format like (f.e.) "Multi (Asian, Black)" 
                # -> can query by "Multi", "Asian" and "Black"
                # always starts in same bit regardless of details, so can be grouped by that
            # this also solves for folks with tags like "Af Lat" etc 
                # -> can just be tagged as "Multi (Black, Latin)" instead
            
            # where info is available:
            # if someone is white + POC biracial and the POC part is >= 1/2 
                # and/or they're easily identifyable as their POC group
                    # -> they will be tagged as "<poc group> (Multi)"
                    # -> obama example stays intact
            # if someone is white + POC biracial, but the white part is more than 1/2
                # -> they will be tagged as "White (Multi)"
                # my "it's unreasonable to tag these ppl as more rep than they are" examples 
                # stay intact
            # if we only know of one group & that they are mixed, 
                # we will tag them as that group + (Multi), same as above
            # if someone is of two groups neither of which is white
                # we will tag them as "<group a> <group b> (Multi)"
                # like f.e. Af Lat (we can keep these labels this way)
            # if someone is less than 1/4 of a different group than their main one 
                # I'm not counting it
            # if someone is of more groups than 2, they are tagged as just "Multi"
                # possibly with another bit for details?

    pass




if __name__ == "__main__":
    collected_dict = collect_race_tags()
    race_tagged_dict = assign_race_tag(collected_dict)
    filepath = "data/reference_and_test_files/assigning_demographic_info/assigning_race_4_assigning_race.json"
    with open(filepath, "w") as file_4:
        dump(race_tagged_dict, file_4, indent=4)