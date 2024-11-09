from visualisation.input_data_code.make_file_dfs import make_characters_df
from copy import deepcopy

fandom_instances = { # putting outside of functions to access in multiple!
    "Harry Potter Universe" : [
        # separating by franchises/media types not individual movies
            # cause main media is pre-2013 and fantastic beasts is barely in the ranking
            # -> individual movies not relevant here

        # only ones that seem relevant bc there's too dang much
        ("Harry Potter (books)",1997,2007),
        ("Harry Potter (movies)",2001,2011),
        ("Fantastic Beasts (movies)",2016,2022),
        ("Harry Potter and the Cursed Child (stage play)",2016,"current"),
        ("Hogwarts Legacy (game)",2023) 
            # (games in general have been releasing since 2001 & until 2024 so far)
        # they're also currently making a fucking TV series rebooting the original series smh
    ],
    "Marvel" : {
        # tracking all MCU media bc specific chars only appear in some of them
        "movies" : [
            # MCU phase 1
            ("Iron Man",2008),
            ("The Incredible Hulk",2008),
            ("Iron Man 2",2010),
            ("Thor", 2011),
            ("Captain America: The First Avenger", 2011),
            ("The Avengers",2012),

            # MCU phase 2
            ("Iron Man 3",2013),
            ("Thor: The Dark World",2013),
            ("Captain America: The Winter Soldier",2014),
            ("Guardians of the Galaxy",2014),
            ("Avengers: Age of Ultron",2015),
            ("Ant-Man",2015),

            # MCU phase 3
            ("Captain America: Civil War", 2016),
            ("Doctor Strange", 2016),
            ("Guardians of the Galaxy Vol. 2", 2017),
            ("Spider-Man: Homecoming", 2017),
            ("Thor: Ragnarok", 2017),
            ("Black Panther", 2018),
            ("Avengers: Infinity War", 2018),
            ("Ant-Man and the Wasp", 2018),
            ("Captain Marvel", 2019),
            ("Avengers: Endgame", 2019),
            ("Spider-Man: Far From Home", 2019),

            # MCU phase 4
            ("Black Widow", 2021),
            ("Shang-Chi and the Legend of the Ten Rings", 2021),
            ("Eternals", 2021),
            ("Spider-Man: No Way Home", 2021),
            ("Doctor Strange in the Multiverse of Madness", 2022),
            ("Thor: Love and Thunder", 2022),
            ("Black Panther: Wakanda Forever", 2022),

            # MCU phase 5 (only until 2023 bc that's out data range for now)
            ("Ant-Man and the Wasp: Quantumania", 2023)
            ("Guardians of the Galaxy Vol. 3", 2023)
            ("The Marvels", 2023)
        ],
        "shows" : [
            # ABC shows
            ("Agents of S.H.I.E.L.D.", 2013, 2020),
            ("Agent Carter", 2015, 2016),
            ("Inhumans", 2017, 2017),

            # netflix shows
            ("Daredevil",2015,2018),
            ("Jessica Jones",2015,2019),
            ("Luke Cage",2016,2018),
            ("Iron Fist",2017,2018),
            ("The Defenders",2017,2017),
            ("The Punisher",2017,2019),

            # YA series
            ("Runaways",2017,2019),
            ("Cloak & Dagger",2018,2019),

            # marvel studios phase 4 & 5 (only until 2023 once again)
            ("WandaVision",2021,2021),
            ("The Falcon and the Winter Soldier",2021,2021),
            ("Loki",2021,2023),
            ("What If...?",2021,2023),
            ("Hawkeye",2021,2021),
            ("Moon Knight",2022,2022),
            ("Ms. Marvel",2022,2022),
            ("She-Hulk: Attorney at Law",2022,2022),
            ("Secret Invasion",2023,2023),
        ],
        "comics" : [ # some from tracked time span that I know about
            ("Young Avengers (Kieron Gillen & Jamie McKelvie)", 2013, 2014), 
                # america & kate bishop as well as the canon gays made the ranking
            # relevant main line series they've been adapting?? inifinity war etc? 
            # maybe only like recent ones??
            ("Loki: Agent Of Asgard (Al Ewing & Lee Garbett)", 2014, 2015), 
                # loki solo series that influenced loki tv show a lot
            ("Hawkeye (Matt Fraction & David Aja)", 2012, 2015)
                # hawkeye series w the good art! Matt Fraction! features both kate & clint
            # there's probably more recent series idk about cause I don't read em anymore rip :l
        ],
        # add animations later too?
        "other_stuff" : [
            ("Marvel Snap", 2022), # cause recent
            ("MCU (overall)", 2008, "current"),
            ("Marvel Comics (overall)", 1961, "current"),

            # other movies
            ("X-Men (original trilogy)",2000,2006),
            ("Wolverine trilogy",2009,2017),
            ("X-Men (prequel movies)",2011,2019),
            ("Deadpool movies",2016,2024),
            ("The New Mutants",2020),
            ("Spider-Man: Into the Spiderverse", 2018),
            ("Spider-Man: Across the Spiderverse", 2023),
        ],
    },
    "DC" : {
        # tracking recent & relevant movies & TV for now
        "movies" : [
            ("Man of Steel",2013),
            ("Batman v Superman: Dawn of Justice",2016),
            ("Suicide Squad",2016),
            ("Wonder Woman",2017),
            ("Justice League",2017),
            ("Aquaman",2018),
            ("Shazam!",2019),
            ("Joker",2019),
            ("Birds of Prey",2020),
            ("Wonder Woman 1984",2020),
            ("The Suicide Squad",2021),
            ("The Batman",2022),
            ("Batgirl",2022),
            ("Black Adam",2022),
            ("Shazam! Fury of the Gods",2023),
            ("The Flash",2023),
            ("Blue Beetle",2023),
            ("Aquaman and the Lost Kingdom",2023),
        ],
        "shows" : [
            ("Arrow",2012,2020)
            ("The Flash",2014,2023)
            ("Supergirl",2015,2021)
            ("Legends of Tomorrow",2016,2022)
            ("Black Lightning",2018,2021)
            ("Batwoman",2019,2022)
        ],
        # add animations & comics later too?
        "other_stuff" : [
            ("Detective Comics (overall)",1937,"current"),
            ("DC movies (overall)", 1951, "current"),
            ("DCEU (overall)", 2013, "current"),
            ("The Lego Batman Movie", 2017),
            ("The Dark Knight trilogy (Nolan movies)", 2005, 2012)
        ],
    },
    "Star Wars Universe" : {
        "movies" : [
            ("Prequel Trilogy",1999,2005),
            ("Original Trilogy",1977,1983),
            ("Sequel Trilogy",2015,2019),
            ("Rogue One: A Star Wars Story",2016),
            ("Solo: A Star Wars Story",2018),
        ],
        "shows" : [
            ("The Mandalorian",2019,"current"),
            ("The Book of Boba Fett",2021,2022),
            ("Obi-Wan Kenobi",2022,2022),
            ("Andor",2022,"current"),
            ("Ahsoka",2023,"current"),
            ("The Clone Wars",2008,2020), # animated series
            ("Rebels",2014,2018), # animated series
        ],
    },
}

