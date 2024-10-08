from visualisation.vis_utils.remove_member_columns import remove_members_from_df
from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup
from visualisation.ao3_femslash_rankings_2014_2023.vis_femslash_ranking_utils import (
    make_joined_femslash_df
)
from visualisation.ao3_femslash_rankings_2014_2023.vis_femslash_ranking_general_stat_code import (
    fandom_market_share_by_year,
    fandoms_popularity_by_year,
    top_5_fandoms_by_year,
    rpf_vs_fic,
    top_5_ships,
    count_appearances,
    count_streaks,
    longest_running_top_5_ships,
    hottest_char,
    gender_stats,
)
from visualisation.ao3_femslash_rankings_2014_2023.vis_femslash_ranking_race_stat_code import (
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
from visualisation.ao3_femslash_rankings_2014_2023.vis_femslash_ranking_general_diagram_code import (
    visualise_market_share_and_popularity,
    visualise_top_5_fandoms,
    visualise_rpf_vs_fic,
    visualise_top_5_pairings,
    visualise_longest_running,
    visualise_hottest_sapphic,
    visualise_sapphic_genders,
)
from visualisation.ao3_femslash_rankings_2014_2023.vis_femslash_ranking_race_stat_diagram_code import (
    visualise_total_race_percent,
    visualise_interracial_lines,
    visualise_pies,
    visualise_line,
    visualise_non_white_counts,
    visualise_top_non_white,
    visualise_average_non_white,
)

# get data & turn into big df
ship_joined_femslash_df = make_joined_femslash_df()

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
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/fandom_market_share_2014_2023.png", 
    width=1500, 
    height=1500, 
    scale=2
)

popularity_dict = fandoms_popularity_by_year(femslash_ship_info_df) 
popularity_fig = visualise_market_share_and_popularity(popularity_dict, colour_lookup_dict)
popularity_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/fandom_popularity_2014_2023.png", 
    width=1500, 
    height=1500, 
    scale=2
)

top_5_fandoms_dict = top_5_fandoms_by_year(market_share_dict, popularity_dict) 
top_5_fandoms_fig = visualise_top_5_fandoms(top_5_fandoms_dict)
top_5_fandoms_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/top_femslash_fandoms_2014_2023.png", 
    width=1300, 
    height=700, 
    scale=2
)

rpf_or_fic_dict = rpf_vs_fic(femslash_ship_info_df) 
rpf_fig = visualise_rpf_vs_fic(rpf_or_fic_dict)
rpf_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/femslash_rpf_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)

top_5_ships_dict = top_5_ships(femslash_ship_info_df)
top_5_ships_fig = visualise_top_5_pairings(top_5_ships_dict)
    # either tables or race categories as a diagram
top_5_ships_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/top_femslash_ships_2014_2023.png", 
    width=875, 
    height=1770, 
    scale=2
)

appearances_ranking = count_appearances(top_5_ships_dict)
streak_ranking = count_streaks(top_5_ships_dict)
longest_running_top_5 = longest_running_top_5_ships(appearances_ranking, streak_ranking) 
longest_running_fig = visualise_longest_running(longest_running_top_5)
longest_running_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/longest_running_femslash_ships_2014_2023.png", 
    width=680, 
    height=320, 
    scale=2
)

hottest_wlw = hottest_char(femslash_character_info_df)
    # possibly another chart abt how many chars were in how many ships over the years
visualise_hottest_sapphic(hottest_wlw) # writes its own files

sapphic_genders = gender_stats(femslash_character_info_df)
gender_fig = visualise_sapphic_genders(sapphic_genders)
gender_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/femslash_genders_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)


## race stats

femslash_race_percent = total_racial_group_nos_by_year(femslash_character_info_df)
femslash_race_fig = visualise_total_race_percent(femslash_race_percent)
femslash_race_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_racial_groups_percent_2014_2023.png", 
    width=1500, 
    height=1500, 
    scale=2
)

femslash_race_combo_percent = total_racial_combo_nos_by_year(femslash_ship_info_df)
femslash_race_combo_fig = visualise_total_race_percent(femslash_race_combo_percent)
femslash_race_combo_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_racial_groups_combo_percent_2014_2023.png", 
    width=1500, 
    height=1500, 
    scale=2
)

total_multi = total_multi_chars(femslash_race_percent)
multi_fig = visualise_pies(total_multi)
multi_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_multiracial_chars_pies_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)
multi_line = visualise_line(total_multi)
multi_line.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_multiracial_chars_line_2014_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

total_groups = total_racial_groups(femslash_race_percent)
total_group_fig = visualise_line(total_groups)
total_group_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_racial_groups_2014_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

total_interracial = total_interracial_ratio(femslash_race_combo_percent)
interracial_fig = visualise_pies(total_interracial)
interracial_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_interracial_pies_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)
interracial_line = visualise_interracial_lines(total_interracial)
interracial_line.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_interracial_lines_2014_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

total_multi_involved = total_multi_involved_ratio(femslash_race_combo_percent)
multi_involved_fig = visualise_pies(total_multi_involved)
multi_involved_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_multi_involved_ships_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)
multi_involved_lines = visualise_line(total_multi_involved)
multi_involved_lines.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_multi_involved_ships_line_2014_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

femslash_prepped_dict = prep_df_for_non_white_ship_comp(femslash_ship_info_df)
non_white_counts = count_non_white_ships(femslash_prepped_dict)
non_white_count_fig = visualise_non_white_counts(non_white_counts)
non_white_count_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_non_white_counts_2014_2023.png", 
    width=1000, 
    height=400, 
    scale=2
)

femslash_separated_dict = separate_out_non_white_ships_info(femslash_prepped_dict)
top_non_white = top_non_white_ships(femslash_separated_dict)
top_non_white_fig = visualise_top_non_white(top_non_white)
top_non_white_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_top_non_white_2014_2023.png", 
    width=3800, 
    height=1800, 
    scale=2
)

average_non_white_rank = average_non_white_ranking(femslash_separated_dict)
average_non_white_fig = visualise_average_non_white(average_non_white_rank)
average_non_white_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_avg_non_white_2014_2023.png", 
    width=800, 
    height=500, 
    scale=2
)
