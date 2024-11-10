from prep_unique_fandoms import make_unique_fandom_list
from add_instances_dates_media_type import add_instances_and_dates, add_media_types
from add_countries_and_languages import add_countries_of_origin_and_languages

# run maker code
fandoms_list = make_unique_fandom_list()

with_instances = add_instances_and_dates(fandoms_list)
with_media_types = add_media_types(with_instances)
final_fandoms_list = add_countries_of_origin_and_languages(with_media_types)

# write to csv file