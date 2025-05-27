from json import load
from data.reference_and_test_files.refactor_helper_files.old_character_names_lookup import OLD_CHARACTERS_LOOKUP
from data.reference_and_test_files.refactor_helper_files.old_fandom_names_lookup import OLD_FANDOMS_LOOKUP

data_folder = "data/reference_and_test_files/refactor_helper_files/old_files_for_ref"


## get characters (with their fandoms)

# read og json file we have
char_names_filepath = f"{data_folder}/characters_full_names_and_old_versions.json"
with open(char_names_filepath, "r") as json_file:
    read_data = load(json_file)
# keys are fandoms
# fandoms contain clean names of characters
# which contain "op_versions" key which is a list of all og names

# this currently only works for data structure from above file
og_names = {}
for fandom in read_data:
    for char in read_data[fandom]:
        op_versions = read_data[fandom][char]["op_versions"]
        for og in op_versions:
            fandom_og = f"{fandom} - {og}"
            if fandom_og not in OLD_CHARACTERS_LOOKUP: # check against what we already have in lookup
                og_names[fandom_og] = char
print(og_names) # print anything that isn't in the lookup yet


## get fandoms

fandoms_filepath = f"{data_folder}/fandoms_clean_names_and_old_versions.json"
with open(fandoms_filepath, "r") as json_file:
    read_data = load(json_file)
# structure is {fandom : [list of old versions]}

# this currently only works for data structure from above file
og_fandoms = {}
for fandom in read_data:
    for og in read_data[fandom]:
        if og not in OLD_FANDOMS_LOOKUP:
            og_fandoms[og] = fandom
print(og_fandoms) # print anything that isn't in the lookup yet








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
