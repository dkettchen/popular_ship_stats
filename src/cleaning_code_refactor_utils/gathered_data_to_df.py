import pandas as pd

def gathered_data_to_df(gathered_dict:dict, data_case:str):
    """
    takes a relevant gathered dict and data_case
    and returns a df with relevant data

    - data_case="fandoms": 
        - takes the output from gather_char_demo_data 
        (or any other dict structured as follows: 
        {fandom: {"rpf": bool, "year_joined": int, "years_appeared": list[int],}, ...})
        - will return a df with the following columns: 
        "fandom", 
        "rpf", 
        "year_joined", 
        "latest_year", 
        "total_years",
    - data_case="characters":
        - takes the output from gather_char_demo_data
        - will return a df with the following columns: 
        "index", 
        "name", 
        "fandom", 
        "year_joined", 
        "latest_year", 
        "total_years", 
        "gender", 
        "race", 
        "orientation",
    - data_case="ships":
        - takes the output from gather_ship_demo_data
        - will return a df with the following columns: 
        "index",
        "ship_name", 
        "fandom",
        "gender_combo",
        "race_combo",
        "orientation_combo",
        "gen_ship",
        "canon",
        "canon_alignment", 
        "incest",
        "member_no",
        "member_1",
        "member_2",
        "member_3",
        "member_4",

    """

    # set columns
    if data_case == "fandoms":
        columns = ["fandom", "rpf", "year_joined", "latest_year", "total_years"]
    elif data_case == "characters":
        columns = [
            "index", 
            "name", 
            "fandom", 
            "year_joined", 
            "latest_year", 
            "total_years", 
            "gender", 
            "race", 
            "orientation"
        ]
    elif data_case == "ships":
        columns = [
            "index", 
            "ship_name", 
            "fandom",
            "gender_combo", 
            "race_combo", 
            "orientation_combo", 
            "gen_ship", 
            "canon", 
            "canon_alignment", 
            "incest",
            "member_no",
            "member_1",
            "member_2",
            "member_3",
            "member_4",
        ]
    
    all_rows = []
    # iterate through fandoms
    for fandom in gathered_dict:
        if data_case == "fandoms":
            fandom_row = [
                fandom, 
                gathered_dict[fandom]["rpf"],
                gathered_dict[fandom]["year_joined"],
                sorted(gathered_dict[fandom]["years_appeared"])[-1],
                len(gathered_dict[fandom]["years_appeared"]),
            ]
            all_rows.append(fandom_row)
        else:
            if data_case == "characters":
                iterable = gathered_dict[fandom]["characters"]
            elif data_case == "ships":
                iterable = gathered_dict[fandom]
            for item in iterable:
                if data_case == "characters":
                    char_data = gathered_dict[fandom]["characters"][item]
                    row = [
                        f'{fandom} - {item}',
                        item,
                        fandom,
                        char_data["year_joined"],
                        sorted(char_data["years_appeared"])[-1],
                        len(char_data["years_appeared"]),
                        char_data["gender_tag"],
                        char_data["race_tag"],
                        char_data["orientation_tag"],
                    ]
                elif data_case == "ships":
                    ship_data = gathered_dict[fandom][item]

                    member_3 = None
                    member_4 = None
                    if len(ship_data["members"]) > 2:
                        member_3 = ship_data["members"][2]
                    if len(ship_data["members"]) > 3:
                        member_4 = ship_data["members"][3]

                    row = [
                        f'{fandom} - {item}',
                        item,
                        fandom,
                        ship_data["gender combo"],
                        ship_data["race combo"],
                        ship_data["orientation combo"],
                        ship_data["gen ship"],
                        ship_data["canon ship"],
                        ship_data["canon alignment"],
                        ship_data["incest ship"],
                        ship_data["no of members"],
                        ship_data["members"][0],
                        ship_data["members"][1],
                        member_3,
                        member_4,
                    ]
                all_rows.append(row)

    df = pd.DataFrame(all_rows, columns=columns)

    df = df.set_index(columns[0]).sort_index()

    return df
