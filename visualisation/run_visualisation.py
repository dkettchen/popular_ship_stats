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
# our many imports!


# TODO: 
# - refactor femslash version we copied for now ✅
# - take any data functions out of the loop where possible ✅
# - add implementation for overall ✅ & annual ✅ rankings too
#   - custom heights for each ✅
#   - adding items not visualised in femslash ✅
#   - make sure only funcs used by that ranking are run before loops ✅
# - fix filepaths of existing diagrams before running this 
# bc I wanna see that it doesn't mess anything up

def run_ao3_2013_2023_vis(input_rankings:list):
    """
    runs ao3 2013-2023 visualisation for all rankings in the input list

    (currently implemented: "femslash")

    produces png files in the relevant folders
    """

    # iterating over all rankings
    for ranking in input_rankings:

        # setting up file path naming conventions

        # year ranges
        if ranking == "overall":
            year_range = "2013_2023"
        elif ranking == "femslash":
            year_range = "2014_2023"
        elif ranking == "annual":
            year_range = "2016_2023"
        
        # file naming blocks
        ranking_name = f"ao3_{ranking}_rankings"
        main_folder = f"visualisation/{ranking_name}_{year_range}"
        folder = f"{main_folder}/{ranking_name}_charts/{ranking}_"
        # chart's individual title goes inbetween
        suffix = f"_{year_range}.png"


        # input df prep: 

        ship_joined_df = make_joined_ranking_df(ranking)

        # make useable dfs
        ship_info_df = remove_members_from_df(ship_joined_df)
        character_info_df = join_character_info_to_df(ship_joined_df)

        # make fandom colour dict:
        colour_lookup_dict = make_colour_lookup(ship_info_df)


        # items to be visualised:

        # making a dict to collect figure info for file writing later
        stuff_to_visualise = {}

        ## general & intersectional stuff

        general_stuff = [
            "fandom_market_share",
            "fandom_popularity",
            "top_fandoms",
            "rpf",
            "rpf_by_gender_combo",
            "top_ships",
            "longest_running_ships",
            "top_100_most_popular_ships", 
            "top_100_demo"
        ]

        if ranking in ["overall", "annual"]: # adding extra subjects
            general_stuff += [
                "gen_vs_slash_fic",
                "gen_by_gender_combo",
                "top_ships_by_gender_combo",
            ]

        # running all data making code for this portion outside the loop
        market_share_dict = fandom_market_share_by_year(ship_info_df) 
        fandom_popularity_dict = fandoms_popularity_by_year(ship_info_df) 
        top_5_fandoms_dict = top_5_fandoms_by_year(market_share_dict, fandom_popularity_dict) 
        rpf_or_fic_dict = get_rpf(ship_info_df)
        rpf_by_gender_combo_dict = get_by_gender_combo(ship_info_df, "rpf_or_fic")
        top_ships_dict = top_ships(ship_info_df, ranking)
        appearances_ranking_df = count_appearances(top_ships_dict, ranking)
        streak_ranking_df = count_streaks(top_ships_dict)
        longest_running_ships_df = longest_running_top_ships(appearances_ranking_df, streak_ranking_df, ranking) 
        top_100_ships_df = most_popular_ships(ship_info_df, ranking)

        if ranking in ["overall", "annual"]:
            gen_vs_slash_total_dict = get_counts(ship_info_df, "fic_type", "ship")
            gen_vs_slash_by_gender_combo = get_by_gender_combo(ship_info_df, "fic_type")
            top_ships_by_gender_combo = make_by_gender_combo(ship_info_df, "top_ships", ranking)

        # making figures & determining dimensions & adding them to our dict
        for subject in general_stuff:
            # what fandoms have the most ships each year? -> ships summed by fandom for each year
            if subject == "fandom_market_share":
                figure = visualise_market_share_and_popularity(market_share_dict, colour_lookup_dict, ranking)
                if ranking == "femslash":
                    width = 1500
                    height = 1500
                elif ranking == "overall":
                    width=2800
                    height=1300
                elif ranking == "annual":
                    width=2500
                    height=1300
            # ships weighted for rank, summed by fandom for each year
            elif subject == "fandom_popularity":
                figure = visualise_market_share_and_popularity(fandom_popularity_dict, colour_lookup_dict, ranking) 
                if ranking == "femslash":
                    width = 1500
                    height = 1500
                elif ranking == "overall":
                    width=2800
                    height=1300
                elif ranking == "annual":
                    width=2500
                    height=1300
            # top 5 fandoms by number of ships and by popularity each year
            elif subject == "top_fandoms":
                figure = visualise_top_5(top_5_fandoms_dict, "fandoms", ranking)
                if ranking == "femslash":
                    width = 1300 
                    height = 800
                elif ranking == "overall":
                    width=2000
                    height=550
                elif ranking == "annual":
                    width=2000
                    height=600
            # the ratio of rpf vs fictional ships each year
            elif subject == "rpf":
                figure = visualise_pies(rpf_or_fic_dict, "rpf", ranking)
                if ranking == "femslash":
                    width = 700 
                    height = 650
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1000
                    height=600
            # what gender combinations have rpf written about them? number of rpf ships of each gender combo
            elif subject == "rpf_by_gender_combo":
                figure = visualise_grouped_bars(rpf_by_gender_combo_dict, "rpf", ranking)
                if ranking == "femslash":
                    width = 1200 
                    height = 600
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1300
                    height=600
            # highest ranking ships each year (just the top 5 or 10 of the ranking basically)
            elif subject == "top_ships":
                figure = visualise_top_5(top_ships_dict, "pairings", ranking)
                if ranking == "femslash":
                    width = 1750
                    height = 1100
                elif ranking == "overall":
                    width=2600
                    height=1800
                elif ranking == "annual":
                    width=2600
                    height=1500
            # the ships that have appeared the most frequently in the top ships of the ranking
            elif subject == "longest_running_ships":
                # TODO: double check for annual ranking if appearances & streaks are diff
                    # make a case & visualise both if so
                figure = visualise_single_table(longest_running_ships_df, ranking, "longest_streak")
                if ranking == "femslash":
                    width = 680
                    height = 370
                elif ranking == "overall":
                    width=950
                    height=500
                elif ranking == "annual":
                    width=950
                    height=500
            # all time top 100 most popular ships by summed, weighted rank numbers
            elif subject == "top_100_most_popular_ships":
                figure = visualise_single_table(top_100_ships_df, ranking, "most_popular_characters")
                if ranking == "femslash":
                    width = 1200
                    height = 2800
                elif ranking == "overall":
                    width=1800
                    height=2800
                elif ranking == "annual":
                    width=1800
                    height=2900
            # pie charts summarising demo stats and rpf about the top 100 ships
            elif subject == "top_100_demo":
                figure = visualise_pies(top_100_ships_df, "most_popular_ships", ranking)
                if ranking == "femslash":
                    width = 1000
                    height = 500
                elif ranking == "overall":
                    width=1500
                    height=600
                elif ranking == "annual":
                    width=1600
                    height=600

            if ranking in ["overall", "annual"]:
                # how much gen vs slash fic total each year
                if subject == "gen_vs_slash_fic":
                    figure = visualise_pies(gen_vs_slash_total_dict, "fic_type", ranking)
                    if ranking == "overall":
                        width = 1300
                        height = 600
                    elif ranking == "annual":
                        width=1000
                        height=600
                # how much gen fic by gender combo each year
                elif subject == "gen_by_gender_combo":
                    figure = visualise_grouped_bars(gen_vs_slash_by_gender_combo, "gen", ranking)
                    if ranking == "overall":
                        width=1300
                        height=600
                    elif ranking == "annual":
                        width=1300
                        height=600
                # highest ranking (top 10) ships each year by gender combo (mlm, wlw, str8)
                elif subject == "top_ships_by_gender_combo":
                    figure = visualise_column_tables(top_ships_by_gender_combo, "gender_combos", ranking)
                    if ranking == "overall":
                        width=3300
                        height=2900
                    elif ranking == "annual":
                        width=3300
                        height=2500

            # adding general subject to our dict
            stuff_to_visualise[subject] = {
                "figure": figure,
                "filepath": f"{folder}{subject}{suffix}", 
                "width": width,
                "height": height,
            }
        
        # the characters in the most (3+) ships each year
        hottest_characters = hottest_char(character_info_df, ranking)
        visualise_hottest_chars(hottest_characters, ranking) # writes its own files


        ## gender stats (keeping categories separate for ease of finding, rather than 1 big loop)

        gender_stuff = [
            "gender_distribution", 
            "gender_minority_distr",
        ]

        if ranking in ["overall", "annual"]: # adding extra subjects
            gender_stuff += [
                "gender_combo_distribution",
                "gender_combo_minority_distr",
                "avg_rank_by_gender",
                "avg_rank_by_gender_combo",
            ]

        gender_subfolder = f"gender_stats/{ranking}_" # putting these into a subfolder

        # running all data making code for this portion outside the loop
        gender_dict = get_counts(character_info_df, "gender", "full_name")

        if ranking in ["overall", "annual"]:
            total_gender_combos = get_gender_combos(ship_info_df)
            average_rank_by_gender = average_rank(character_info_df, "gender")
            average_rank_by_gender_combo = average_rank(ship_info_df, "gender_combo")

        # making figures & determining dimensions & adding them to our dict
        for subject in gender_stuff:
            # how many characters of each gender label each year
            if subject == "gender_distribution":
                figure = visualise_pies(gender_dict, "gender", ranking)
                if ranking == "femslash":
                    width = 700
                    height = 650
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1000
                    height=600
            # genders minus biggest labels (ie "M", "F") each year
            elif subject == "gender_minority_distr":
                figure = visualise_grouped_bars(gender_dict, "minority_genders", ranking)
                if ranking == "femslash":
                    width = 1200
                    height = 600
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1500
                    height=600

            if ranking in ["overall", "annual"]:
                # how many ships of each gender combination each year
                if subject == "gender_combo_distribution":
                    figure = visualise_grouped_bars(total_gender_combos, "gender_combos", ranking)
                    if ranking == "overall":
                        width=1300
                        height=600
                    elif ranking == "annual":
                        width=1700
                        height=600
                # how many ships of gender combinations other than mlm & str8 each year
                elif subject == "gender_combo_minority_distr":
                    figure = visualise_grouped_bars(total_gender_combos, "minority_gender_combos", ranking)
                    if ranking == "overall":
                        width=1300
                        height=600
                    elif ranking == "annual":
                        width=1300
                        height=600

                # what was the average rank of characters of each gender each year
                elif subject == "avg_rank_by_gender":
                    figure = visualise_multi_lines(average_rank_by_gender, "average_by_label", ranking)
                    if ranking == "overall":
                        width=800
                        height=600
                    elif ranking == "annual":
                        width=800
                        height=600
                # what was the average rank of ships of each gender combination each year
                elif subject == "avg_rank_by_gender_combo":
                    figure = visualise_multi_lines(average_rank_by_gender_combo, "average_by_label", ranking)
                    if ranking == "overall":
                        width=800
                        height=600
                    elif ranking == "annual":
                        width=800
                        height=600

            stuff_to_visualise[subject] = {
                "figure": figure,
                "filepath": f"{folder}{gender_subfolder}{subject}{suffix}", 
                "width": width,
                "height": height,
            }


        ## race stats

        race_stuff = [
            # characters' racial groups
            "racial_distribution", 
            "racial_minority_distr", 
            "multi_char_pies", 
            "multi_char_line",
            "racial_groups_no",

            # race combos of ships
            "race_combo_distr",
            "interracial_ships_pies",
            "interracial_ships_lines",
            "multi_involved_ships_pies",
            "multi_involved_ships_line",

            # 4 categories of ships w/ & w/out white & east asian ppl
            "non_white_distr",
            "non_white_top_ships",
            "non_white_avg_ranks"
        ]

        race_subfolder = f"race_stats/{ranking}_" # putting these into a subfolder

        # running all data making code for this portion outside the loop
        race_percent_dict = get_counts(character_info_df, "race", "full_name")
        total_multi = total_multi_nos_by_year(race_percent_dict, "race")
        total_groups = total_racial_groups(race_percent_dict)

        race_combo_dict = get_counts(ship_info_df, "race_combo", "ship")
        total_multi_involved = total_multi_nos_by_year(race_combo_dict, "race_combo")
        total_interracial = total_interracial_ratio(race_combo_dict)

        prepped_dict = prep_df_for_non_white_ship_comp(ship_info_df)
        separated_dict = separate_out_non_white_ships_info(prepped_dict)
        non_white_counts = count_non_white_ships(prepped_dict)
        top_non_white = top_non_white_ships(separated_dict)
        average_non_white_rank = average_non_white_ranking(separated_dict)

        # making figures & determining dimensions & adding them to our dict
        for subject in race_stuff:
            # how many characters of each racial group each year
            if subject == "racial_distribution":
                figure = visualise_pies(race_percent_dict, "race", ranking)
                if ranking == "femslash":
                    width = 1500
                    height = 1500
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1200
                    height=600
            # racial groups minus white people, east asian people & any unknown, ambiguous or non-human characters
            elif subject == "racial_minority_distr":
                # (same info, printing bar charts by year)
                # for year in race_percent_dict:
                #     year_df = race_percent_dict[year].copy()
                #     year_race_fig = visualise_stacked_bars(year_df, "minority_racial_groups", ranking)
                #     year_race_
                #         f"{folder}{sub_folder}racial_minorities_by_year/{ranking}_minority_racial_distr_{year}.png", 
                #         width = 1200, 
                #         height = 600, 
                #         scale=2
                #     )
                figure = visualise_multi_lines(race_percent_dict, "minority_racial_groups", ranking)
                if ranking == "femslash":
                    width = 1000
                    height = 600
                elif ranking == "overall":
                    width=1000
                    height=600
                elif ranking == "annual":
                    width=1000
                    height=600

            # how many characters were multiracial each year
            # as pie charts
            elif subject == "multi_char_pies":
                figure = visualise_pies(total_multi, "multi_chars", ranking)
                if ranking == "femslash":
                    width = 700
                    height = 650
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1000
                    height=600
            # as a line chart
            elif subject == "multi_char_line":
                figure = visualise_line(total_multi, "multi_chars", ranking)
                if ranking == "femslash":
                    width = 700
                    height = 600
                elif ranking == "overall":
                    width=700
                    height=600
                elif ranking == "annual":
                    width=700
                    height=600

            # how many racial groups were represented total each year
            elif subject == "racial_groups_no":
                figure = visualise_line(total_groups, "total_racial_groups", ranking)
                if ranking == "femslash":
                    width = 700
                    height = 600
                elif ranking == "overall":
                    width=700
                    height=600
                elif ranking == "annual":
                    width=700
                    height=600

            # how many ships of each racial group combination each year
            elif subject == "race_combo_distr":
                figure = visualise_pies(race_combo_dict, "race_combos", ranking)
                if ranking == "femslash":
                    width = 1500
                    height = 1500
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1200
                    height=600

            # how many interracial, non-interracial, and ambiguous ships
            # as pie charts
            elif subject == "interracial_ships_pies":
                figure = visualise_pies(total_interracial, "interracial_ships", ranking)
                if ranking == "femslash":
                    width = 700
                    height = 650
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1000
                    height=600
            # as a line chart
            elif subject == "interracial_ships_lines":
                figure = visualise_multi_lines(total_interracial, "interracial_ships", ranking)
                if ranking == "femslash":
                    width = 800
                    height = 500
                elif ranking == "overall":
                    width=800
                    height=500
                elif ranking == "annual":
                    width=800
                    height=500

            # how many ships involved multiracial characters
            # as pie charts
            elif subject == "multi_involved_ships_pies":
                figure = visualise_pies(total_multi_involved, "multi_char_ships", ranking)
                if ranking == "femslash":
                    width = 700
                    height = 650
                elif ranking == "overall":
                    width=1300
                    height=600
                elif ranking == "annual":
                    width=1000
                    height=600
            # as a line chart
            elif subject == "multi_involved_ships_line":
                figure = visualise_line(total_multi_involved, "multi_char_ships", ranking)
                if ranking == "femslash":
                    width = 700
                    height = 600
                elif ranking == "overall":
                    width=700
                    height=600
                elif ranking == "annual":
                    width=700
                    height=600

            # how many ships each year contained 
            # 1) white ppl, 2) east asian ppl, 3) no white ppl, 4) neither white nor EA ppl
            elif subject == "non_white_distr":
                figure = visualise_non_white_counts(non_white_counts, ranking)
                if ranking == "femslash":
                    width = 1000
                    height = 400
                elif ranking == "overall":
                    width=1000
                    height=400
                elif ranking == "annual":
                    width=900
                    height=400
            # which ships were the top ranked in each category each year
            elif subject == "non_white_top_ships":
                figure = visualise_column_tables(top_non_white, "non_white_ships", ranking)
                if ranking == "femslash":
                    width = 3800
                    height = 1800
                elif ranking == "overall":
                    width=3500
                    height=1500
                elif ranking == "annual":
                    width=3500
                    height=1700
            # what was the average rank of each category each year
            elif subject == "non_white_avg_ranks":
                figure = visualise_multi_lines(average_non_white_rank, "non_white_ships", ranking) 
                if ranking == "femslash":
                    width = 800
                    height = 500
                elif ranking == "overall":
                    width=800
                    height=500
                elif ranking == "annual":
                    width=800
                    height=500

            stuff_to_visualise[subject] = {
                "figure": figure,
                "filepath": f"{folder}{race_subfolder}{subject}{suffix}", 
                "width": width,
                "height": height,
            }


        # writing files
        for item in stuff_to_visualise:
            figure_info = stuff_to_visualise[item]

            figure_info["figure"].write_image(
                figure_info["filepath"],
                width = figure_info["width"],
                height = figure_info["height"], 
                scale=2
            )