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

    