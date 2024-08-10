from src.util_functions.get_file_paths import find_paths
from src.util_functions.attempting_pandas import json_list_of_dicts_to_data_frame

def gather_all_raw_characters():
    """
    returns a list of all unique character names from the stage 3 data sets
    """
    name_list = []

    all_paths = find_paths("data/third_clean_up_data/")

    for path in all_paths:
        read_df = json_list_of_dicts_to_data_frame(path)
        relationship_list = list(read_df["Relationship"])
        name_list.extend(relationship_list)

    unique_list = sorted(list(set(name_list)))

    return unique_list
#TODO: test

def remove_brackets(character_list):
    """
    takes a list of unique character names, removes all suffixes in brackets ()

    returns a dict in the format of {<old_name>: <new_name>, ...}, 
    with a key for each value in the input list
    """
    name_dict = {}

    for old_name in character_list:
        if "(" in old_name:
            for char in range(len(old_name)):
                if old_name[char] == "(":
                    bracket_index = char - 1 # including preceding whitespace
            new_name = old_name[:bracket_index]
        else: new_name = old_name

        name_dict[old_name] = new_name
        # -> so we can say "if it was this, make it this", 
        # and avoid double trouble between fandoms or same character formatted differently
        # in testing we'll also be able to check that same amount of keys as input names

    return name_dict
#TODO: test

#TODO:
    # check that bracket caused doubles have been removed
    # separate & collect name parts
        # split at " | " for aliases
        # split at white spaces afterwards
    # categorise name parts
        # if split item starts & ends on ' -> it's a nickname
        # figure out which bits are first names, last names & aliases
    # complete name parts where missing
        # complete first/last names where missing from one double but present in the other
        # add aliases where obviously missing
        # add translations if you can find a reliable way to scrape the info 
        #   cause fucking hell it'd be a lot of work otherwise ToT


# pandas will be hecking useful for some of this current shuffling things about!
    # I am tempted to like- refactor a bunch of my functions to use pandas instead ToT
# update: we can use pandas to add the clean info to our main data sets, 
# but I still think it'll be easier to do the cleaning manually in regular python
# where I feel like I can have more control (with my current skills) and flexibility

(
#things to fix at a glance:
    # fix misattributed late-addition music groups ✅

    # RM form bts is doubled
    # so is xiao zhan/sean from untamed
    # mcr is both doubled up
    # the expected first name/last name order inconsistency issue w a lot of names
    # a buncha doubles among the youtubers

    # there's a few doubles in AoT
    # critical role has doubles
    # DC has a suspicious lack of aliases, pls fix in formatting later
    # dragon age has doubles
    # elsa frozen is double
    # crowley good omens is double
    # america hetalia is double
    # les mis has doubles
    # lost girl lauren is double
    # of course there's marvel doubles, and same as w dc a sus lack of aliases
    # mass effect has male & female & non-specified shepard 
    #   -> figure out what regular shepard was classed as gender-wise
    # merlin has doubles
    # as does miraculous ladybug
    # mha has doubles & lacks some aliases
    # naruto has a double
    # rumpelstiltskin once upon a time still misspellt & therefore double
    # zosan one piece lacking their aliases
    # pretty sure mccree's dead name in overwatch, also missing aliases
    # person of interest has a double
    # pitch perfect has a double
    # as does power rangers
    # and queer as folk
    # are jim & james moriarity the same person in sherlock holmes? if so they're double
    # star trek has double
    # star wars has kylo double
    # so many steven universe doubles
    # reader & you doubled up in supernatural
    # tmnt have doubles
    # the 100 has doubles
    # last of us ellie is double
    # undyne undertale is double
    # as is lance voltron
# the rest looks fine but we'll have to see if everyone is accounted for later    
)

#TODO:
# remove doubles
    #doubles are generally caused by:
        # missing parts of names vs present ones
        # brackets specifying property we don't need to specify
    # -> remove brackets ✅
    # for missing name parts more formatting is needed (see above)

# add original fandom instances to character profiles
    # eg their fandom may have many instances but they were only listed for these ones specifically
    # -> to keep track of that as we clean, same as w fandoms
# make a file that contains 
    # new name of character
    # all old names of character
    # fandom they're from (new name)
    # og instances of fandom they were listed with
    # -> to look up & replace main files from later

# -> other details will be in their separate files to be in their own tables later!
    # we should make a file that doesn't have two keys but instead is json lines or csv format
    #   with all RPF & fictional fandoms mixed in
    #   w the respective fandom's details in one line
    # and then another one to do the same w characters & their details

# add gender where same-sex slash pairings
    # start from latest info
    # do not replace after it's been added
    # if it's not a same-sex slash pairing, hence has another label, 
    #   find a way to skip or keep track of other label
# same for race where in order or same
    # from most recent info, do not replace w older info
    # otherwise keep track of untouched labels for later research & categorisation


# - adding types of media for fictional category
        # -many fandoms will have multiple adaptations
        # -categories I def saw so far:
            # movies (live action)
            # TV (live action)
            # web series
            # comics
            # books
            # musicals
            # animation
        # (if I find more translated versions from international properties in 
        # this research process I shall add them to their names as a case in previous function)
    # -> also add country of origin while we're at it
        # eg anime wouldn't be labelled anime, simply as "animation" from "japan"
        # -countries are easy enough to look up while looking up the property itself
        # -some fandoms may have international adaptations, hence have several countries listed
            # ex one piece from japan, but has a western adaptation now too
            # -how do we handle shows that are produced cross-countries tho? 
            # like where it was shot & made across more than one country per thing
            # & actors f.e. are from all over the place too (like the one piece example,
            # does it have an official country of origin? do we count it as US american? 
            # there were so many british ppl tho, 
            # and I know how much the americans produce over here)
                # maybe count it as the country that the production company is sitting in
                # even if it was shot/made elsewhere
                # as that's who came up with the idea & spent the money & now owns the thing
                # ex new batman movie was shot in the UK but would count 
                # as american cause the americans produced it right?
        # -for RPF list country of origin/residence of people in question
        # or where present country(ies) of origin of the media they are famous for
            # eg kpop groups should be listed as korean (even if some of the members aren't)
            # eg US american movies/TV should be listed as US american
            # but eg youtubers or sports are global categories, 
                # so should be listed for specific ppl involved instead
    # and release years while we're at it where possible
        # where it's many things we should add them individually maybe (like marvel & DC)
        # for series/franchises that spanned multiple years include beginning & end years
