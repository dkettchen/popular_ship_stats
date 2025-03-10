import pandas as pd
from visualisation.vis_utils.read_csv_to_df import df_from_csv
from copy import deepcopy

# get data from countries population file & prep for visualisation
#TODO: 
# - add missing data to population file ✅
    # - add small countries' population data to file! ✅
    # - also fix relevant indexes in functions here accordingly ✅
    # - need to also add continents to em ✅

# - add countries to multi national rpf other than the youtubers too ✅

# - we can test these functions o.o

# - visualise:
    # - ratio of countries in ranking vs population ratio of countries irl
    # - ratio of continents in ranking vs population ratio of continents irl
    # - countries that were represented in ranking by population 
    #   + remainder of world that didn't make it
    # - countries by continent that were represented in ranking by population 
    #   + remainder of continent that didn't make it
        # ie uk pop + france, polish, norwegian & swedish pop + remainder of rest of europe
    # - countries by continent that made the ranking, by ranking char numbers (no remainder)
        # ie europe mostly uk

def make_population_df():
    """
    returns a dataframe with the read data from 
    data/reference_and_test_files/additional_data/world_population_by_countries.csv
    """
    df = df_from_csv("data/reference_and_test_files/additional_data/world_population_by_countries.csv")
    return df

def get_pop_sizes(input_df:pd.DataFrame, data_case:str):
    """
    takes a df with at least "Location", "Population", "Continent" columns, 
    with a first row of the total population in question (ie world population)
    and only the countries listed that one wants to include in the output 
    (ie excluding rows one wants to go in the remainder rather than listed by name)

    - adds a "Remainder" row which contains the difference between the total population 
    and the sum of the populations listed. Returns a new df with ["Country", "Population", 
    "Continent"] columns. (data_case="remainder")

    - sums the populations of each continent. Input must contain all countries for accurate result. 
    Returns a new df with ["Continent", "Population"] columns, ordered by descending population. 
    (data_case="continents") 

    returns a new df
    """

    # - get dataframe of all country names & their pop sizes
    new_df = input_df.copy().get([
        "Location", 
        "Population", 
        "Continent"
    ]).rename(columns={"Location":"Country"})

    # all but first row
    country_df = new_df[1:]

    if data_case == "remainder":
        # - sum their total population & then substract from total pop to get a "rest" value
        world_pop = new_df["Population"][0]
        named_countries_pop_sum = country_df["Population"].agg("sum")
        remaining_countries_pop = world_pop - named_countries_pop_sum
        print(world_pop, named_countries_pop_sum, remaining_countries_pop)

        country_df = pd.concat([ # appending "rest" value
            country_df,
            pd.DataFrame( # making single row to append
                [["Remainder", remaining_countries_pop, "N/A"]], 
                columns=country_df.columns
            )
        ])
    elif data_case == "continents":
        # removing any non-continents:
        country_df = country_df.mask(country_df["Continent"] == "-").dropna(how="all")

        # summing by continent & sorting
        country_df = country_df.groupby("Continent").agg("sum")
        country_df = country_df.reset_index().get(
            ["Continent", "Population"]
        ).sort_values(
            by="Population", ascending=False
        )

        # # - we didn't get tiny countries but like prolly won't make much of a difference??? 
        # # idk worst case add missing data
        # summed_continents = country_df["Population"].agg("sum")
        # world_pop = new_df["Population"][0]
        # remainder = world_pop - summed_continents
        # print(remainder) # 187,598,066 ok this is a big enough number to matter, (bc bigger than oceania)
        #                  # let's find extra data rip
            # even with extra countries there's still 170,739,877 left??? 
            # meaning most of this remainder isn't actually accounted for????
            # probably due to incorrect numbers & different collection times idk hm

    return country_df

def get_some_countries(input_df:pd.DataFrame, input_list:list):
    """
    takes a df that has at least a "Location" and "Population" column, 
    and a list of locations (countries and/or total, ie "World" or continent) 
    that should have corresponding rows in the output df

    returns a new df that only contains those countries' rows
    ordered by population size
    """
    # adjusting input
    new_df = input_df.copy().set_index("Location")
    new_list = deepcopy(input_list)

    # collecting relevant country rows
    country_dict = {}
    for country in new_list:
        country_dict[country] = new_df.loc[country]

    # making a new df using only these values
    concated_df = pd.DataFrame(country_dict).transpose().sort_values(by="Population", ascending=False)

    # resetting & renaming countries column to match input columns
    final_df = concated_df.reset_index().rename(columns={"index":"Location"})

    return final_df

def get_continent_df(data_df:pd.DataFrame, continent:str):
    """
    takes a df with at least ["Location", "Population", "Continent"] columns, 
    with all countries of the relevant continent represented, and the name of the desired continent

    returns a new df with ["Location", "Population", "Continent"] columns, the total population of 
    the entered continent, and all countries of that continent that were in the input df, ordered
    by descending population size
    """
    # get total pop per all continents using pop sizes util
    continent_totals = get_pop_sizes(data_df, "continents")

    # retrieve requested continent's total pop
    continent_row = continent_totals.set_index("Continent").loc[continent]

    # make list of all countries in data of this continent
        # how to handle europe/asia ones?
    continent_countries = list(data_df.where(
        data_df["Continent"] == continent
    ).dropna(how="all")["Location"])

    # get df of only those countries
    countries_df = get_some_countries(data_df, continent_countries)

    countries_df = countries_df.get([
        "Location", 
        "Population", 
        "Continent"
    ])

    # add continent total
    concat_df = pd.concat([ # appending "rest" value
        countries_df,
        pd.DataFrame( # making single row to append
            [["Total", continent_row["Population"], continent]], 
            columns=countries_df.columns
        )
    ]).sort_values(by="Population", ascending=False)

    return concat_df

if __name__ == "__main__":
    pop_df = make_population_df()
    country_pop_df = get_pop_sizes(pop_df[:124], "remainder") # excluding countries smaller than those included
    continent_pop_df = get_pop_sizes(pop_df[:-1], "continents") # excluding "unknown" row
    only_english_speakers = get_some_countries(pop_df, ["USA", "Canada", "UK", "Ireland", "Australia", "New Zealand", "World"])
    only_africa = get_continent_df(pop_df[:-1], "Africa")