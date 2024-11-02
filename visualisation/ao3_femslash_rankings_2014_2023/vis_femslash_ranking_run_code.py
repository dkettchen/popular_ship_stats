from visualisation.vis_utils.remove_member_columns import remove_members_from_df
from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup
from visualisation.input_data_code.make_joined_ranking_df import make_joined_ranking_df
from visualisation.input_data_code.make_general_data import (
    get_by_gender_combo,
    get_counts,
    get_rpf
)
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
from visualisation.input_data_code.make_fandom_data import (
    fandom_market_share_by_year,
    fandoms_popularity_by_year,
    top_5_fandoms_by_year,
)
from visualisation.input_data_code.make_hottest_chars import hottest_char
from visualisation.input_data_code.make_top_ships import (
    top_ships,
    count_appearances,
    count_streaks,
    longest_running_top_ships,
    most_popular_ships,
)
from visualisation.diagram_code.visualise_bars import (
    visualise_non_white_counts, 
    visualise_grouped_bars, 
)
from visualisation.diagram_code.visualise_lines import visualise_line, visualise_multi_lines
from visualisation.diagram_code.visualise_pies import visualise_pies, visualise_market_share_and_popularity
from visualisation.diagram_code.visualise_tables import (
    visualise_single_table, 
    visualise_top_5, 
    visualise_hottest_chars,
    visualise_column_tables
)


# get data & turn into big df
ship_joined_femslash_df = make_joined_ranking_df("femslash")

# make useable dfs
femslash_ship_info_df = remove_members_from_df(ship_joined_femslash_df)
femslash_character_info_df = join_character_info_to_df(ship_joined_femslash_df)

# make fandom colour dict:
colour_lookup_dict = make_colour_lookup(femslash_ship_info_df)


# make items to be visualised:

## general stuff

market_share_dict = fandom_market_share_by_year(femslash_ship_info_df) 
market_share_fig = visualise_market_share_and_popularity(market_share_dict, colour_lookup_dict, "femslash")
market_share_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/fandom_market_share_2014_2023.png", 
    width=1500, 
    height=1500, 
    scale=2
)

popularity_dict = fandoms_popularity_by_year(femslash_ship_info_df) 
popularity_fig = visualise_market_share_and_popularity(popularity_dict, colour_lookup_dict, "femslash")
popularity_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/fandom_popularity_2014_2023.png", 
    width=1500, 
    height=1500, 
    scale=2
)

top_5_fandoms_dict = top_5_fandoms_by_year(market_share_dict, popularity_dict) 
top_5_fandoms_fig = visualise_top_5(top_5_fandoms_dict, "fandoms", "femslash")
top_5_fandoms_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/top_femslash_fandoms_2014_2023.png", 
    width=1300, 
    height=800, 
    scale=2
)

rpf_or_fic_dict = get_rpf(femslash_ship_info_df)
rpf_fig = visualise_pies(rpf_or_fic_dict, "rpf", "femslash")
rpf_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/femslash_rpf_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)
rpf_by_gender_combo = get_by_gender_combo(femslash_ship_info_df, "rpf_or_fic")
rpf_by_combo_fig = visualise_grouped_bars(rpf_by_gender_combo, "rpf", "femslash")
rpf_by_combo_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/femslash_rpf_by_gender_combo_2014_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)


top_5_ships_dict = top_ships(femslash_ship_info_df, "femslash")
top_5_ships_fig = visualise_top_5(top_5_ships_dict, "pairings", "femslash")
    # either tables or race categories as a diagram
top_5_ships_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/top_femslash_ships_2014_2023.png", 
    width=1750,
    height=1100,
    scale=2
)

appearances_ranking = count_appearances(top_5_ships_dict, "femslash")
streak_ranking = count_streaks(top_5_ships_dict)
longest_running_top_5 = longest_running_top_ships(appearances_ranking, streak_ranking, "femslash") 
longest_running_fig = visualise_single_table(longest_running_top_5, "femslash", "longest_streak")
longest_running_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/longest_running_femslash_ships_2014_2023.png", 
    width=680, 
    height=370, 
    scale=2
)

# all time top 100 most popular ships by rank numbers
most_popular_ships_df = most_popular_ships(femslash_ship_info_df, "femslash")
most_popular_ships_fig = visualise_single_table(most_popular_ships_df, "femslash", "most_popular_characters")
most_popular_ships_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/most_popular_femslash_ships_2013_2023.png", 
    width=1200, 
    height=2800, 
    scale=2
)
# make some pie charts too! about gender distr, race distr, rpf & fic
most_popular_demo_fig = visualise_pies(most_popular_ships_df, "most_popular_ships", "femslash")
most_popular_demo_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/most_popular_femslash_ships_demo_2013_2023.png", 
    width=1000, 
    height=500, 
    scale=2
)



