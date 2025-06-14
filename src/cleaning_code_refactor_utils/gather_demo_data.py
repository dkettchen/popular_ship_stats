from json import load
from src.cleaning_code_refactor_utils.collect_demo_tags import collect_demo_tags
from src.cleaning_code_refactor_utils.assign_demo_tags import assign_demo_tags
import pandas as pd
from data.reference_and_test_files.refactor_helper_files.demo_data_lookup import (
    ALL_PAIRING_COMBOS, DEMO_COMBOS, CANON_STATUS, INCEST_STATUS
)

def gather_char_demo_data(clean_dict:dict):
    """
    assigns the gender, race and orientation data of all characters, 
    cleans and prints if any are not in the lookup yet
    """

    # read in json file to get fandoms & chars dict
    fandom_and_char_file = "data/reference_and_test_files/refactor_helper_files/cleaned_fandoms_and_characters.json"
    with open(fandom_and_char_file, "r") as json_file:
        fandom_and_char_dict = load(json_file)

    # go through rankings, collect data to fandoms' characters' entries
    raw_tags_added = collect_demo_tags(fandom_and_char_dict, clean_dict)

    # determine gender, race & orientation tags
    tags_assigned = assign_demo_tags(raw_tags_added)
    
    # TODO turns relevant values into df & print to csv??

    return tags_assigned

