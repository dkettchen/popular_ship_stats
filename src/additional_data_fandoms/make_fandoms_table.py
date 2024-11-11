from prep_unique_fandoms import make_unique_fandom_list
from add_media_types import add_media_types
from add_countries_and_languages import add_countries_of_origin_and_languages
from src.util_functions.write_csv_file import make_csv_file
from prep_for_csv import list_of_dicts_to_list_of_lists

# run maker code
fandoms_list = make_unique_fandom_list()

# with_instances = add_instances_and_dates(fandoms_list)
with_media_types = add_media_types(fandoms_list)
final_fandoms_list = add_countries_of_origin_and_languages(with_media_types)

# need to make a list of lists, not list of dicts!
key_list = [
    "fandom",
    "media_type",
    "country_of_origin",
    "original_language"
]
prepped_list = list_of_dicts_to_list_of_lists(final_fandoms_list, key_list)

# write to csv file
csv_fandom_filepath = "data/reference_and_test_files/additional_data/additiona_fandoms_data.csv"
make_csv_file(prepped_list, csv_fandom_filepath)
