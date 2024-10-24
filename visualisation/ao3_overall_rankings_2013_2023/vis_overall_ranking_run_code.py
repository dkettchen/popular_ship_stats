from visualisation.input_data_code.make_joined_ranking_df import make_joined_ranking_df
from visualisation.vis_utils.remove_member_columns import remove_members_from_df
from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup
from visualisation.ao3_overall_rankings_2013_2023.vis_overall_ranking_general_stat_code import (
    get_counts,
    get_gender_combos,
    get_by_gender_combo,
    get_rpf
)
from visualisation.diagram_code.visualise_pies import visualise_pies
from visualisation.diagram_code.visualise_bars import (
    visualise_grouped_bars, 
    visualise_stacked_bars, 
    visualise_non_white_counts
)
from visualisation.diagram_code.visualise_lines import visualise_multi_lines, visualise_line
from visualisation.diagram_code.visualise_tables import visualise_top_non_white_ships
from visualisation.input_data_code.make_race_data import (
    total_multi_nos_by_year, 
    total_interracial_ratio,
    total_racial_groups,
    prep_df_for_non_white_ship_comp,
    count_non_white_ships,
    separate_out_non_white_ships_info,
    top_non_white_ships,
    average_non_white_ranking,
)

# get data & turn into big df ✅
ship_joined_overall_df = make_joined_ranking_df("overall")

# make useable dfs ✅
overall_ship_info_df = remove_members_from_df(ship_joined_overall_df)
overall_character_info_df = join_character_info_to_df(ship_joined_overall_df)

# make fandom colour dict: ✅
colour_lookup_dict = make_colour_lookup(overall_ship_info_df)


# make items to be visualised:


## general & intersectional stuff

# how much gen vs slash (total) ✅
gen_vs_slash_total_dict = get_counts(overall_ship_info_df, "fic_type", "ship")
gen_vs_slash_pies = visualise_pies(gen_vs_slash_total_dict, "fic_type", "overall")
gen_vs_slash_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_fic_type_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
# how much gen vs slash (by gender combo) ✅
gen_vs_slash_by_gender_combo = get_by_gender_combo(overall_ship_info_df, "fic_type")
gen_by_combo_fig = visualise_grouped_bars(gen_vs_slash_by_gender_combo, "gen", "overall")
gen_by_combo_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_general_fic_by_gender_combo_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)

# how much rpf vs fic (total) ✅
rpf_total_dict = get_rpf(overall_ship_info_df)
rpf_fig = visualise_pies(rpf_total_dict, "rpf", "overall")
rpf_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_rpf_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
# how much rpf vs fic (by gender combo) ✅
rpf_by_gender_combo = get_by_gender_combo(overall_ship_info_df, "rpf_or_fic")
rpf_by_combo_fig = visualise_grouped_bars(rpf_by_gender_combo, "rpf", "overall")
rpf_by_combo_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_rpf_by_gender_combo_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)


# fandom market share by numbers
# fandom market share by rank popularity
# fandom market share by works no?
# top 5 fandoms

# top 10 ships (total)
# top 10 ships (by gender combo)
# all time top 5 ships by no of appearances in top 10
# all time top 5 ships by longest streak in top 10

# hottest characters

# racial distr by char gender
# racial distr by gender combo


## gender stuff

# gender percentages total ✅
gender_percent_total = get_counts(overall_character_info_df, "gender", "full_name")
gender_percent_pies = visualise_pies(gender_percent_total, "gender", "overall")
gender_percent_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_gender_charts/overall_gender_distr_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
# gender minorities (same info, second diagram) ✅
gender_percent_pies = visualise_grouped_bars(gender_percent_total, "minority_genders", "overall")
gender_percent_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_gender_charts/overall_minority_genders_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)


