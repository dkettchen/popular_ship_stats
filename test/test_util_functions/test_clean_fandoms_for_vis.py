from visualisation.vis_utils.clean_fandoms_for_vis import clean_fandoms
from string import whitespace, ascii_letters, punctuation, digits

def test_returns_list():
    test_list = ["My Hero Academia | 僕のヒーローアカデミア"]
    result = clean_fandoms(test_list)
    assert type(result) == list

def test_does_not_mutate_input():
    test_list = ["My Hero Academia | 僕のヒーローアカデミア"]
    clean_fandoms(test_list)
    assert test_list == ["My Hero Academia | 僕のヒーローアカデミア"]

def test_returns_items_ending_in_universe_with_ending_removed():
    test_list = [
        "A Song of Ice and Fire / Game of Thrones Universe", 
        "Avatar: The last Airbender Universe", 
        "Lord of the Rings Universe", 
        "Vampire Diaries Universe"
    ]
    result = clean_fandoms(test_list)
    for item in result:
        assert "Universe" not in item

def test_with_the_exception_of_steven_universe():
    test_list = ["Steven Universe", "Vampire Diaries Universe"]
    result = clean_fandoms(test_list)
    assert result == ["Steven Universe", "Vampire Diaries"]

def test_removes_translations():
    test_list = [
        "My Hero Academia | 僕のヒーローアカデミア",
        "Haikyuu!! | ハイキュー!!",
        "Genshin Impact | 原神",
    ]
    result = clean_fandoms(test_list)
    for item in result:
        assert "|" not in item
        for letter in item:
            assert letter in whitespace or \
                letter in ascii_letters or \
                letter in punctuation or \
                letter in digits
            
def test_shortens_relevant_fandoms():
    test_list = [
        "My Hero Academia | 僕のヒーローアカデミア",
        "Bangtan Boys / BTS",
        "A Song of Ice and Fire / Game of Thrones Universe",
        "Avatar: The last Airbender Universe",
        "Puella Magi Madoka Magica | 魔法少女まどか☆マギカ",
        "She-Ra and the Princesses of Power",
        "Pretty Guardian Sailor Moon | 美少女戦士セーラームーン",
        "The Locked Tomb / Gideon the Ninth",
        "American Horror Story",
        "Chilling Adventures of Sabrina",
        "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令",
        "Hatsune Miku / Vocaloid | 初音ミク / ボーカロイド",
        "Hunger Games / Panem Universe",
        "JoJo's Bizarre Adventure | ジョジョの奇妙な冒険",
        "Lord of the Rings Universe",
        "Miraculous: Tales of Ladybug & Cat Noir | Miraculous: Les Aventures de Ladybug et Chat Noir",
        "Mobile Suit Gundam Wing | 新機動戦記ガンダム W",
        "TOMORROW X TOGETHER / TXT",
        "Teenage Mutant Ninja Turtles"
    ]
    result = clean_fandoms(test_list)
    assert result == [
        "MHA",
        "BTS",
        "GoT",
        "ATLA",
        "Madoka",
        "She-Ra",
        "Sailor Moon",
        "The Locked Tomb",
        "AHS",
        "Sabrina",
        "The Untamed",
        "Vocaloid",
        "Hunger Games",
        "JJBA",
        "LotR",
        "Miraculous",
        "Gundam",
        "TXT",
        "TMNT"
    ]

