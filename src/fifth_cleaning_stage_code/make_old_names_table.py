# separating op versions:

# second func:
# take output from make character table func
# make dict of just the old names (possibly also full name & fandom), w same keys
# return that

# third func:
# take previous output
# locate longest list in dict values -> length n
# create a list of [key, full_name, fandom, n columns for old versions]
# -> this is our column titles
# then for each key make a list of "" values + all old values & then fill any missing length w none
# -> add to nested list
# return nested list

# print that nested list to a csv
    # use util