# gender combos total ✅
total_gender_combos = get_gender_combos(overall_ship_info_df)
gender_combo_pies = visualise_grouped_bars(total_gender_combos, "gender_combos", "overall")
gender_combo_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_gender_charts/overall_gender_combos_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
# gender combo minorities (same info, second diagram) ✅
gender_minority_combo_pies = visualise_grouped_bars(total_gender_combos, "minority_gender_combos", "overall")
gender_minority_combo_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_gender_charts/overall_minority_gender_combos_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)


# average rank by char gender
# average rank by ship gender combo

# top 3 ships by gender combo


## race stuff

# race percentages total ✅
race_percent_total = get_counts(overall_character_info_df, "race", "full_name")
race_percent_pies = visualise_pies(race_percent_total, "race", "overall")
race_percent_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_racial_distr_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
# race minorities (same info, second diagram) ✅
# for year in race_percent_total:
#     year_df = race_percent_total[year].copy()
#     year_race_fig = visualise_stacked_bars(year_df, "minority_racial_groups", "overall")
#     year_race_fig.write_image(
#         f"visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/racial_minorities_by_year/overall_minority_racial_distr_{year}.png", 
#         width=1200, 
#         height=600, 
#         scale=2
#     )
race_minority_lines = visualise_multi_lines(race_percent_total, "minority_racial_groups", "overall")
race_minority_lines.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_minority_racial_distr_2013_2023.png", 
    width=1000, 
    height=600, 
    scale=2
)

# race combo totals ✅
race_combo_total = get_counts(overall_ship_info_df, "race_combo", "ship")
race_combo_pies = visualise_pies(race_combo_total, "race_combos", "overall")
race_combo_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_racial_combos_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)

# multi racial characters totals ✅
multi_total = total_multi_nos_by_year(race_percent_total, "race")
multi_fig = visualise_pies(multi_total, "multi_chars", "overall")
multi_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_multi_characters_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
multi_line = visualise_line(multi_total, "multi_chars", "overall")
multi_line.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_multi_characters_line_2013_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

# multi racial involved ships totals ✅
multi_involved_total = total_multi_nos_by_year(race_combo_total, "race_combo")
multi_involved_fig = visualise_pies(multi_involved_total, "multi_char_ships", "overall")
multi_involved_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_multi_involved_ships_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
multi_involved_line = visualise_line(multi_involved_total, "multi_char_ships", "overall")
multi_involved_line.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_multi_involved_ships_line_2013_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

# interracial ships
interracial_total = total_interracial_ratio(race_combo_total)
interracial_fig = visualise_pies(interracial_total, "interracial_ships", "overall")
interracial_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_interracial_ships_2013_2023.png", 
    width=1300, 
    height=600,
    scale=2
)
interracial_line = visualise_multi_lines(interracial_total, "interracial_ships", "overall")
interracial_line.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_interracial_ships_line_2013_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

# total racial groups
no_of_racial_groups = total_racial_groups(race_percent_total)
total_group_fig = visualise_line(no_of_racial_groups, "total_racial_groups", "overall")
total_group_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_total_racial_groups_2013_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

# non-white categories:
    # total nos each year
    # top 3 ships for each category that year
    # average ranking by category

overall_prepped_dict = prep_df_for_non_white_ship_comp(overall_ship_info_df)
non_white_counts = count_non_white_ships(overall_prepped_dict)
non_white_count_fig = visualise_non_white_counts(non_white_counts, "overall")
non_white_count_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_non_white_counts_2013_2023.png", 
    width=1000, 
    height=400, 
    scale=2
)

overall_separated_dict = separate_out_non_white_ships_info(overall_prepped_dict)
top_non_white = top_non_white_ships(overall_separated_dict)
top_non_white_fig = visualise_top_non_white_ships(top_non_white, "overall")
top_non_white_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_top_non_white_2013_2023.png", 
    width=3800, 
    height=1800, 
    scale=2
)

average_non_white_rank = average_non_white_ranking(overall_separated_dict)
average_non_white_fig = visualise_multi_lines(average_non_white_rank, "non_white_ships", "overall")
average_non_white_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_charts/overall_avg_non_white_2013_2023.png", 
    width=800, 
    height=500, 
    scale=2
)
