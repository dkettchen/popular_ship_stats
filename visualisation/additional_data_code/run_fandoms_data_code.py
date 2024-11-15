from visualisation.input_data_code.make_joined_df import (
    make_joined_ranking_df, 
    make_fandom_joined_df
)
from visualisation.input_data_code.make_file_dfs import make_ships_df, make_characters_df
from visualisation.input_data_code.make_general_data import get_counts
from visualisation.diagram_code.visualise_pies import visualise_pies

# make total version (ships/char list x fandom data)

# make yearly version (for each ranking) (ship/char joined ranking x fandom data)
for ranking in [
    #"total",
    "femslash", "overall", "annual"
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

        # no of ships per country
        ships_per_country = get_counts(fandom_joined_ship_df, "country_of_origin", "ship")
        ships_per_country_pies = visualise_pies(ships_per_country, "ships_by_country", ranking)
        ships_per_country_pies.write_image(
                f"{folder}/{ranking}_additional_stats/{ranking}_ships_per_country.png",
                width = width,
                height = height, 
                scale=2
            )
        ships_by_continent = get_counts(fandom_joined_ship_df, "continent", "ship")
        ships_by_continent_pies = visualise_pies(ships_by_continent, "ships_by_continent", ranking)
        ships_by_continent_pies.write_image(
                f"{folder}/{ranking}_additional_stats/{ranking}_ships_per_continent.png",
                width = width,
                height = height, 
                scale=2
            )
        ships_by_language = get_counts(fandom_joined_ship_df, "original_language", "ship")
        ships_by_language_pies = visualise_pies(ships_by_language, "ships_by_language", ranking)
        ships_by_language_pies.write_image(
                f"{folder}/{ranking}_additional_stats/{ranking}_ships_per_language.png",
                width = width,
                height = height, 
                scale=2
            )

    else: # total just needs total ships/characters
        ship_df = make_ships_df()
        char_df = make_characters_df()

        fandom_joined_char_df = make_fandom_joined_df(char_df)
        fandom_joined_ship_df = make_fandom_joined_df(ship_df)

    


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