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
)
from visualisation.ao3_all_data_2013_2023.vis_chars_and_ships import (
    make_full_chars_df, 
    make_hottest_char_df,
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
)
from visualisation.input_data_code.get_data_df import get_data_df
from visualisation.diagram_code.visualise_bars import (
    visualise_stacked_bars,
    visualise_3_grouped_bars,
    visualise_simple_bar,
)
from visualisation.diagram_code.visualise_pies import visualise_single_pie
from visualisation.diagram_code.visualise_tables import visualise_single_table

# read from char file make a df
characters_df = df_from_csv("data/fifth_clean_up_data/stage_5_characters.csv")

total_characters = get_data_df(characters_df, "total_chars")

total_gender_percentages = get_data_df(characters_df, "total_genders")
total_genders_fig = visualise_single_pie(total_gender_percentages, "gender", "total")
total_genders_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_characters_gender_distr_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

minority_genders_fig = visualise_simple_bar(total_gender_percentages, "minority_genders", "total")
minority_genders_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_characters_gender_minorities_2013_2023.png", 
    width=1100, 
    height=420, 
    scale=2
)

average_gender_df = average_gender_per_fandom_df(characters_df)

total_race_percentages = get_data_df(characters_df, "total_racial_groups")
total_race_groups_fig = visualise_single_pie(total_race_percentages, "racial_groups", "total")
total_race_groups_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_characters_all_racial_groups_2013_2023.png", 
    width=800, 
    height=600, 
    scale=2
)

total_racial_minority_fig = visualise_stacked_bars(total_race_percentages, "minority_racial_groups", "total")
total_racial_minority_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_characters_racial_groups_excl_white_n_ea_2013_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)

racial_div_by_fandom = get_data_df(characters_df, "racial_diversity")

plural_vs_monoracial_fandoms = plural_vs_monoracial_fandoms_df(characters_df, racial_div_by_fandom)
plural_vs_monoracial_fig = visualise_single_pie(plural_vs_monoracial_fandoms, "racial_diversity", "total")
plural_vs_monoracial_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_fandoms_with_one_v_multi_groups_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

highest_racial_div = highest_racial_diversity_df(racial_div_by_fandom)
highest_racial_div_fig = visualise_simple_bar(highest_racial_div, "racial_diversity", "total")
highest_racial_div_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_fandoms_top_racial_diversity_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

average_racial_div = average_racial_diversity_df(racial_div_by_fandom)

full_character_df = make_full_chars_df()
hottest_rank_df = make_hottest_char_df(full_character_df)
hottest_rank_fig = visualise_single_table(hottest_rank_df, "total")
hottest_rank_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/all_ao3_hottest_characters_ranking_2013_2023.png", 
    width=1000, 
    height=1200, 
    scale=2
)

# read from ships file make a df
ships_df = df_from_csv("data/fifth_clean_up_data/stage_5_ships.csv")

total_gender_combo_percentages = get_data_df(ships_df, "total_gender_combos")
total_gender_percent_fig = visualise_stacked_bars(total_gender_combo_percentages, "gender_combos", "total")
total_gender_percent_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_ranked_ships_gender_combos_2013_2023.png", 
    width=600, 
    height=400, 
    scale=2
)

minority_gender_combos_fig = visualise_stacked_bars(total_gender_combo_percentages, "minority_gender_combos", "total")
minority_gender_combos_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_ranked_ships_minority_gender_combos_2013_2023.png", 
    width=1300, 
    height=600, 
    scale=2
)

fandom_market_share = fandom_market_share_srs(ships_df)
fandom_market_share_fig = visualise_single_pie(fandom_market_share, "market_share", "total")
fandom_market_share_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/all_ao3_ranked_ships_fandom_market_share_2013_2023.png", 
    width=800, 
    height=650, 
    scale=2
)

ships_per_fandom_by_type = ship_per_fandom_by_type_df(ships_df)

total_gender_combos_series = total_gender_combos_srs(ships_per_fandom_by_type)
total_gender_combos_fig = visualise_3_grouped_bars(total_gender_combos_series, "no_half_only", "total")
total_gender_combos_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_with_no_over_half_only_by_ship_type_2013_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)

highest_of_type_df = highest_of_this_type_df(ships_per_fandom_by_type)
highest_of_type_fig = visualise_3_grouped_bars(highest_of_type_df, "top_fandoms", "total")
highest_of_type_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_top_3_by_ship_type_no_2013_2023.png", 
    width=1200, 
    height=600, 
    scale=2
)

average_gender_combo_per_fandom_series = average_gender_combo_srs(ships_per_fandom_by_type)
average_gender_combo_fig = visualise_simple_bar(average_gender_combo_per_fandom_series, "average_ship_combo", "total")
average_gender_combo_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/gender_diagrams/all_ao3_fandoms_average_no_of_ships_by_type_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

total_race_combo_counts = get_data_df(ships_df, "total_race_combos")

interracial_ships_counts = interracial_srs(total_race_combo_counts)
interracial_fig = visualise_single_pie(interracial_ships_counts, "interracial_ships", "total")
interracial_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_ranked_ships_interracial_percent_2013_2023.png", 
    width=800, 
    height=400, 
    scale=2
)

non_white_ships_counts = non_white_ships_srs(total_race_combo_counts)
non_white_fig = visualise_simple_bar(non_white_ships_counts, "non_white_ships", "total")
non_white_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/racial_groups_diagrams/all_ao3_ranked_ships_non_white_ships_2013_2023.png", 
    width=800, 
    height=500, 
    scale=2
)

rpf_vs_fic_df = get_data_df(ships_df, "rpf")
rpf_fig = visualise_single_pie(rpf_vs_fic_df, "rpf", "total")
rpf_fig.write_image(
    "visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/all_ao3_ranked_ships_rpf_vs_fic_2013_2023.png", 
    width=600, 
    height=400, 
    scale=2
)

