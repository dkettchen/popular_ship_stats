from visualisation.input_data_code.make_joined_df import (
    make_joined_ranking_df, 
    make_fandom_joined_df
)
from visualisation.input_data_code.make_file_dfs import make_ships_df, make_characters_df

# make total version (ships/char list x fandom data)

# make yearly version (for each ranking) (ship/char joined ranking x fandom data)
for ranking in ["total","femslash", "overall", "annual"]:

    # input df prep: 
    if ranking != "total": # rankings need extra steps
        ship_joined_df = make_joined_ranking_df(ranking)

        fandom_joined_char_df = make_fandom_joined_df(ship_joined_df, "characters")
        fandom_joined_ship_df = make_fandom_joined_df(ship_joined_df, "ships")

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