hottest_wlw = hottest_char(femslash_character_info_df, "femslash")
    # possibly another chart abt how many chars were in how many ships over the years
visualise_hottest_chars(hottest_wlw, "femslash") # writes its own files

sapphic_genders = get_counts(femslash_character_info_df, "gender", "full_name")
gender_fig = visualise_pies(sapphic_genders, "gender", "femslash")
gender_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/femslash_genders_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)

minority_gender_fig = visualise_grouped_bars(sapphic_genders, "minority_genders", "femslash")
minority_gender_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/femslash_minority_genders_2014_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)


## race stats

femslash_race_percent = get_counts(femslash_character_info_df, "race", "full_name")
femslash_race_fig = visualise_pies(femslash_race_percent, "race", "femslash")
femslash_race_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_racial_groups_percent_2014_2023.png", 
    width=1500, 
    height=1500, 
    scale=2
)

# race minorities (same info, second diagram)
# for year in femslash_race_percent:
#     year_df = femslash_race_percent[year].copy()
#     year_race_fig = visualise_stacked_bars(year_df, "minority_racial_groups", "femslash")
#     year_race_fig.write_image(
#         f"visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/racial_minorities_by_year/femslash_minority_racial_distr_{year}.png", 
#         width=1200, 
#         height=600, 
#         scale=2
#     )
race_minority_lines = visualise_multi_lines(femslash_race_percent, "minority_racial_groups", "femslash")
race_minority_lines.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_minority_racial_distr_2014_2023.png", 
    width=1000, 
    height=600, 
    scale=2
)

femslash_race_combo_percent = get_counts(femslash_ship_info_df, "race_combo", "ship")
femslash_race_combo_fig = visualise_pies(femslash_race_combo_percent, "race_combos", "femslash")
femslash_race_combo_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_racial_groups_combo_percent_2014_2023.png", 
    width=1500, 
    height=1500, 
    scale=2
)

total_multi = total_multi_nos_by_year(femslash_race_percent, "race")
multi_fig = visualise_pies(total_multi, "multi_chars", "femslash")
multi_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_multiracial_chars_pies_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)
multi_line = visualise_line(total_multi, "multi_chars", "femslash")
multi_line.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_multiracial_chars_line_2014_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

total_groups = total_racial_groups(femslash_race_percent)
total_group_fig = visualise_line(total_groups, "total_racial_groups", "femslash")
total_group_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_racial_groups_2014_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

total_interracial = total_interracial_ratio(femslash_race_combo_percent)
interracial_fig = visualise_pies(total_interracial, "interracial_ships", "femslash")
interracial_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_interracial_pies_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)
interracial_line = visualise_multi_lines(total_interracial, "interracial_ships", "femslash")
interracial_line.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_interracial_lines_2014_2023.png", 
    width=800, 
    height=500, 
    scale=2
)

total_multi_involved = total_multi_nos_by_year(femslash_race_combo_percent, "race_combo")
multi_involved_fig = visualise_pies(total_multi_involved, "multi_char_ships", "femslash")
multi_involved_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_multi_involved_ships_2014_2023.png", 
    width=700, 
    height=650, 
    scale=2
)
multi_involved_lines = visualise_line(total_multi_involved, "multi_char_ships", "femslash")
multi_involved_lines.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_multi_involved_ships_line_2014_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

femslash_prepped_dict = prep_df_for_non_white_ship_comp(femslash_ship_info_df)
non_white_counts = count_non_white_ships(femslash_prepped_dict)
non_white_count_fig = visualise_non_white_counts(non_white_counts, "femslash")
non_white_count_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_non_white_counts_2014_2023.png", 
    width=1000, 
    height=400, 
    scale=2
)

femslash_separated_dict = separate_out_non_white_ships_info(femslash_prepped_dict)
top_non_white = top_non_white_ships(femslash_separated_dict)
top_non_white_fig = visualise_column_tables(top_non_white, "non_white_ships", "femslash")
top_non_white_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_top_non_white_2014_2023.png", 
    width=3800, 
    height=1800, 
    scale=2
)

average_non_white_rank = average_non_white_ranking(femslash_separated_dict)
average_non_white_fig = visualise_multi_lines(average_non_white_rank, "non_white_ships", "femslash")
average_non_white_fig.write_image(
    "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts/sapphic_race_stats/femslash_avg_non_white_2014_2023.png", 
    width=800, 
    height=500, 
    scale=2
)