def add_instances(input_list):
    """
    takes a list of dicts with at least a "fandom" key

    returns a list of dicts that contains unchanged dicts for fandoms without different instances
    and a dict for each instance of relevant other fandoms (ie for each youtuber, for each movie 
    in certain franchises, etc)
    """

    fandom_list = deepcopy(input_list)
    
    new_list = []

    for fandom_dict in fandom_list:
        fandom = fandom_dict["fandom"]
        if fandom in fandom_instances:
            instance_list = fandom_instances[fandom]

        if fandom == "Youtube": # bc they're from diff countries etc
            char_df = make_characters_df()
            youtube_df = char_df.where(char_df["fandom"] == "Youtube").dropna()
            youtuber_list = sorted(list(youtube_df["full_name"]))

            for youtuber in youtuber_list:
                new_dict = deepcopy(fandom_dict)
                new_dict["instance"] = youtuber

                new_list.append(new_dict) # appending a dict for each youtuber

        elif "Harry Potter" in fandom: 
            for item in instance_list:
                new_dict = deepcopy(fandom_dict)
                new_dict["instance"] = item[0]
                new_dict["start_date"] = item[1]
                if len(item) == 3:
                    new_dict["end_date"] = item[2]
                else: new_dict["end_date"] = item[1]

                new_list.append(new_dict)
        
        elif fandom in ["Marvel", "DC", "Star Wars Universe"]:
            for movie in instance_list["movies"]:
                new_dict = deepcopy(fandom_dict)
                new_dict["instance"] = movie[0]
                new_dict["start_date"] = movie[1]
                new_dict["end_date"] = movie[1]

                new_list.append(new_dict)
            for show in instance_list["shows"]:
                new_dict = deepcopy(fandom_dict)
                new_dict["instance"] = show[0]
                new_dict["start_date"] = show[1]
                new_dict["end_date"] = show[2]
                
                new_list.append(new_dict)
            if fandom == "Marvel": # comics so far only for marvel
                for comic in instance_list["comics"]:
                    new_dict = deepcopy(fandom_dict)
                    new_dict["instance"] = comic[0]
                    new_dict["start_date"] = comic[1]
                    new_dict["end_date"] = comic[2]
                    
                    new_list.append(new_dict)
            if fandom != "Star Wars Universe": # other stuff so far only for marvel & DC
                for stuff in instance_list["other_stuff"]:
                    new_dict = deepcopy(fandom_dict)
                    new_dict["instance"] = stuff[0]
                    new_dict["start_date"] = stuff[1]
                    if len(stuff) == 3:
                        new_dict["end_date"] = stuff[2]
                    else: new_dict["end_date"] = stuff[1]
                    
                    new_list.append(new_dict)

        # check what other stuff may need instances!

        else: # if no instances need to be added, we add unchanged dict
            new_list.append(fandom_dict)

    return new_list

def add_remaining_dates(input_list): #TODO

    pass

def add_media_types(input_list): #TODO

    pass

