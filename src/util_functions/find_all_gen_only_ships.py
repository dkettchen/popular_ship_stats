from visualisation.input_data_code.make_file_dfs import make_yearly_df_dict
from re import sub

def find_non_slash_ships(end_date:int=2023):
    """
    checks all ships as they're represented in the rankings up to the specified end date (2023 by default atm)

    returns a list of all the ships that only have their non-slash version represented

    ex. "Aizawa Shouta | Eraserhead & Midoriya Izuku | Deku"  is a teacher-student relationship, 
    and THANK FUCK they're only represented as a general ship 🙏😩
    """
    
    # collecting all rankings
    rankings_dict = {}
    for ranking in ["overall", "femslash", "annual"]:
        year_dict = make_yearly_df_dict(ranking, end_date)
        for year in year_dict:
            rankings_dict[f"{ranking}_{year}"] = year_dict[year]

    # find all unique ships represented
    all_unique_ships = set()
    for key in rankings_dict:
        current_year = rankings_dict[key]
        ships_of_year = current_year["ship"]
        for ship in list(ships_of_year):
            all_unique_ships.add(ship)
    all_unique_ships = sorted(list(all_unique_ships))

    # locate all gen ships
    gen_ships = []
    for ship in all_unique_ships:
        if "&" in ship:
            gen_ships.append(ship)

    # locate gen ships that don't have a slash equivalent represented
    gen_only_ships = []
    for ship in gen_ships:
        if sub("&", "x", ship) not in all_unique_ships:
            gen_only_ships.append(ship)
            # print(f'"{ship}",')

    return gen_only_ships