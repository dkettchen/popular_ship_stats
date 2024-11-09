from prep_unique_fandoms import make_unique_fandom_list
from add_instances_dates_media_type import add_instances, add_media_types, add_remaining_dates
from add_countries_and_languages import add_countries_of_origin_and_languages

# run maker code
fandoms_list = make_unique_fandom_list()

with_instances = add_instances(fandoms_list)
with_media_types = add_media_types(with_instances)
with_dates = add_remaining_dates(with_media_types)
final_fandoms_list = add_countries_of_origin_and_languages(with_dates)

# write to csv file