from visualisation.input_data_code.make_file_dfs import make_characters_df
from copy import deepcopy

fandom_instances = {
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
            ("Ant-Man and the Wasp: Quantumania", 2023),
            ("Guardians of the Galaxy Vol. 3", 2023),
            ("The Marvels", 2023),
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
            ("Arrow",2012,2020),
            ("The Flash",2014,2023),
            ("Supergirl",2015,2021),
            ("Legends of Tomorrow",2016,2022),
            ("Black Lightning",2018,2021),
            ("Batwoman",2019,2022),
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
    "Star Wars" : {
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
    "Figure Skating": [
        'Boyang Jin', # chinese
        'Yuzuru Hanyu', # japanese
    ],
    "Hockey": [
        'Jonathan Toews', # canadian
        'Patrick Kane', # american
    ],
    "Dragon Age": [ 
        # these are I think the only ones relevant??
        ("Dragon Age: Origins",2009), # Warden
        ("Dragon Age II",2011), # Hawke
        ("Dragon Age: Inquisition",2014) # Inquisitor
    ],
    "A Song of Ice and Fire / Game of Thrones Universe": [
        ("A Song of Ice and Fire (books)",1996,"current"),
        ("Game of Thrones",2011,2019),
        ("House of the Dragon",2022,"current")
    ],
    "Buffy Universe": [
        ("Buffy the Vampire Slayer",1997,2003),
        ("Angel",1999,2004)
    ],
    "Star Trek": [
        ("Star Trek: The Original Series",1965,1969),
        ("Star Trek: Deep Space Nine",1993,1999),
        ("Star Trek: Voyager",1995,2001),
        ("Star Trek: The Next Generation",1987,1994),
        ("Star Trek: Enterprise",2001,2005),
        ("Star Trek (Original movies)",1979,1982),
        ("Star Trek (J.J. Abrams movies)",2009,2016),
        ("Star Trek: Picard",2020,2023),
        ("Star Trek: Discovery",2017,2024)
    ],
    "Stargate": [
        ("Stargate SG-1",1997,2007),
        ("Stargate Atlantis",2004,2009),
    ],
    "Dangan Ronpa": [ # only collecting main line cause there's too many
        ("Danganronpa: Trigger Happy Havoc",2010),
        ("Danganronpa 2: Goodbye Despair", 2012),
        ("Danganronpa V3: Killing Harmony", 2017),
    ],
    "Doctor Who": [
        ("Doctor Who (original series, Doctors 1-7)",1963,1989),
        ("Doctor Who (movie, 8th Doctor)",1996),
        ("Ninth Doctor",2005),
        ("Tenth Doctor",2005,2010),
        ("Eleventh Doctor",2010,2013),
        ("Twelfth Doctor",2014,2017),
        ("Thirteenth Doctor",2018,2022),
        ("Fourteenth Doctor",2023),
        ("Fifteenth Doctor",2023, "current"),
        ("Torchwood",2006,2011)
    ], # group by doctor eras? #"Torchwood", (cause we'll unite it w doctor who n make it an instance later)
    "Final Fantasy | ファイナルファンタジー" : [
        ("Final Fantasy",1987),
        ("Final Fantasy II",1988),
        ("Final Fantasy III",1990),
        ("Final Fantasy IV",1991),
        ("Final Fantasy V",1992),
        ("Final Fantasy VI",1994),
        ("Final Fantasy VII",1997),
        ("Crisis Core: Final Fantasy VII",2007),
        ("Final Fantasy VII (remake series)", 2020, "current"),
        ("Final Fantasy VIII",1999),
        ("Final Fantasy IX",2000),
        ("Final Fantasy X",2001),
        ("Final Fantasy X-2",2003),
        ("Final Fantasy XI: Online",2002),
        ("Final Fantasy XII",2006),
        ("Final Fantasy XIII",2009),
        ("Final Fantasy XIV",2013,"current"),
        ("Final Fantasy XV",2016),
        ("Final Fantasy XVI",2023),
    ],
    "Lord of the Rings Universe": [
        ("Lord of the Rings (book series)", 1954, 1955),
        ("Lord of the Rings (movie trilogy)", 2001, 2003),
        ("The Hobbit (book)", 1937),
        ("The Hobbit (movie trilogy)",2012,2014),
    ],
    "Persona": [ # there's only these 2 in the ranking
        ("Persona 5",2016),
        ("Persona 4",2008),
    ],
    "Shadowhunters | Mortal Instruments": [
        ("Shadowhunters: The Mortal Instruments", 2016,2019),
        ("The Mortal Instruments (book series)", 2007,2014),
        ("The Mortal Instruments: City of Bones", 2013)
    ], # it should just be mortal instruments! shadow hunters is just the tv show version!
    "Teenage Mutant Ninja Turtles": [
        ("Rise of the Teenage Mutant Ninja Turtles", 2018, 2020),
        ("Rise of the Teenage Mutant Ninja Turtles (movie)", 2022),
        ("Teenage Mutant Ninja Turtles (overall)", 1984,"current")
    ],
    "The Witcher | Wiedźmin": [
        ("The Witcher (TV)", 2019, "current"),
        ("The Witcher | Wiedźmin (book series)",1986,2013),
        ("The Witcher (game series)", 2007,2015),
    ],
    "Trigun Universe | トライガン": [
        ("Trigun (manga)",1995,1996),
        ("Trigun (original anime)",1998),
        ("Trigun Stampede",2023)
    ],
    "Vampire Diaries Universe": [
        ("The Vampire Diaries",2009,2017),
        ("Legacies",2018,2022),
        ("The Originals",2013,2018)
    ],
    "Les Misérables": [
        ("book",1862),
        ("musical", 1980,"current"),
        ("movie",2012)
    ],
    "Queer as Folk": [
        ("US version (original)",2000,2005), 
        ("UK version",1999,2000), 
        ("US version (reboot)",2022)
    ],
    "Drag":[
        ("RuPaul's Drag Race (US)", 2009,"current"),
        ("RuPaul's Drag Race UK", 2019,"current")
    ],
    "Shameless":[
        ("UK version",2004,2013),
        ("US version",2011,2021),
    ],
    "One Piece | ワンピース": [
            ("manga",1997,"current"), 
            # Oda Eiichiro
            ("anime",1999,"current"),
            ("live action series",2023,"current") # live action!!
    ],
    "Avatar: The last Airbender Universe": [
        ("Avatar: The last Airbender",2005,2008),
        ("The Legend of Korra",2012,2014),
    ],
    "adaptations": {
        "Good Omens": [
            ("Good Omens: The Nice and Accurate Prophecies of Agnes Nutter, Witch",1990), 
            # Terry Pratchett and Neil Gaiman
            ("Good Omens",2019,"current")
        ],
        "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令": [
            ("Grandmaster of Demonic Cultivation | 魔道祖师",2015,2016),
            # Mo Xiang Tong Xiu | MXTX
            ("The Untamed | 陈情令",2019)
        ],
        "Heaven Official's Blessing | 天官赐福": [
            ("Heaven Official's Blessing | 天官赐福 (books)",2017,2019),
            # Mo Xiang Tong Xiu | MXTX
            ("Heaven Official's Blessing | 天官赐福 (donghua)",2020,2024) # animated show
        ],
        "Heartstopper": [
            ("graphic novel",2016),
            # Alice Oseman
            ("show",2022, "current")
        ],
        "Hunger Games / Panem Universe": [
            ("Panem trilogy",2008,2010),
            # Suzanne Collins
            ("The Hunger Games (movies)",2012,2015)
        ],
        "IT": [
            ("IT",1986),
            # Stephen King
            ("IT (movies)",2017,2019)
        ],
        "James Bond Universe": [
            ("James Bond (book series)",1953,1966), 
            # Ian Fleming
            ("James Bond (movies)",1962,2021)
        ],
        "Attack on Titan | 進撃の巨人": [
            ("manga",2009,2021), 
            # Isayama Hajime 
            ("anime",2013,2023)
        ],
        "BLUELOCK | ブルーロック": [
            ("manga",2018,"current"), 
            # Kaneshiro Muneyuki
            ("anime",2022,"current")
        ],
        "Bungou Stray Dogs | 文豪ストレイドッグス": [
            ("manga",2012,"current"), 
            # written by Asagiri Kafka, illustrated by Harukawa Sango
            ("anime",2016,"current")
        ],
        "Carmilla": [
            ("book",1872),
            # Sheridan Le Fanu # irish
            ("web series",2014,2016) # canadian
        ],
        "Fullmetal Alchemist | 鋼の錬金術師": [
            ("manga",2001,2010), 
            # Arakawa Hiromu
            ("Fullmetal Alchemist: Brotherhood",2009,2010)
        ],
        "Haikyuu!! | ハイキュー!!": [
            ("manga",2012,2020), 
            # Furudate Haruichi
            ("anime (incl movies)",2014,2024)
        ],
        "Hetalia | ヘタリア": [
            ("manga",2003,"current"), 
            # Himaruya Hidekazu
            ("anime",2009,2021)
        ],
        "JoJo's Bizarre Adventure | ジョジョの奇妙な冒険": [
            ("manga",1987,"current"), 
            # Araki Hirohiko
            ("anime",2012,"current")
        ],
        "Jujutsu Kaisen | 呪術廻戦": [
            ("manga",2018,2024), 
            # Akutami Gege
            ("anime",2020,2023)
        ],
        "My Hero Academia | 僕のヒーローアカデミア": [
            ("manga",2014,2024), 
            # Horikoshi Kōhei
            ("anime",2016,"current")
        ],
        "Naruto": [
            ("manga",1999,2014), 
            # Kishimoto Masashi
            ("anime",2002,2017)
        ],
        "One-Punch Man | ワンパンマン": [
            ("manga",2009,"current"), 
            # One
            ("anime",2015,"current")
        ],
        "Orange is the New Black": [
            ("Orange Is the New Black: My Year in a Women's Prison",2010), 
            # Piper Kerman
            ("Orange is the New Black",2013,2019)
        ],
        "Percy Jackson": [
            ("Percy Jackson & the Olympians",2005,2009), 
            # Rick Riordan
            ("Percy Jackson (movies)",2010,2013)
        ],
        "Pretty Guardian Sailor Moon | 美少女戦士セーラームーン": [
            ("manga",1991,1997), 
            # Takeuchi Naoko
            ("anime",1992,1997)
        ],
        "Seraph of the End | 終わりのセラフ": [
            ("manga",2012,"current"),
            # written by Kagami Takaya and illustrated by Yamamoto Yamato
            ("anime",2015)
        ],
        "The Old Guard": [
            ("graphic novel",2017,2021),
            # by Greg Rucka and Leandro Fernández
            ("movies",2020,2023)
        ],
        "The Sandman": [
            ("comic",1989,1996),
            # Neil Gaiman
            ("show",2022,"current")
        ],
        "Tokyo Ghoul | 東京喰種": [
            ("manga",2011,2014),
            # Ishida Sui
            ("anime",2014)
        ],
        "Tokyo Revengers | 東京卍リベンジャーズ": [
            ("manga",2017,2022),
            # Wakui Ken
            ("anime",2021,"current")
        ],
        "Twilight": [
            ("books",2005,2008),
            # Stephenie Meyer
            ("movies",2008,2012)
        ],
        "Word of Honor | 山河令": [
            ("Faraway Wanderers | 天涯客",2010), # also a danmei novel!
            # Priest (pseudonym)
            ("Word of Honor | 山河令",2021)
        ], # "Faraway Wanderers" (天涯客) is book name - fix name to add that
        "Be More Chill": [
            ("book",2004),
            # Ned Vizzini
            ("musical",2015,"current")
        ],
        "Bridgerton": [
            ("books",2000,2006),
            # Julia Quinn
            ("show",2020,"current")
        ],
        "Carol": [
            ("The Price of Salt",1952),
            # Patricia Highsmith
            ("Carol",2015)
        ],
        "Free!": [
            ("High Speed! | ハイ☆スピード!", 2013,2014),
            # Kōji Ōji
            ("anime",2013,2018)
        ],
        "Kingsman": [
            ("comics",2012,2023), # published by marvel!
            # comic book series created by Mark Millar and Dave Gibbons
            ("movies",2014,2021), 
        ],
        "Legend of the Seeker": [
            ("The Sword of Truth", 1994,2020),
            # Terry Goodkind
            ("Legend of the Seeker",2008,2010),
        ],
        "The Last of Us": [
            ("game",2013),
            ("show",2023) 
        ],
    },
    "other_fandoms": {
        "Addam's Family Universe": ("Wednesday",2022,"current"),
        "Fire Emblem | ファイアーエムブレム": ("Fire Emblem: Three Houses",2019),
        "Journey to the West Universe": ("LEGO Monkie Kid",2020,2024),
        "Kill la Kill | キルラキル": (2013,2014), # not based on a manga! studio trigger
        "Little Witch Academia | リトルウィッチアカデミア": (2013,2017), 
            # started as (short) films, then anime & manga stuff, also studio trigger
        "Omniscient Reader | 전지적 독자 시점": ("web novel",2018,2020), 
            # Sing Shong (dunno if this is correct order)
        "Puella Magi Madoka Magica | 魔法少女まどか☆マギカ": (2011,),
        "SK8 the Infinity | SK∞ エスケーエイト": (2021,"current"),
        "9-1-1": (2018,"current"),
        "Adventure Time": (2010,2018),
        "All For The Game": (2013,2014), # Nora Sakavic # novel series
        "American Horror Story": (2011,"current"),
        "Amphibia": (2019,2022),
        "Arcane": (2021,2024),
        "Battlestar Galactica": (2004,2009), # there are so many but I'm counting the 2004 TV show
        "Call of Duty": (2003,"current"),
        "Carry On": (2015,), # there are other books in this series w diff titles, 
                            # this seems to only refer to one specific book
        "Castle": (2009,2016),
        "Check Please!": (2013,2020), # webcomic by Ngozi Ukazu
        "Criminal Minds": (2005, "current"), # WYM CRIMINAL MINDS IS STILL GOING
        "Critical Role": (2015,"current"), # we could mess with campaigns if we want to
        "Descendants": (2015,),
        "Detroit: Become Human": (2018,),
        "Due South": (1994,1999),
        "Emmerdale": (1972,"current"),
        "Faking It": ("US version", 2014,2016),
        "Frozen": (2013,),
        "Generation Kill": (2008,),
        "Genshin Impact | 原神": (2020,"current"),
        "Ghostbusters": (1984,"current"),
        "Girl Meets World": (2014,2017),
        "Glee": (2009,2015),
        "Gravity Falls": (2012,2016),
        "Grey's Anatomy": (2005,"current"),
        "Hamilton": (2015,"current"),
        "Hannibal": (2013,2015),
        "Hawaii Five-0": (2010,2020),
        "Hazbin Hotel": (2019,"current"), # Vivienne "VivziePop" Medrano
        "Highlander": (1986,),
        "Holby City": (1999,2022),
        "Homestuck": (2009,2016),
        "House M.D.": (2004,2012),
        "Inception": (2010,),
        "Julie and The Phantoms": (2020,),
        "Killing Eve": (2018,2022),
        "Kim Possible": (2002,2007),
        "Kingdom Hearts": (2002,2020),
        "KinnPorsche | คินน์พอร์ช เดอะ ซีรีส์": (2022,),
        "Law & Order": (1990,"current"),
        "Life Is Strange": (2015,),
        "Life on Mars": (2006,2007),
        "Lizzie Bennet Diaries": (2012,2013),
        "Lockwood & Co.": (2023,),
        "Lost Girl": (2010,2016),
        "Love Live! | ラブライブ!": (2010,2023),
        "Lucifer": (2016,2021),
        "Maleficent": (2014,),
        "Mass Effect": (2007,2021),
        "Merlin": (2008,2012),
        "Miraculous: Tales of Ladybug & Cat Noir | Miraculous: Les Aventures de Ladybug et Chat Noir": (2015,"current"),
        "Mobile Suit Gundam Wing | 新機動戦記ガンダム W": (1995,1996),
        "Motherland": (2016,2022),
        "NCIS": (2003,"current"),
        "New Gods | 新神榜": (2021,2022), # animated movies
        "Once Upon a Time": (2011,2018),
        "Orphan Black": (2013,2017),
        "Our Flag Means Death": (2022,2023),
        "Overwatch": (2016,"current"),
        "Pacific Rim": (2013,2021),
        "Person of Interest": (2011,2016),
        "Pitch Perfect": (2012,2017),
        "Power Rangers": (1993,"current"),
        "RWBY": (2012,"current"),
        "Raven Cycle": (2012,2016), # novel series
        "Rizzoli & Isles": (2010,2016),
        "Rookie Blue": (2010,2015), # tv show
        "Roswell New Mexico": (2019,2022),
        "SKAM": (2015,2017),
        "Sanders Sides": (2016,"current"),
        "Schitt's Creek": (2015,2020),
        "Shadow and Bone": (2021,2023),
        "She-Ra and the Princesses of Power": (2018,2020),
        "Sherlock": (2010,2017),
        "Six of Crows": (2015,), # novel
        "Skins": (2007,2013),
        "South Park": (1997,"current"),
        "Spartacus": (2010,2013),
        "Starsky & Hutch": (1975,1979),
        "Station 19": (2018,2024), # tv show abt fire fighters
        "Steven Universe": (2013,2019),
        "Stranger Things": (2019,2025),
        "Suits": (2011,2019),
        "Super-Vocal | 声入人心": (2018,2019),
        "Supernatural": (2005,2020),
        "Teen Wolf": (2011,2017),
        "The 100": (2014,2020),
        "The Big Bang Theory": (2007,2019),
        "The Closer": (2005,2012),
        "The Devil Wears Prada": (2006,),
        "The Good Wife": (2009,2016),
        "The Haunting of Bly Manor": (2020,),
        "The Locked Tomb / Gideon the Ninth": (2019,2022), # only a book series so far
        "The Magnus Archives": (2016,2021),
        "The Man From U.N.C.L.E.": (2015,), # movie
        "The Owl House": (2020,2023),
        "The Professionals": (1977,1983), # show
        "The Rookie": (2018,"current"), # show
        "The Sentinel": (2006,), # movie
        "The Walking Dead": (2010,2022),
        "The Wilds": (2020,2022), # show
        "The X-Files": (1993,2018),
        "Top Gun": (1986,2022),
        "Undertale": (2015,),
        "Victorious": (2010,2013), # show
        "Voltron": (2016,2018),
        "Warehouse 13": (2009,2014),
        "Warrior Nun": (2020,2022), # based on a comic char but not a specific comic
        "Welcome to Night Vale": (2012,"current"),
        "Wentworth": (2013,2021),
        "White Collar": (2009,2014),
        "Wynonna Earp": (2016,2021),
        "Xena": (1995,2001), # show
        "Young Royals": (2021,2024),
        "Yuri!!! on ICE | ユーリ!!! on ICE": (2016,2017), # didn't have a manga
    },
    "music": { # debut dates (acc to wikipedia)
        "5 Seconds of Summer": (2011,), # formed in
        "Adam Lambert": (2009,), # rose to fame after american idol
        "Bangtan Boys / BTS": (2010,), # formed in
        "EXO": (2012,), # debut in 
        "Fall Out Boy": (2001,), # formed in
        "Fifth Harmony": (2012,2018), # years active
        "Hatsune Miku / Vocaloid | 初音ミク / ボーカロイド": (2007,), # released in
        "KAT-TUN": (2001,),
        "MIRROR": (2018,),
        "My Chemical Romance": (2001,),
        "NCT": (2016,),
        "One Direction": (2010,2016),
        "Panic! at the Disco": (2004,2023),
        "Red Velvet": (2014,),
        "Stray Kids": (2017,),
        "TOMORROW X TOGETHER / TXT": (2019,),
        "Twenty One Pilots": (2009,),
    }
}

def add_instances_and_dates(input_list):
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
        if fandom in fandom_instances: # all fandoms that aren't in adaptations or other fandoms
            instance_list = fandom_instances[fandom]

            if fandom in ["Marvel", "DC", "Star Wars Universe"]:
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

            elif fandom in ["Figure Skating","Hockey"]: # RPF where ppl are from diff countries
                for real_human in instance_list:
                    new_dict = deepcopy(fandom_dict)
                    new_dict["instance"] = real_human
                    new_list.append(new_dict)

            else: 
                for item in instance_list:
                    new_dict = deepcopy(fandom_dict)
                    new_dict["instance"] = item[0]
                    new_dict["start_date"] = item[1]
                    if len(item) == 3:
                        new_dict["end_date"] = item[2]
                    else: new_dict["end_date"] = item[1]

                    new_list.append(new_dict)

        elif fandom in fandom_instances["adaptations"]:
            instance_list = fandom_instances["adaptations"][fandom]

            for item in instance_list:
                new_dict = deepcopy(fandom_dict)
                new_dict["instance"] = item[0]
                new_dict["start_date"] = item[1]
                if len(item) == 3:
                    new_dict["end_date"] = item[2]
                else: new_dict["end_date"] = item[1]

                new_list.append(new_dict)

        elif fandom in fandom_instances["other_fandoms"]:
            item = fandom_instances["other_fandoms"][fandom] # cause each fandom only has one item

            new_dict = deepcopy(fandom_dict)

            if type(item[0]) == str: # if we have an instance name
                new_dict["instance"] = item[0]
                new_dict["start_date"] = item[1]
                if len(item) == 3:
                    new_dict["end_date"] = item[2]
                else: new_dict["end_date"] = item[1]
            else: # otherwise only dates
                new_dict["start_date"] = item[0]
                if len(item) == 3:
                    new_dict["end_date"] = item[1]
                else: new_dict["end_date"] = item[0]

            new_list.append(new_dict)

        elif fandom == "Youtube": # bc they're from diff countries etc
            char_df = make_characters_df()
            youtube_df = char_df.where(char_df["fandom"] == "Youtube").dropna(how="all")
            youtuber_list = sorted(list(youtube_df["full_name"]))

            for youtuber in youtuber_list:
                new_dict = deepcopy(fandom_dict)
                new_dict["instance"] = youtuber

                new_list.append(new_dict) # appending a dict for each youtuber

        elif fandom in fandom_instances["music"]:
            item = fandom_instances["music"][fandom] # cause each fandom only has one item

            new_dict = deepcopy(fandom_dict)

            new_dict["start_date"] = item[0]
            if len(item) == 2:
                new_dict["end_date"] = item[1]
            else: new_dict["end_date"] = "current"

            new_list.append(new_dict)

        # check what other stuff may need instances!

        else: # if no instances or dates need to be added, we add unchanged dict
            #print(f'"{fandom}",')
            new_list.append(fandom_dict)

    return new_list
