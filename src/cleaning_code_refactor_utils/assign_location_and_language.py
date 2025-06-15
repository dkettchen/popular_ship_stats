from copy import deepcopy
from data.reference_and_test_files.refactor_helper_files.location_lookup import (
    COUNTRIES, MULTI_NATIONALS, RPF
)
from src.cleaning_code_refactor_utils.find_continent_and_lang import find_continent_and_language

def assign_location_data(fandoms_dict:dict):
    """
    assigns country of origin, continent, and language to each fandom 
    and members of rpf fandoms that contain multiple nationalities
    """

    new_dict = deepcopy(fandoms_dict)

    for fandom in new_dict:

        # finding fandom's data

        country_of_origin = None
        cont_lang = None
        # assigning base countries based on fandoms
        for country in COUNTRIES:
            if fandom in COUNTRIES[country]:
                country_of_origin = country
        for multi_fandom in MULTI_NATIONALS:
            if fandom == multi_fandom:
                country_of_origin = MULTI_NATIONALS[multi_fandom]
        
        # real human beings with multiple nationalities in their fandom
        if fandom in RPF:
            all_countries = set()
            # adding individual countries for ppl based on their nationalities
            for char in new_dict[fandom]["characters"]:
                real_human_nationality = None
                # specifically listed countries
                for country in RPF[fandom]:
                    if country == "else":
                        continue
                    if char in RPF[fandom][country]:
                        real_human_nationality = country
                # if there is a value for anyone else in the group
                if not real_human_nationality and "else" in RPF[fandom].keys():
                    real_human_nationality = RPF[fandom]["else"]
                
                # check if we missed anyone
                if not real_human_nationality:
                    print(char)
                
                # assign continent & language
                cont_lang = find_continent_and_language(real_human_nationality, fandom)

                # add to dict
                new_dict[fandom]["characters"][char]["country_of_origin"] = real_human_nationality
                new_dict[fandom]["characters"][char]["continent"] = cont_lang[0]
                new_dict[fandom]["characters"][char]["language"] = cont_lang[1]

                all_countries.add(real_human_nationality)

            # ignore kpop bands' foreign members' countries, bc the band is still korean
            if fandom not in COUNTRIES["South Korea"]:
                # for other international fandoms, list all currently involved countries
                country_of_origin = " / ".join(sorted(list(all_countries)))

                # gotta re-find the stuff
                cont_lang = find_continent_and_language(country_of_origin, fandom)

                # update in dict
                new_dict[fandom]["country_of_origin"] = country_of_origin
                new_dict[fandom]["continent"] = cont_lang[0]
                new_dict[fandom]["language"] = cont_lang[1]

        else: # just make same country etc as main
            cont_lang = find_continent_and_language(country_of_origin, fandom)
            for char in new_dict[fandom]["characters"]:
                # add to dict
                new_dict[fandom]["characters"][char]["country_of_origin"] = country_of_origin
                new_dict[fandom]["characters"][char]["continent"] = cont_lang[0]
                new_dict[fandom]["characters"][char]["language"] = cont_lang[1]

        # check if origin has been assigned to fandom
        if not country_of_origin:
            print("This fandom is not in location lookup yet:",fandom)

        if not cont_lang: # only calculate if we haven't done it yet
            # assign continent & language
            cont_lang = find_continent_and_language(country_of_origin, fandom)
            print(fandom)

        # add to dict
        new_dict[fandom]["country_of_origin"] = country_of_origin
        new_dict[fandom]["continent"] = cont_lang[0]
        new_dict[fandom]["language"] = cont_lang[1]

        # adding data to characters



    return new_dict



