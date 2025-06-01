from json import load
from data.reference_and_test_files.refactor_helper_files.old_character_names_lookup import OLD_CHARACTERS_LOOKUP
from data.reference_and_test_files.refactor_helper_files.old_fandom_names_lookup import OLD_FANDOMS_LOOKUP
import pandas as pd

data_folder = "data/reference_and_test_files/refactor_helper_files/old_files_for_ref"


# ## get characters (with their fandoms)

# # read og json file we have
# char_names_filepath = f"{data_folder}/characters_full_names_and_old_versions.json"
# with open(char_names_filepath, "r") as json_file:
#     read_data = load(json_file)
# # keys are fandoms
# # fandoms contain clean names of characters
# # which contain "op_versions" key which is a list of all og names

# # this currently only works for data structure from above file
# og_names = {}
# for fandom in read_data:
#     for char in read_data[fandom]:
#         op_versions = read_data[fandom][char]["op_versions"]
#         for og in op_versions:
#             fandom_og = f"{fandom} - {og}"
#             if fandom_og not in OLD_CHARACTERS_LOOKUP: # check against what we already have in lookup
#                 og_names[fandom_og] = char
# print(og_names) # print anything that isn't in the lookup yet


# ## get fandoms

# fandoms_filepath = f"{data_folder}/fandoms_clean_names_and_old_versions.json"
# with open(fandoms_filepath, "r") as json_file:
#     read_data = load(json_file)
# # structure is {fandom : [list of old versions]}

# # this currently only works for data structure from above file
# og_fandoms = {}
# for fandom in read_data:
#     for og in read_data[fandom]:
#         if og not in OLD_FANDOMS_LOOKUP:
#             og_fandoms[og] = fandom
# print(og_fandoms) # print anything that isn't in the lookup yet


# ## get demo data

# fandoms_filepath = f"{data_folder}/characters_list.csv"
# with open(fandoms_filepath, "r") as csv_file:
#     read_df = pd.read_csv(csv_file, escapechar="`")

# less_columns = read_df.get(['full_name', 'fandom', 'gender', 'race'])

# lookup_dict = {}
# for row in less_columns.index:
#     current_row = less_columns.loc[row]
#     fandom_char = f'{current_row["fandom"]} - {current_row["full_name"]}'
#     gender_race = f'{current_row["gender"]} - {current_row["race"]}'
#     lookup_dict[fandom_char] = gender_race

# print(lookup_dict) # print entire lookup


# ## get orientation data

# fandoms_filepath = f"{data_folder}/orientation_list.csv"
# with open(fandoms_filepath, "r") as csv_file:
#     read_df = pd.read_csv(csv_file, escapechar="`")

# lookup_dict = {}
# orient_labels = sorted(list(read_df["orientation"].unique()))
# for label in orient_labels:
#     lookup_dict[label] = []

# for row in read_df.index:
#     current_row = read_df.loc[row]
#     fandom_char = f'{current_row["fandom"]} - {current_row["full_name"]}'
#     orientation = current_row["orientation"]
#     lookup_dict[orientation].append(fandom_char)

# print(lookup_dict) # print entire lookup



## get orientation data

fandoms_filepath = f"{data_folder}/ship_status_list.csv"
with open(fandoms_filepath, "r") as csv_file:
    read_df = pd.read_csv(csv_file, escapechar="`")

canon_lookup = {}
incest_lookup = {}
canon_labels = sorted(list(read_df["canon"].unique()))
incest_labels = sorted(list(read_df["related"].unique()))
for label in canon_labels:
    canon_lookup[label] = []
for label in incest_labels:
    incest_lookup[label] = []


for row in read_df.index:
    current_row = read_df.loc[row]
    fandom_char = f'{current_row["fandom"]} - {current_row["slash_ship"]}'
    canon_status = current_row["canon"]
    canon_lookup[canon_status].append(fandom_char)
    incest_status = current_row["related"]
    incest_lookup[incest_status].append(fandom_char)

print(canon_lookup) # print entire lookup
print(incest_lookup)


