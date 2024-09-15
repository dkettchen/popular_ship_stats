from visualisation.vis_utils.remove_translation import remove_translation
from string import ascii_letters, whitespace, punctuation

def test_returns_string():
    test_fandom = "My Hero Academia | 僕のヒーローアカデミア"
    result = remove_translation(test_fandom)
    assert type(result) == str

def test_returns_new_string():
    test_fandom = "My Hero Academia | 僕のヒーローアカデミア"
    result = remove_translation(test_fandom)
    assert result != test_fandom

def test_does_not_mutate_input():
    test_fandom = "My Hero Academia | 僕のヒーローアカデミア"
    remove_translation(test_fandom)
    assert test_fandom == "My Hero Academia | 僕のヒーローアカデミア"

def test_removes_translation():
    test_fandom = "My Hero Academia | 僕のヒーローアカデミア"
    result = remove_translation(test_fandom)
    assert "|" not in result
    for char in result:
        assert char in ascii_letters or char in whitespace

    test_fandom_2 = "Haikyuu!! | ハイキュー！！"
    result_2 = remove_translation(test_fandom_2)
    assert "|" not in result_2
    for char in result_2:
        assert char in ascii_letters or char in punctuation

def test_keeps_english_title(): # and works with regardless of language
    test_fandom = "Haikyuu!! | ハイキュー！！"
    result = remove_translation(test_fandom)
    assert result == "Haikyuu!!"

    test_fandom_2 = "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令"
    result_2 = remove_translation(test_fandom_2)
    assert result_2 == "Grandmaster of Demonic Cultivation / The Untamed"

    test_fandom_3 = "KinnPorsche | คินน์พอร์ช เดอะ ซีรีส์"
    result_3 = remove_translation(test_fandom_3)
    assert result_3 == "KinnPorsche"
