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

# get data & turn into big df
ship_joined_overall_df = make_joined_ranking_df("overall")

# make useable dfs
overall_ship_info_df = remove_members_from_df(ship_joined_overall_df)
overall_character_info_df = join_character_info_to_df(ship_joined_overall_df)

# make fandom colour dict:
colour_lookup_dict = make_colour_lookup(overall_ship_info_df)


# make items to be visualised:


## general & intersectional stuff

# how much gen vs slash (total)
gen_vs_slash_total_dict = get_counts(overall_ship_info_df, "fic_type", "ship")
# how much gen vs slash (by gender combo)
gen_vs_slash_by_gender_combo = get_by_gender_combo(overall_ship_info_df, "fic_type")

# how much rpf vs fic (total)
rpf_total_dict = get_rpf(overall_ship_info_df)
rpf_fig = visualise_pies(rpf_total_dict, "rpf", "overall")
rpf_fig.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_rpf_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)

# how much rpf vs fic (by gender combo)
rpf_by_gender_combo = get_by_gender_combo(overall_ship_info_df, "rpf_or_fic")

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

# gender percentages total
gender_percent_total = get_counts(overall_character_info_df, "gender", "full_name")
gender_percent_pies = visualise_pies(gender_percent_total, "gender", "overall")
gender_percent_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_gender_distr_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
# gender minorities (same info, second diagram)

# gender combos total
total_gender_combos = get_gender_combos(overall_ship_info_df)
# gender combo minorities (same info, second diagram)

# average rank by char gender
# average rank by ship gender combo

# top 3 ships by gender combo


## race stuff

# race percentages total
race_percent_total = get_counts(overall_character_info_df, "race", "full_name")
race_percent_pies = visualise_pies(race_percent_total, "race", "overall")
race_percent_pies.write_image(
    "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts/overall_racial_distr_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)
# race minorities (same info, second diagram)

# race combo totals
# race combo minorities (same info, second diagram)

# multi racial characters totals
# multi racial involved ships totals

# interracial ships

# total racial groups

# non-white categories:
    # total nos each year
    # top 3 ships for each category that year
    # average ranking by category

