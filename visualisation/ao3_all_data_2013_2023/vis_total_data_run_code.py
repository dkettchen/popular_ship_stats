from visualisation.vis_utils.read_csv_to_df import df_from_csv
from visualisation.ao3_all_data_2013_2023.vis_characters_file import (
    total_chars_df,
    all_characters_gender_df,
    average_gender_per_fandom_df,
    all_characters_racial_groups_df,
    make_racial_diversity_df,
    plural_vs_monoracial_fandoms_df,
    highest_racial_diversity_df,
    average_racial_diversity_df,
    visualise_gender_totals,
    visualise_gender_minorities,
    visualise_racial_group_totals,
    visualise_racial_minority_totals,
    visualise_racial_diversity,
    visualise_highest_racial_diversity,
)
from visualisation.ao3_all_data_2013_2023.vis_chars_and_ships import (
    make_full_chars_df, 
    make_hottest_char_df,
    visualise_hottest_characters
)
from visualisation.ao3_all_data_2013_2023.vis_ships_file import (
    total_gender_combo_percent_df,
    fandom_market_share_srs,
    ship_per_fandom_by_type_df,
    total_gender_combos_srs,
    highest_of_this_type_df,
    average_gender_combo_srs,
    total_race_combo_df,
    interracial_srs,
    non_white_ships_srs,
    rpf_fic_df,
    visualise_gender_combo_total,
    visualise_gender_combo_minorities,
    visualise_fandom_market_share,
    visualise_no_half_only,
    visualise_top_3_per_fandom_df,
    visualise_average_ship_combos_per_fandom,
    visualise_interracial_ships,
    visualise_non_white_ships,
    visualise_rpf_fic,
)

# read from char file make a df
characters_df = df_from_csv("data/fifth_clean_up_data/stage_5_characters.csv")

total_characters = total_chars_df(characters_df)

total_gender_percentages = all_characters_gender_df(characters_df)
total_genders_fig = visualise_gender_totals(total_gender_percentages)
total_genders_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_characters_gender_distr_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

minority_genders_fig = visualise_gender_minorities(total_gender_percentages)
minority_genders_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_characters_gender_minorities_2013_2023.png", 
    width=1100, 
    height=420, 
    scale=2
)

average_gender_df = average_gender_per_fandom_df(characters_df)

total_race_percentages = all_characters_racial_groups_df(characters_df)
total_race_groups_fig = visualise_racial_group_totals(total_race_percentages)
total_race_groups_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_characters_all_racial_groups_2013_2023.png", 
    width=800, 
    height=600, 
    scale=2
)

total_racial_minority_fig = visualise_racial_minority_totals(total_race_percentages)
total_racial_minority_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_characters_racial_groups_excl_white_n_ea_2013_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)

racial_div_by_fandom = make_racial_diversity_df(characters_df)

plural_vs_monoracial_fandoms = plural_vs_monoracial_fandoms_df(characters_df, racial_div_by_fandom)
plural_vs_monoracial_fig = visualise_racial_diversity(plural_vs_monoracial_fandoms)
plural_vs_monoracial_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_fandoms_with_one_v_multi_groups_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

highest_racial_div = highest_racial_diversity_df(racial_div_by_fandom)
highest_racial_div_fig = visualise_highest_racial_diversity(highest_racial_div)
highest_racial_div_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_fandoms_top_racial_diversity_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

average_racial_div = average_racial_diversity_df(racial_div_by_fandom)

full_character_df = make_full_chars_df()
hottest_rank_df = make_hottest_char_df(full_character_df)
hottest_rank_fig = visualise_hottest_characters(hottest_rank_df)
hottest_rank_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/all_ao3_hottest_characters_ranking_2013_2023.png", 
    width=1000, 
    height=1200, 
    scale=2
)

# read from ships file make a df
ships_df = df_from_csv("data/fifth_clean_up_data/stage_5_ships.csv")

total_gender_percentages = total_gender_combo_percent_df(ships_df)
total_gender_percent_fig = visualise_gender_combo_total(total_gender_percentages)
total_gender_percent_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_ranked_ships_gender_combos_2013_2023.png", 
    width=600, 
    height=400, 
    scale=2
)

minority_gender_combos_fig = visualise_gender_combo_minorities(total_gender_percentages)
minority_gender_combos_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_ranked_ships_minority_gender_combos_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)

fandom_market_share = fandom_market_share_srs(ships_df)
fandom_market_share_fig = visualise_fandom_market_share(fandom_market_share)
fandom_market_share_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/all_ao3_ranked_ships_fandom_market_share_2013_2023.png", 
    width=800, 
    height=650, 
    scale=2
)

ships_per_fandom_by_type = ship_per_fandom_by_type_df(ships_df)

total_gender_combos_series = total_gender_combos_srs(ships_per_fandom_by_type)
total_gender_combos_fig = visualise_no_half_only(total_gender_combos_series)
total_gender_combos_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_with_no_over_half_only_by_ship_type_2013_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)

highest_of_type_df = highest_of_this_type_df(ships_per_fandom_by_type)
highest_of_type_fig = visualise_top_3_per_fandom_df(highest_of_type_df)
highest_of_type_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_top_3_by_ship_type_no_2013_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)

average_gender_combo_per_fandom_series = average_gender_combo_srs(ships_per_fandom_by_type)
average_gender_combo_fig = visualise_average_ship_combos_per_fandom(average_gender_combo_per_fandom_series)
average_gender_combo_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_average_no_of_ships_by_type_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

total_race_combo_counts = total_race_combo_df(ships_df)

interracial_ships_counts = interracial_srs(total_race_combo_counts)
interracial_fig = visualise_interracial_ships(interracial_ships_counts)
interracial_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_ranked_ships_interracial_percent_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

non_white_ships_counts = non_white_ships_srs(total_race_combo_counts)
non_white_fig = visualise_non_white_ships(non_white_ships_counts)
non_white_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_ranked_ships_non_white_ships_2013_2023.png", 
    width=800, 
    height=500, 
    scale=2
)

rpf_vs_fic_df = rpf_fic_df(ships_df)
rpf_fig = visualise_rpf_fic(rpf_vs_fic_df)
rpf_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/all_ao3_ranked_ships_rpf_vs_fic_2013_2023.png", 
    width=600, 
    height=400, 
    scale=2
)

