from src.formatting_data import find_paths


class TestFindPaths:
    def test_find_returns_list(self):
        assert type(find_paths("data/raw_data/")) == list

    def test_find_returns_non_empty_list(self):
        assert len(find_paths("data/raw_data/")) > 0

    def test_find_returns_list_of_strings(self):
        for item in find_paths("data/raw_data/"):
            assert type(item) == str
    
    def test_find_returns_data_folder_file_paths(self):
        for item in find_paths("data/raw_data/"):
            assert "data/" in item

    def test_find_returns_expected_file_paths(self):
        assert "data/raw_data/ao3_2023/raw_ao3_2023_data.txt" in find_paths("data/raw_data/")
        assert "data/raw_data/ao3_2013/raw_ao3_2013_fandoms.txt" in find_paths("data/raw_data/")
        assert "data/raw_data/ao3_2016/raw_ao3_2016_femslash_ranking.txt" in find_paths("data/raw_data/")

