#TODO:
# data set table: ✅
# - go through (sorted?) list of filepaths ✅
# - collect:
    # - year ✅
    # - type ✅
# - set website to be "AO3" for all these ones ✅
# possibly convert to a csv file instead of json due to no collection values or anything? ✅
    # use util ✅

# characters table:
# (they all have their fandom in their dicts, so don't need to be classified by those)
# - un-categorise them -> we want a list of char names (as keys w dict values)
    # - I think we have a few names that are doubled (like "Ruby"), 
    # so maybe have the keys as like "name from fandom" or something
    # -> we can then either split by " from " or simply query the 
    # full_name/fandom key inside the value
# - add rpf or fic value
# - if we extract & save op versions in a separate file we can save this as a csv o.o
    # - extract op versions & save separately under same key names!
    # as in like {fandom_character_key: [op_version, op_version_2, ...], ...}
    # -> save as json
    # - find longest list in this dict
    # - make a list of lists w key + that many columns (possibly new name & fandom in there too)
    # -> insert none values for any that have less than max
    # -> make old names csv

# main sets:
# - sort characters in relationship alphabetically
# - get number of characters in relationship
# - de-list characters (?) -> where less than max num "none" for other characters
# - remove gender from type column - replace with gen or slash only
# - remove race column
# - make rank a simple number
    # possibly add a "tied" column???
# - make change a simple value (ie pos. num, neg. num, "new", none)
# - add data set column


# this file should be the one running the functions & creating all the files in question
# rather than each file its own files
# -> so we only have to run this file