def gather_ship_demo_data(clean_dict:dict, demo_data:dict):
    """
    assigns all ships' gender combo, race combo, 
    orientation combo, canon (orientation) alignment, 
    canon status, and incest status 
    (the latter three are only for slash ships, 
    gen ships are tagged as "gen ship" instead)

    if any ships are not in the lookups yet, it prints them

    returns a new version of the dict containing these new values
    """

    # get all years & all rankings
    all_rankings = []
    for year in clean_dict:
        for ranking in clean_dict[year]:
            current_df = clean_dict[year][ranking]
            all_rankings.append(current_df)
    # concat & get relevant columns
    all_data = pd.concat(all_rankings).reset_index().get(["Relationship", "Fandom", "Type"])

    # get all unique ships & group by fandom
    ship_dict = {}
    for row in all_data.index:
        # get data
        current_row = all_data.loc[row]
        relationship = sorted(current_row["Relationship"])
        fandom = current_row["Fandom"]
        pairing_type = current_row["Type"]

        # gen ships based on type
        if pairing_type == ["Gen"]:
            joined_relationship = " & ".join(relationship)
            gen = True
        else: 
            joined_relationship = " x ".join(relationship)
            gen = False

        # add fandom if not in dict yet
        if fandom not in ship_dict.keys():
            ship_dict[fandom] = {}
        # add ship to fandom if not in there yet
        if joined_relationship not in ship_dict[fandom]:
            ship_dict[fandom][joined_relationship] = {
                "members": relationship,
                "no of members": len(relationship),
                "gen ship": gen,
                "gender combo": None,
                "race combo": None,
                "orientation combo": None,
                "canon alignment": None,
                "canon ship": None,
                "incest ship": None
            }

    # add demo data combos
    for fandom in ship_dict:
        for ship in ship_dict[fandom]:
            # add gender, race, orientation & canon aligned/conflicted from checking lookup once we have it
            if f"{fandom} - {ship}" in DEMO_COMBOS:
                ship_list = DEMO_COMBOS[f"{fandom} - {ship}"]
                ship_dict[fandom][ship]["gender combo"] = ship_list[0]
                ship_dict[fandom][ship]["race combo"] = ship_list[1]
                ship_dict[fandom][ship]["orientation combo"] = ship_list[2]
                ship_dict[fandom][ship]["canon alignment"] = ship_list[3]

            # otherwise assign from demo data
            else:

                # make combo tags
                for tag in [
                    "gender_tag",
                    "race_tag",
                    "orientation_tag"
                ]:
                    ls = []
                    for member in ship_dict[fandom][ship]["members"]:
                        # is member in here?
                        if member not in demo_data[fandom]["characters"].keys():
                            print(member, fandom, "why not in demo dict?")

                        # retrieve from demo dict
                        char_tag = demo_data[fandom]["characters"][member][tag]
                        # append to lists
                        ls.append(char_tag)

                    if len(ls) == 0:
                        print(ship, member, tag, "why no collected tags")
                    elif len(set(ls)) == 1 and tag != "gender_tag":
                        combo = ls[0]
                    else:
                        combo = " / ".join(ls)

                        # fix gender combos that are too long
                        if combo in [
                            "M / M / M / M",
                            "M / M / M",
                        ]:
                            combo = "M / M"
                        elif combo in ["M | Other / M / M",]:
                            combo = "M | Other / M"
                        elif combo in ["F / F / F",]:
                            combo = "F / F"
                        # check for any other gender combos that are too long
                        if len(ls) > 2 and len(set(ls)) < len(ls) and combo not in [
                            "M / M", "F / F", "M | Other / M"
                        ] and tag == "gender_tag":
                            print(combo)

                    which_combo = tag[:-4] + " combo"
                    ship_dict[fandom][ship][which_combo] = combo


                # determine alignment with canon

                # add canon aligned, conflicted, ambiguous based on genders & orientation
                gender_combo = ship_dict[fandom][ship]["gender combo"]
                race_combo = ship_dict[fandom][ship]["race combo"]
                orient_combo = ship_dict[fandom][ship]["orientation combo"]

                # default to replace
                canon_alignment = "ambiguous"

                if not ship_dict[fandom][ship]["gen ship"]:

                    # conflicted conditions:
                    # any fully acearo characters
                    # any mlm/wlw pairings with str8 ppl in it
                    # any het pairings with gay ppl in it
                    # any Other involved ships with str8 or gay non-other partners
                    # any Other/Ambig characters who are only into men/women but are shipped w/ the opposite
                    if "acearo" in orient_combo \
                    or (
                        "str8" in orient_combo \
                        and (gender_combo in ALL_PAIRING_COMBOS["mlm"] \
                        or gender_combo in ALL_PAIRING_COMBOS["wlw"])
                    ) or (
                        "gay" in orient_combo \
                        and gender_combo in ALL_PAIRING_COMBOS["het"]
                    ) or (("Ambig" not in gender_combo and (
                            gender_combo in ALL_PAIRING_COMBOS["woman_attracted_other"] \
                            or gender_combo in ALL_PAIRING_COMBOS["man_attracted_other"]
                        )) and ("str8" in orient_combo or "gay" in orient_combo)
                    ) or ((
                            "man_attracted" in orient_combo \
                            and gender_combo in ALL_PAIRING_COMBOS["woman_attracted_other"]
                        ) or (
                            "woman_attracted" in orient_combo \
                            and gender_combo in ALL_PAIRING_COMBOS["man_attracted_other"]
                    )):
                        canon_alignment = "conflicted"

                    # aligned conditions:
                    # must not contain acearo or unspecified
                    # mlm and wlw pairings without str8 ppl (ie only bi/gay)
                    # het pairings without gay ppl (ie only bi/str8)
                    # women/men x other without str8, gay, or man_attracted/woman_attracted respectively
                    # ambig pairings with bi non-ambig partner and bi or appropriately-attracted ambig partner
                    elif "acearo" not in orient_combo \
                    and "unspecified" not in orient_combo \
                    and ((
                        "str8" not in orient_combo and (
                            gender_combo in ALL_PAIRING_COMBOS["mlm"] \
                            or gender_combo in ALL_PAIRING_COMBOS["wlw"]
                        )
                    ) or (
                        "gay" not in orient_combo \
                        and gender_combo in ALL_PAIRING_COMBOS["het"]
                    ) or (
                        "Ambig" not in gender_combo \
                        and "str8" not in orient_combo \
                        and "gay" not in orient_combo \
                        and ((
                                "man_attracted" not in orient_combo \
                                and gender_combo in ALL_PAIRING_COMBOS["woman_attracted_other"]
                            ) or (
                                "woman_attracted" not in orient_combo \
                                and gender_combo in ALL_PAIRING_COMBOS["man_attracted_other"]
                            )
                        )
                    ) or (
                        "Ambig" in gender_combo and (
                        orient_combo == "bi / bi" or (
                            "bi" in orient_combo \
                            and ((
                                    "man_attracted" in orient_combo \
                                    and gender_combo in ALL_PAIRING_COMBOS["man_attracted_other"]
                                ) or (
                                    "woman_attracted" in orient_combo \
                                    and gender_combo in ALL_PAIRING_COMBOS["woman_attracted_other"]
                            ))
                        ))
                    )):
                        canon_alignment = "aligned"
                else:
                    canon_alignment = 'gen ship'

                ship_dict[fandom][ship]["canon alignment"] = canon_alignment

                print({f"{fandom} - {ship}": [gender_combo, race_combo, orient_combo, canon_alignment]})


            # non-gen ships also need canon & incest data
            if not ship_dict[fandom][ship]["gen ship"]:
                canon_or_no = None
                for x in CANON_STATUS:
                    if f"{fandom} - {ship}" in CANON_STATUS[x]:
                        canon_or_no = x
                        break
                ship_dict[fandom][ship]["canon ship"] = canon_or_no
                if not canon_or_no:
                    print(f"{fandom} - {ship}", "canon?")

                incest_or_no = None
                for x in INCEST_STATUS:
                    if f"{fandom} - {ship}" in INCEST_STATUS[x]:
                        incest_or_no = x
                        break
                ship_dict[fandom][ship]["incest ship"] = incest_or_no
                if not incest_or_no:
                    print(f"{fandom} - {ship}", "related?")
            else: # if it's a gen ship
                ship_dict[fandom][ship]["canon ship"] = "gen ship"
                ship_dict[fandom][ship]["incest ship"] = "gen ship"

    return ship_dict

