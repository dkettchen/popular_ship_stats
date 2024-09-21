
# runs stage 1, stage 2, and stage 3 cleaning -> updating files in order after code changes
run-cleaning-1-3:
	python src/first_cleaning_stage_code/run_stage_1_cleaning.py && python src/second_cleaning_stage_code/run_stage_2_cleaning.py && python src/third_cleaning_stage_code/run_third_stage_cleaning.py

# runs collecting_fandoms.py -> updating any of the 3 full_[...].json files in reference data
collect-fandoms:
	python src/fourth_stage_fixing_values_code/collecting_fandoms.py


# updates fourth stage fandom files
update-fandoms:
	python src/fourth_stage_fixing_values_code/unify_fandoms.py && python src/fourth_stage_fixing_values_code/updating_fandom_characters.py

# updates fourth stage character name files
update-names:
	python src/fourth_stage_fixing_values_code/separate_names_into_parts.py && python src/fourth_stage_fixing_values_code/categorise_character_names.py && python src/fourth_stage_fixing_values_code/complete_character_names.py && python src/fourth_stage_fixing_values_code/extracting_clean_abbr_name_lists.py

# updates stage four main files
run-cleaning-4:
	python src/fourth_stage_fixing_values_code/run_stage_4_cleaning.py

# updates demographic info (gender & race tags) -> updates all files in data/reference_and_test_files/assigning_demographic_info/
update-demographics:
	python src/fifth_cleaning_stage_code/collect_gender_tags_per_character.py && python src/fifth_cleaning_stage_code/assign_gender_per_character.py && python src/fifth_cleaning_stage_code/collect_race_tags_per_character.py && python src/fifth_cleaning_stage_code/assign_race_tag_per_character.py


#need to double check notes abt vv these two's syntax

# runs all stage 4 & 5 character updates (names & demo)
update-characters:
	make update-names run-cleaning-4 update-demographics

# runs all fandom & character updates
update-fandoms-and-characters:
	make update-fandoms update-characters

# runs stage 5 cleaning file
run-cleaning-5:
	python src/fifth_cleaning_stage_code/run_stage_5_cleaning.py

# run all "ao3_all_data_2013_2023" vis files to (re)make diagrams
make-ao3-overall-data-charts:
	python visualisation/ao3_all_data_2013_2023/vis_characters_file.py && python visualisation/ao3_all_data_2013_2023/vis_ships_file.py && python visualisation/ao3_all_data_2013_2023/vis_chars_and_ships.py

# run "ao3_femslash_rankings_2013_2023"'s vis file to (re)make diagrams
make-ao3-femslash-charts:
	python visualisation/ao3_femslash_rankings_2014_2023/vis_femslash_ranking_run_code.py
