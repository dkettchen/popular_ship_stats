from copy import deepcopy

def years_total_entries(joined_data:dict):
    """
    adds a new "total" key to every year entry of input

    its value is a list of all the unique ships that made any ranking that year, 
    listed alphabetically in "fandom_ship" format

    returns a new nested dict with the added key:value pairs
    """

    new_data = deepcopy(joined_data)

    for year in joined_data:
        current_year = joined_data[year]
        year_data = []
        for ranking in current_year:
            # add fandom_ship item to year's data if it's not in there yet
            data = list(current_year[ranking]["clean"]["Fandom"] + "_" + current_year[ranking]["clean"]["Relationship"])
            year_data.extend([item for item in data if item not in year_data])

        # add alphabetical list
        new_data[year]["total"] = sorted(year_data)

    return new_data
