from visualisation.input_data_code.make_joined_ranking_df import make_joined_ranking_df
from visualisation.vis_utils.remove_member_columns import remove_members_from_df
from visualisation.vis_utils.join_member_info import join_character_info_to_df
from visualisation.vis_utils.make_colour_lookup import make_colour_lookup
from visualisation.input_data_code.make_general_data import (
    get_counts,
    get_gender_combos,
    get_by_gender_combo,
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
from visualisation.input_data_code.make_by_gender_combo import make_by_gender_combo
from visualisation.input_data_code.make_average_rank import average_rank
from visualisation.diagram_code.visualise_pies import (
    visualise_pies, 
    visualise_market_share_and_popularity
)
from visualisation.diagram_code.visualise_bars import (
    visualise_grouped_bars, 
    visualise_non_white_counts
)
from visualisation.diagram_code.visualise_lines import (
    visualise_multi_lines, 
    visualise_line
)
from visualisation.diagram_code.visualise_tables import (
    visualise_top_5,
    visualise_hottest_chars,
    visualise_single_table,
    visualise_column_tables
)


# get data & turn into big df ✅
ship_joined_annual_df = make_joined_ranking_df("annual")

# make useable dfs ✅
annual_ship_info_df = remove_members_from_df(ship_joined_annual_df)
annual_character_info_df = join_character_info_to_df(ship_joined_annual_df)

# make fandom colour dict: ✅
colour_lookup_dict = make_colour_lookup(annual_ship_info_df)


# make items to be visualised:


## general & intersectional stuff

# how much gen vs slash (total) ✅
gen_vs_slash_total_dict = get_counts(annual_ship_info_df, "fic_type", "ship")
gen_vs_slash_pies = visualise_pies(gen_vs_slash_total_dict, "fic_type", "annual")
gen_vs_slash_pies.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_fic_type_2016_2023.png", 
    width=1000, 
    height=600, 
    scale=2
)
# how much gen vs slash (by gender combo) ✅
gen_vs_slash_by_gender_combo = get_by_gender_combo(annual_ship_info_df, "fic_type")
gen_by_combo_fig = visualise_grouped_bars(gen_vs_slash_by_gender_combo, "gen", "annual")
gen_by_combo_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_general_fic_by_gender_combo_2016_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)

# how much rpf vs fic (total) ✅
rpf_total_dict = get_rpf(annual_ship_info_df)
rpf_fig = visualise_pies(rpf_total_dict, "rpf", "annual")
rpf_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_rpf_2016_2023.png", 
    width=1000, 
    height=600, 
    scale=2
)
# how much rpf vs fic (by gender combo) ✅
rpf_by_gender_combo = get_by_gender_combo(annual_ship_info_df, "rpf_or_fic")
rpf_by_combo_fig = visualise_grouped_bars(rpf_by_gender_combo, "rpf", "annual")
rpf_by_combo_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_rpf_by_gender_combo_2016_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)


# fandom market share by numbers ✅
market_share_dict = fandom_market_share_by_year(annual_ship_info_df) 
market_share_fig = visualise_market_share_and_popularity(market_share_dict, colour_lookup_dict, "annual")
market_share_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_fandom_market_share_2016_2023.png",
    width=2500, 
    height=1300, 
    scale=2
)

# fandom market share by rank popularity ✅
popularity_dict = fandoms_popularity_by_year(annual_ship_info_df) 
popularity_fig = visualise_market_share_and_popularity(popularity_dict, colour_lookup_dict, "annual")
popularity_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_fandom_popularity_2016_2023.png",
    width=2500, 
    height=1300, 
    scale=2
)

# fandom market share by works no? 🔴

# top 5 fandoms ✅
top_5_fandoms_dict = top_5_fandoms_by_year(market_share_dict, popularity_dict) 
top_5_fandoms_fig = visualise_top_5(top_5_fandoms_dict, "fandoms", "annual")
top_5_fandoms_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_top_fandoms_2016_2023.png",
    width=2000, 
    height=500, 
    scale=2
)


# top 10 ships (total) ✅
top_10_ships_dict = top_ships(annual_ship_info_df, "annual")
top_10_ships_fig = visualise_top_5(top_10_ships_dict, "pairings", "annual")
    # either tables or race categories as a diagram
