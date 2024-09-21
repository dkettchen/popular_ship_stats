from visualisation.vis_utils.make_file_dfs import make_femslash_dfs
from visualisation.vis_utils.remove_member_columns import remove_members_from_df
from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup
from visualisation.ao3_femslash_rankings_2013_2023.vis_femslash_ranking_utils import (
    edit_femslash_df_columns, join_ship_info_to_femslash
)
from visualisation.ao3_femslash_rankings_2013_2023.vis_femslash_ranking_general_stat_code import (
    fandom_market_share_by_year,
    fandoms_popularity_by_year,
    top_5_fandoms_by_year,
    rpf_vs_fic,
    top_5_wlw,
    count_appearances,
    count_streaks,
    longest_running_top_5_ships,
    hottest_sapphic,
    sapphic_gender_stats,
)
from visualisation.ao3_femslash_rankings_2013_2023.vis_femslash_ranking_race_stat_code import (
    total_racial_group_nos_by_year,
    total_multi_chars,
    total_racial_groups,
    total_racial_combo_nos_by_year,
    total_interracial_ratio,
    total_multi_involved_ratio,
    prep_df_for_non_white_ship_comp,
    count_non_white_ships,
    separate_out_non_white_ships_info,
    top_non_white_ships,
    average_non_white_ranking,
)
from visualisation.ao3_femslash_rankings_2013_2023.vis_femslash_ranking_diagram_code import (
    visualise_market_share_and_popularity,
)

# get data
femslash_df_dict = make_femslash_dfs()

# fix columns
new_femslash_df_dict = edit_femslash_df_columns(femslash_df_dict)
# combine into one big df
ship_joined_femslash_df = join_ship_info_to_femslash(new_femslash_df_dict) 

# make useable dfs
femslash_ship_info_df = remove_members_from_df(ship_joined_femslash_df)
femslash_character_info_df = join_character_info_to_df(ship_joined_femslash_df)

# make fandom colour dict:
colour_lookup_dict = make_colour_lookup(femslash_ship_info_df)

# make items to be visualised:

## general stuff

market_share_dict = fandom_market_share_by_year(femslash_ship_info_df) 
market_share_fig = visualise_market_share_and_popularity(market_share_dict, colour_lookup_dict)
market_share_fig.write_image(
    "visualisation/ao3_femslash_rankings_2013_2023/ao3_femslash_rankings_charts/fandom_market_share_2013_2023.png", 
    width=2200, 
    height=1000, 
    scale=2
)

popularity_dict = fandoms_popularity_by_year(femslash_ship_info_df) 
popularity_fig = visualise_market_share_and_popularity(popularity_dict, colour_lookup_dict)
popularity_fig.write_image(
    "visualisation/ao3_femslash_rankings_2013_2023/ao3_femslash_rankings_charts/fandom_popularity_2013_2023.png", 
    width=2200, 
    height=1000, 
    scale=2
)

top_5_fandoms_dict = top_5_fandoms_by_year(market_share_dict, popularity_dict) 
    # make into tables

rpf_or_fic_dict = rpf_vs_fic(femslash_ship_info_df) 
    # make into pie charts

top_5_ships_dict = top_5_wlw(femslash_ship_info_df)
    # either tables or race categories as a diagram
appearances_ranking = count_appearances(top_5_ships_dict)
streak_ranking = count_streaks(top_5_ships_dict)
longest_running_top_5 = longest_running_top_5_ships(appearances_ranking, streak_ranking) 
    # make into table

hottest_wlw = hottest_sapphic(femslash_character_info_df)
    # needs more futzing before vis
    # make into tables 
    # (rank (all chars of top number or top 2 nums), char name, top ship, per each year)

sapphic_genders = sapphic_gender_stats(femslash_character_info_df)

# race stats

femslash_race_percent = total_racial_group_nos_by_year(femslash_character_info_df)
femslash_race_combo_percent = total_racial_combo_nos_by_year(femslash_ship_info_df)

total_multi = total_multi_chars(femslash_race_percent)
total_groups = total_racial_groups(femslash_race_percent)

total_interracial = total_interracial_ratio(femslash_race_combo_percent)
total_multi_involved = total_multi_involved_ratio(femslash_race_combo_percent)

femslash_prepped_dict = prep_df_for_non_white_ship_comp(femslash_ship_info_df)
non_white_counts = count_non_white_ships(femslash_prepped_dict)

femslash_separated_dict = separate_out_non_white_ships_info(femslash_prepped_dict)
top_non_white = top_non_white_ships(femslash_separated_dict)
average_non_white_rank = average_non_white_ranking(femslash_separated_dict)
    # in 2020 we have non-white-ea ranking highest bc there's a singular ship and they 
    # happened to be 47th in the ranking which was higher than everyone else's averages lmao


