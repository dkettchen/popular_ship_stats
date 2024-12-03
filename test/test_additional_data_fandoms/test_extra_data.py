from src.additional_data_fandoms.make_extra_data import (
    make_population_df, 
    get_continent_df, 
    get_pop_sizes, 
    get_some_countries
)
import pytest
import pandas as pd

@pytest.fixture
def population_df():
    return make_population_df()[:-1] # not using last "unknown" row

@pytest.fixture
def smaller_list():
    return [
        {
            "Location": "World",
            "Population": 10000,
            "Continent": None,
        },
        {
            "Location": "Emerald City",
            "Population": 2032,
            "Continent": "Oz",
        },
        {
            "Location": "Isengard",
            "Population": 1392,
            "Continent": "Middle Earth",
        },
        {
            "Location": "Yellow Brick Road",
            "Population": 117,
            "Continent": "Oz",
        },
        {
            "Location": "The Shire",
            "Population": 1205,
            "Continent": "Middle Earth",
        },
        {
            "Location": "Mordor",
            "Population": 280,
            "Continent": "Middle Earth",
        },
        {
            "Location": "The Frozen North",
            "Population": 402,
            "Continent": "Bahumia",
        }
    ]

@pytest.fixture
def smaller_df(smaller_list):
    df = pd.DataFrame(
        smaller_list
    )
    return df

class TestPopSizes:
    def test_does_not_mutate_input(self, population_df):
        input_df = population_df.copy()
        get_pop_sizes(population_df, "remainder")
        assert list(input_df.shape) == list(population_df.shape)
        assert list(input_df.columns) == list(population_df.columns)
        for column in input_df.columns:
            assert list(input_df[column]) == list(population_df[column])

    def test_returns_df(self, population_df):
        result = get_pop_sizes(population_df, "remainder")
        assert type(result) == pd.DataFrame


    def test_returns_df_of_correct_shape(self, population_df):
        result_countries = get_pop_sizes(population_df, "remainder")
        result_countries_short = get_pop_sizes(population_df[:6], "remainder")
        result_continents = get_pop_sizes(population_df, "continents")
        assert len(list(result_countries.columns)) == 3
        assert len(result_countries) == len(population_df) # minus world value plus remainder
        assert len(list(result_countries_short.columns)) == 3
        assert len(result_countries_short) == 6 # 5 countries + remainder value
        assert len(list(result_continents.columns)) == 2
        assert len(result_continents) == 7 # 6 continents + eurasian border countries

    def test_returns_expected_columns(self, population_df):
        result_countries = get_pop_sizes(population_df, "remainder")
        result_continents = get_pop_sizes(population_df, "continents")
        assert list(result_countries.columns) == ["Country", "Population", "Continent"]
        assert list(result_continents.columns) == ["Continent", "Population"]

    def test_no_longer_contains_world_row(self, smaller_df):
        result_countries = get_pop_sizes(smaller_df, "remainder")
        result_countries = result_countries.set_index("Country")
        assert "World" not in result_countries.index

        result_continents = get_pop_sizes(smaller_df, "continents")
        result_continents = result_continents.set_index("Continent")
        assert sorted(list(result_continents.index)) == ["Bahumia", "Middle Earth", "Oz"]


    def test_countries_case_contains_remainder_row(self, smaller_df):
        result_countries = get_pop_sizes(smaller_df, "remainder")
        result_countries = result_countries.set_index("Country")
        assert "Remainder" in result_countries.index

    def test_countries_case_returns_unchanged_values_for_other_rows(self, smaller_df, smaller_list):
        result_countries = get_pop_sizes(smaller_df, "remainder")
        result_countries = result_countries.set_index("Country")

        for location_dict in smaller_list[1:]: # excluding world
            current_country = location_dict["Location"]
            assert list(result_countries.loc[current_country]) == [
                location_dict["Population"], 
                location_dict["Continent"]
            ]

    def test_countries_case_remainder_row_is_actual_remainder(self, smaller_df):
        result_countries = get_pop_sizes(smaller_df, "remainder")
        result_countries = result_countries.set_index("Country")
        assert result_countries.loc["Remainder"]["Population"] == 4572

    def test_countries_case_remainder_continent_is_NA(self, smaller_df):
        result_countries = get_pop_sizes(smaller_df, "remainder")
        result_countries = result_countries.set_index("Country")
        assert result_countries.loc["Remainder"]["Continent"] == "N/A"
    

    def test_continents_case_returns_continent_populations_summed(self, smaller_df):
        result_continents = get_pop_sizes(smaller_df, "continents")
        result_continents = result_continents.set_index("Continent")

        continent_sums = {
            "Bahumia" : 402, 
            "Middle Earth" : 1392 + 1205 + 280, 
            "Oz" : 2032 + 117
        }

        for continent in continent_sums: # excluding world
            assert result_continents.loc[continent]["Population"] == continent_sums[continent]

    def test_continents_case_returns_populations_in_desc_order(self, smaller_df):
        result_continents = get_pop_sizes(smaller_df, "continents")
        assert list(result_continents["Population"]) == sorted(
            list(result_continents["Population"]), reverse=True
        )

