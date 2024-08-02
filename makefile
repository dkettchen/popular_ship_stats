
# runs stage 1, stage 2, and stage 3 cleaning -> updating files in order after code changes
run-cleaning:
	python src/first_cleaning_stage_code/run_stage_1_cleaning.py && python src/second_cleaning_stage_code/run_stage_2_cleaning.py && python src/third_cleaning_stage_code/run_third_stage_cleaning.py

# runs collecting_fandoms.py -> updating any of the 3 full_[...].json files in reference data
collect-fandoms:
	python src/fourth_stage_fixing_values_code/collecting_fandoms.py