top_10_ships_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/top_annual_ships_2016_2023.png", 
    width=2600, 
    height=2000, 
    scale=2
)

# top 10 ships (by gender combo) (for the straights pls) ✅
top_ships_by_gender_combo = make_by_gender_combo(annual_ship_info_df, "top_ships", "annual")
top_ships_by_gender_combo_fig = visualise_column_tables(top_ships_by_gender_combo, "gender_combos", "annual")
top_ships_by_gender_combo_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/top_annual_ships_by_gender_combo_2016_2023.png", 
    width=3300, 
    height=2850, 
    scale=2
)

# all time top 5 ships by no of appearances in top 10 ✅
# all time top 5 ships by longest streak in top 10 ✅ # they're the same again
appearances_ranking = count_appearances(top_10_ships_dict, "annual")
streak_ranking = count_streaks(top_10_ships_dict)
longest_running_top_5 = longest_running_top_ships(appearances_ranking, streak_ranking, "annual") 
longest_running_fig = visualise_single_table(longest_running_top_5, "annual", "longest_streak")
longest_running_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/longest_running_annual_ships_2016_2023.png", 
    width=950, 
    height=450, 
    scale=2
)

# all time top 100 most popular ships by rank numbers ✅
most_popular_ships_df = most_popular_ships(annual_ship_info_df, "annual")
most_popular_ships_fig = visualise_single_table(most_popular_ships_df, "annual", "most_popular_characters")
most_popular_ships_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/most_popular_annual_ships_2016_2023.png", 
    width=1400, 
    height=2270, 
    scale=2
)
# make some pie charts too! about gender distr, race distr, rpf & fic ✅
most_popular_demo_fig = visualise_pies(most_popular_ships_df, "most_popular_ships", "annual")
most_popular_demo_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/most_popular_annual_ships_demo_2016_2023.png", 
    width=1500, 
    height=600, 
    scale=2
)


# hottest characters ✅
hottest_chars = hottest_char(annual_character_info_df, "annual")
    # possibly another chart abt how many chars were in how many ships over the years
visualise_hottest_chars(hottest_chars, "annual") # writes its own files

## gender stuff

# gender percentages total ✅
gender_percent_total = get_counts(annual_character_info_df, "gender", "full_name")
gender_percent_pies = visualise_pies(gender_percent_total, "gender", "annual")
gender_percent_pies.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_gender_charts/annual_gender_distr_2016_2023.png", 
    width=1000, 
    height=600, 
    scale=2
)
# gender minorities (same info, second diagram) ✅
gender_percent_pies = visualise_grouped_bars(gender_percent_total, "minority_genders", "annual")
gender_percent_pies.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_gender_charts/annual_minority_genders_2016_2023.png", 
    width=1500, 
    height=600, 
    scale=2
)


# gender combos total ✅
total_gender_combos = get_gender_combos(annual_ship_info_df)
gender_combo_pies = visualise_grouped_bars(total_gender_combos, "gender_combos", "annual")
gender_combo_pies.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_gender_charts/annual_gender_combos_2016_2023.png", 
    width=1700, 
    height=600, 
    scale=2
)
# gender combo minorities (same info, second diagram) ✅
gender_minority_combo_pies = visualise_grouped_bars(total_gender_combos, "minority_gender_combos", "annual")
gender_minority_combo_pies.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_gender_charts/annual_minority_gender_combos_2016_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)

# average rank by char gender ✅
average_rank_by_gender = average_rank(annual_character_info_df, "gender")
average_rank_by_gender_fig = visualise_multi_lines(average_rank_by_gender, "average_by_label", "annual")
average_rank_by_gender_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_gender_charts/annual_avg_rank_by_gender_2016_2023.png", 
    width=800, 
    height=600, 
    scale=2
)

# average rank by ship gender combo ✅
average_rank_by_gender_combo = average_rank(annual_ship_info_df, "gender_combo")
average_rank_by_gender_combo_fig = visualise_multi_lines(average_rank_by_gender_combo, "average_by_label", "annual")
average_rank_by_gender_combo_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_gender_charts/annual_avg_rank_by_gender_combo_2016_2023.png", 
    width=800, 
    height=600, 
    scale=2
)


