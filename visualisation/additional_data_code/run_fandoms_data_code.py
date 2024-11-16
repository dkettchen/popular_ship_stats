from visualisation.input_data_code.make_joined_df import (
    make_joined_ranking_df, 
    make_fandom_joined_df
)
from visualisation.input_data_code.make_file_dfs import make_ships_df, make_characters_df
from visualisation.input_data_code.make_general_data import get_counts, get_by_gender_combo
from visualisation.diagram_code.visualise_pies import visualise_pies, visualise_demo_pies
from visualisation.diagram_code.visualise_bars import visualise_grouped_bars

# make total version (ships/char list x fandom data)

# make yearly version (for each ranking) (ship/char joined ranking x fandom data)
for ranking in [
    "total",
    #"femslash", "overall", "annual"
]:
    
    if ranking == "femslash":
        folder = "visualisation/ao3_femslash_rankings_2014_2023/ao3_femslash_rankings_charts"
    elif ranking == "overall":
        folder = "visualisation/ao3_overall_rankings_2013_2023/ao3_overall_rankings_charts"
    elif ranking == "annual":
        folder = "visualisation/ao3_annual_rankings_2016_2023/ao3_annual_rankings_charts"

    if ranking == "femslash":
        width = 700 
        height = 650
    elif ranking == "overall":
        width=1300
        height=600
    elif ranking == "annual":
        width=1000
        height=600

    # input df prep: 
    if ranking != "total": # rankings need extra steps
        ship_joined_df = make_joined_ranking_df(ranking)

        fandom_joined_char_df = make_fandom_joined_df(ship_joined_df, "characters")
        fandom_joined_ship_df = make_fandom_joined_df(ship_joined_df, "ships")

        # no of ships per country/continent/language
        for case in ["country", "continent", "language"]:
            if case == "country":
                column = "country_of_origin"
            elif case == "continent":
                column = "continent"
            elif case == "language":
                column = "original_language"
        
            ships_by_data = get_counts(fandom_joined_ship_df, column, "ship")
            ships_by_pies = visualise_pies(ships_by_data, f"ships_by_{case}", ranking)
            ships_by_pies.write_image(
                f"{folder}/{ranking}_additional_stats/{ranking}_ships_by_{case}.png",
                width = width,
                height = height, 
                scale=2
            )

        # rpf by country

        for country in ["USA", "UK", "Canada", "Japan", "China", "South Korea"]:
            only_this_country_ships = fandom_joined_ship_df.copy().where(
                fandom_joined_ship_df["country_of_origin"] == country
            ).dropna(how="all")

            only_this_country_chars = fandom_joined_char_df.copy().where(
                fandom_joined_char_df["country_of_origin"] == country
            ).dropna(how="all")

            # gender distr
            gender_distr = get_counts(only_this_country_chars, "gender", "full_name")
            gender_fig = visualise_pies(gender_distr, "gender_by_country", ranking, country)
            gender_fig.write_image(
                f"{folder}/{ranking}_additional_stats/{ranking}_gender_distr_({country}).png",
                width = width,
                height = height, 
                scale=2
            )

            # racial distr
            racial_distr = get_counts(only_this_country_chars, "race", "full_name")
            racial_fig = visualise_pies(racial_distr, "race_by_country", ranking, country)
            racial_fig.write_image(
                f"{folder}/{ranking}_additional_stats/{ranking}_racial_distr_({country}).png",
                width = width,
                height = height, 
                scale=2
            )
            
            # gender combos
            gender_combos = get_counts(only_this_country_chars, "gender_combo", "ship")
            gender_combo_fig = visualise_grouped_bars(gender_combos, "gender_combos", ranking, country)
            gender_combo_fig.write_image(
                f"{folder}/{ranking}_additional_stats/{ranking}_gender_combos_({country}).png",
                width = width,
                height = height, 
                scale=2
            )

            # interracial vs non-interracial

        # for case in english speaking media, asian media
            # gender distr
            # gender combos
            # racial distr
            # interracial vs non-interracial


            # data_by_gender_combo = get_by_gender_combo(fandom_joined_ship_df, column)
            # print(data_by_gender_combo)
            # TODO: we need a means to visualise gender by language by year (or only total??)
                # maybe one chart per big language?? (english, japanese, chinese, korean)
                # and then one per minority languages??
                
                # OR languages per gender combo?? 
                # -> chart for mlm, for wlw, for str8s & for minority genders??
            
            # data_by_gender_combo_fig = visualise_pies(data_by_gender_combo, case, ranking)
            # data_by_gender_combo_fig.write_image(
            #     f"{folder}/{ranking}_additional_stats/{ranking}_{case}_by_gender.png",
            #     width = width,
            #     height = height, 
            #     scale=2
            # )


    else: # total just needs total ships/characters
        ship_df = make_ships_df()
        char_df = make_characters_df()

        #TODO: make it so multinational rpf is tagged individually when joining 
        # (to offset youtube share per relevant countries)
        fandom_joined_char_df = make_fandom_joined_df(char_df)
        fandom_joined_ship_df = make_fandom_joined_df(ship_df)

        for country in ["USA", "UK", "Canada", "Japan", "China", "South Korea"]:
            only_this_country_ships = fandom_joined_ship_df.copy().where(
                (fandom_joined_ship_df["country_of_origin"] == country) | (
                fandom_joined_ship_df["country_of_origin"].str.contains(country))
            ).dropna(how="all")

            only_this_country_chars = fandom_joined_char_df.copy().where(
                (fandom_joined_char_df["country_of_origin"] == country) | (
                fandom_joined_char_df["country_of_origin"].str.contains(country))
            ).dropna(how="all")

            country_pies = visualise_demo_pies(only_this_country_chars, only_this_country_ships)
            country_pies.write_image(
                f"visualisation/ao3_all_data_2013_2023/ao3_all_data_charts/additional_diagrams/total_overview_({country}).png",
                width = 2000,
                height = 1000, 
                scale=2
            )

    


# geo data

# country distribution (total & yearly/per ranking)
    # comp to the world by population (over 1mil or over smallest country's number)
# continent distribution (total & yearly/per ranking)
# language (total & yearly/per ranking)
# gender/gender combo by country
# race distr by country
    # if we can easily find & translate to our racial groupings: comp to actual pop of that country
        # at least for big rep countries (US, UK, Canada, Japan, Korea, China, any others w enough chars)

# media type data

# media types (total & yearly/per ranking)
# media types by countries/continents/languages (x country's distr of media types)
# countries by media types too? (x media type's most countries)
# gender/gender combo by media type
# race distr by media type (we might actually get a minority of white chars in animation o.o)