# helper
def make_pairing_combo_lookup():
    """
    combines all male aligned, female aligned and other/ambig tags 
    and prints/returns the different categories 
    (mlm, wlw, het, other/women, other/men, other/other)
    to use as a lookup
    """

    # make all possible combos
    male_aligned_tags = [
        "M", "M | Other", "M | F | Other",
    ]
    female_aligned_tags = [
        "F", "F | Other", 
    ]
    other_tags = [
        "Ambig", "Other",
    ]

    # same sex pairings
    mlm_combos = []
    for tag_1 in male_aligned_tags:
        for tag_2 in male_aligned_tags:
            mlm_combos.append(f"{tag_1} / {tag_2}")
    wlw_combos = []
    for tag_1 in female_aligned_tags:
        for tag_2 in female_aligned_tags:
            wlw_combos.append(f"{tag_1} / {tag_2}")
    # het combos
    het_combos = []
    for tag_1 in male_aligned_tags:
        for tag_2 in female_aligned_tags:
            het_combos.append(f"{tag_1} / {tag_2}")
    for tag_1 in female_aligned_tags:
        for tag_2 in male_aligned_tags:
            het_combos.append(f"{tag_1} / {tag_2}")
    # any ambig or other involved ship combos
    other_x_women = []
    for tag_1 in other_tags:
        for tag_2 in female_aligned_tags:
            other_x_women.append(f"{tag_1} / {tag_2}")
    for tag_1 in female_aligned_tags:
        for tag_2 in other_tags:
            other_x_women.append(f"{tag_1} / {tag_2}")
    other_x_men = []
    for tag_1 in other_tags:
        for tag_2 in male_aligned_tags:
            other_x_men.append(f"{tag_1} / {tag_2}")
    for tag_1 in male_aligned_tags:
        for tag_2 in other_tags:
            other_x_men.append(f"{tag_1} / {tag_2}")
    other_x_other = []
    for tag_1 in other_tags:
        for tag_2 in other_tags:
            other_x_other.append(f"{tag_1} / {tag_2}")
    print(mlm_combos, wlw_combos, het_combos, other_x_women, other_x_men, other_x_other)

    return {
        "mlm": mlm_combos,
        "wlw": wlw_combos,
        "het": het_combos,
        "woman_attracted_other": other_x_women,
        "man_attracted_other": other_x_men,
        "other_x_other": other_x_other,
    }






# try and refactor the existing one but I think we'll make a lookup file for ease

# -> write some code to read in old characters file & extract relevant columns??
# idk.......

# our current version basically relies on partial lookups anyway (ie "all these names are in this order" etc)
# -> why wouldn't we just unify that into an actual lookup??? 

# I've copied stage 5 chars file & abbr char list with old names
    # -> combine into a new lookup??

# should we still have the other code to parse names 
# or are we assuming they will be few enough to add manually??
    # I think it'll be good to recreate/refactor the code I guesss.....

# # TODO temp func
# def make_char_lookup():
#     # read in both files (diff formats!)
#     # make into dfs
#     # join all data info to full names of full name & old name info
#     # -> make a lookup that has all new data attached to old names??
#     # or a json with an old names dict but also new names in there???
#     pass

# TODO func to read from lookup, check if char's in there, return other data if yes, print char if no
# -> if we still have cleaning funcs too we can then run those new characters through cleaning 
# & assigning funcs!
    # (we'll have to look em up manually anyway *sigh*)
    # -> saves time on cleaning already-researched characters 
    # but we still *can* clean/re-generate em if we need to
        # means we still gotta add em to our cleaning & assigning funcs when they're new then

# TODO refactor completing names func as well
# and gender & race assigning funcs too later

    # accents on the untamed boys seem to have been removed in latest ranking I think -> unify pls
    # also charlie magne morningstar from hazbin hotel seems to not be caught, 
    #   maybe they added her other last name by now? -> check

#########
# ok I got it:
# we make a file for fandoms & for characters
# of a dict of old version: clean version (ie new fandom or full name)
    # include fandom in characters one
    # make an rpf lookup for fandoms too??
# then we check old version we get against that dict
# if it's in the dict, we don't need to run cleaning bc we already know this one!
# if it's not in the dict, clean & print all of it -> then we can manually add it to dict

# then once we've cleaned all the names, we'll have a different lookup file later for gender & race info
# & maybe rpf info???