## race stuff

# race percentages total ✅
race_percent_total = get_counts(annual_character_info_df, "race", "full_name")
race_percent_pies = visualise_pies(race_percent_total, "race", "annual")
race_percent_pies.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_racial_distr_2016_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)
# race minorities (same info, second diagram) ✅
# for year in race_percent_total:
#     year_df = race_percent_total[year].copy()
#     year_race_fig = visualise_stacked_bars(year_df, "minority_racial_groups", "annual")
#     year_race_fig.write_image(
#         f"visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/racial_minorities_by_year/annual_minority_racial_distr_{year}.png", 
#         width=1200, 
#         height=600, 
#         scale=2
#     )
race_minority_lines = visualise_multi_lines(race_percent_total, "minority_racial_groups", "annual")
race_minority_lines.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_minority_racial_distr_2016_2023.png", 
    width=1000, 
    height=600, 
    scale=2
)

# race combo totals ✅
race_combo_total = get_counts(annual_ship_info_df, "race_combo", "ship")
race_combo_pies = visualise_pies(race_combo_total, "race_combos", "annual")
race_combo_pies.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_racial_combos_2016_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)

# multi racial characters totals ✅
multi_total = total_multi_nos_by_year(race_percent_total, "race")
multi_fig = visualise_pies(multi_total, "multi_chars", "annual")
multi_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_multi_characters_2016_2023.png", 
    width=1000, 
    height=600, 
    scale=2
)
multi_line = visualise_line(multi_total, "multi_chars", "annual")
multi_line.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_multi_characters_line_2016_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

# multi racial involved ships totals ✅
multi_involved_total = total_multi_nos_by_year(race_combo_total, "race_combo")
multi_involved_fig = visualise_pies(multi_involved_total, "multi_char_ships", "annual")
multi_involved_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_multi_involved_ships_2016_2023.png", 
    width=1000, 
    height=600, 
    scale=2
)
multi_involved_line = visualise_line(multi_involved_total, "multi_char_ships", "annual")
multi_involved_line.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_multi_involved_ships_line_2016_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

# interracial ships ✅
interracial_total = total_interracial_ratio(race_combo_total)
interracial_fig = visualise_pies(interracial_total, "interracial_ships", "annual")
interracial_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_interracial_ships_2016_2023.png", 
    width=1000, 
    height=600,
    scale=2
)
interracial_line = visualise_multi_lines(interracial_total, "interracial_ships", "annual")
interracial_line.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_interracial_ships_line_2016_2023.png", 
    width=800, 
    height=500, 
    scale=2
)

# total racial groups ✅
no_of_racial_groups = total_racial_groups(race_percent_total)
total_group_fig = visualise_line(no_of_racial_groups, "total_racial_groups", "annual")
total_group_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_total_racial_groups_2016_2023.png", 
    width=700, 
    height=600, 
    scale=2
)

# non-white categories: ✅
# total nos each year ✅
annual_prepped_dict = prep_df_for_non_white_ship_comp(annual_ship_info_df)
non_white_counts = count_non_white_ships(annual_prepped_dict)
non_white_count_fig = visualise_non_white_counts(non_white_counts, "annual")
non_white_count_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_non_white_counts_2016_2023.png", 
    width=900, 
    height=400, 
    scale=2
)

# top 3 ships for each category that year ✅
annual_separated_dict = separate_out_non_white_ships_info(annual_prepped_dict)
top_non_white = top_non_white_ships(annual_separated_dict)
top_non_white_fig = visualise_column_tables(top_non_white, "non_white_ships", "annual")
top_non_white_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_top_non_white_2016_2023.png", 
    width=3500, 
    height=1500, 
    scale=2
)

# average ranking by category ✅
average_non_white_rank = average_non_white_ranking(annual_separated_dict)
average_non_white_fig = visualise_multi_lines(average_non_white_rank, "non_white_ships", "annual")
average_non_white_fig.write_image(
    "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts/annual_racial_charts/annual_avg_non_white_2016_2023.png", 
    width=800, 
    height=500, 
    scale=2
)
