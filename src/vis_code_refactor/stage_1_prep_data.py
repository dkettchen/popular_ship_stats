# TODO 
# a func that takes a df of a total data set or a yearly ranking data set,
# and a case
# that then prepares the data requested by the case from the given data set
# ex. "race percent" might give a series of all our race labels along with the % of characters 
# in the given data set that had that label

import pandas as pd
from re import split

def prep_data(df:pd.DataFrame, case:str):
    """
    prepares the given data set in the requested manner and returns a new series or df (depending on case)

    if something goes wrong (eg invalid case entered), prints & returns None

    - case="{column_name}_count" - returns count 
    for each label in relevant column as a series
    - case="{column_name}_percent" - returns rounded percentage of total 
    for each label in relevant column as a series

    - case="group_by_{gender_alignment|race_combo_category|multiracial|interracial|east_west}" - returns 
    a new df with one added column of the same name (ie given case str minus "group_by_" bit) 
    with group labels for the requested case or multiple added columns with group names and bool values
        - gender_alignment (chars) -> ["{female|male|no|unspecified} alignment"]
        - race_combo_category (ships) -> will add 4 new columns with bools as ships can be 
        part of multiple categories: "white-involved"|"EA-involved"|"non-white"|"non-white/non-EA"
        - multiracial (chars) -> ["multiracial"|"non-multiracial"|"ambiguous"]
        - interracial (ships) -> ["interracial"|"non-interracial"|"ambiguous"]
        - east_west (big 6 country data) -> ["eastern_countries"|"western_countries"]

    - case="{male|female|mlm|wlw|het|other_gender_combo|white-involved|EA-involved|non-white|non-white/non-EA|
    minority_genders|minority_races|rpf|fictional|big_countries|
    {country name}_country|{continent name}_continent|
    eastern_countries|western_countries}_subset" - returns a new, shortened df with only the 
    requested subset of data
        - male/female (chars) - returns only rows with male/female aligned characters
        - mlm/wlw/het (ships) - returns only rows with relevant gender combo non-gen ships 
        (including if M | Other, F | Other or M | F | Other characters are involved, 
        ex two cis-male drag queens will still be counted as mlm, 
        ex the crystal gems will still be counted as wlw)
        - other_gender_combo (ships) - returns any non-gen ships that are not covered by mlm/wlw/het subsets
        - {race_combo_category} (ships) - returns only rows with the requested race combo category
        - minority_genders (chars) - returns only rows with characters that aren't tagged as "F" or "M"
        - minority_races (chars) - returns only rows with characters that aren't white, east asian, non-human, 
        ambiguous, or of unknown race
        - rpf/fictional (rpf data) - returns only rows with rpf/fictional status
        - big_countries (country data) - returns only rows from our 6 most-represented countries of origin, 
        namely: USA, UK, Canada, Japan, South Korea, China
        - {country name}_country (country data) - returns only rows from the requested country 
        (country must contain the usual spaces & capitalisation f.e. "South Korea_country_subset")
        - {continent name}_continent (continent data) - returns only rows from the requested continent 
        (continent must contain the usual spaces & capitalisation f.e. "North America_continent_subset")
        - eastern_countries/western_countries (country data, optionally: already big_countries subset 
        grouped by east_west) - returns only rows from the requested hemisphere's big 3, 
        namely: USA/UK/Canada for the west, Japan/South Korea/China for the east
    
    - case="{dimension}_by_{subgroup}" - returns a df with sub group columns, dimension value indexes, and 
    the counts of the dimension for each subgroup
    (ex. "orientation_by_gender_alignment" => columns will be gender categories, index will be orientation labels,
    and the values will be the number of characters of that gender category that have that orientation)
        - can be either an existing column name or one of the columns group_by_ creates

    """
    new_df = df.copy()

    # figuring out which country_of_origin column to use
    # TODO repeat for continent
    if "country" in case:
        # if plain "country_of_origin" is a column -> use that
        if "country_of_origin" in new_df.columns:
            country = "country_of_origin"
        # otherwise use char specific column if any 
        # (TODO this should only be in char version, not ship version, but check pls)
        elif "char_country_of_origin" in new_df.columns:
            country = "char_country_of_origin"
        # otherwise use fandom specific column if any
        elif "fandom_country_of_origin" in new_df.columns:
            country = "fandom_country_of_origin"
        else: print(f"No country of origin column found. Received case: {case}; Columns: {list(new_df.columns)}")

    if case[-6:] == "_count": # count by label
        # name/ship column to use as correct count
        for name in [
            "name", # character reference file
            "Name", # character joined ranking file
            "ship_name", # ship reference file
            "Relationship", # (joined) ranking file
            "total_years", # fandom reference file bc it doesn't have a "fandom" column, that's the index
        ]:
            if name in new_df.columns:
                break
        
        grouping_column = case[:-6]
        if grouping_column not in new_df.columns:
            print(f"Requested column is not in given df. Received case: {case}; Columns: {list(new_df.columns)}")
            return None

        srs = new_df.groupby(grouping_column).count()[name]
        return srs
    
    elif case[-8:] == "_percent": # percentage by label
        total_len = len(new_df)
        grouping_column = case[:-8]
        if grouping_column not in new_df.columns:
            print(f"Requested column is not in given df. Received case: {case}; Columns: {list(new_df.columns)}")
            return None
        srs = prep_data(new_df, f"{grouping_column}_count").apply(make_percent, args=(total_len,))
        return srs
    
    elif "group_by_" in case: # add column(s) of requested groupings to df & return
        grouping_case = case[9:]
        groups = df.copy()
        groups[grouping_case] = "To be set"
        if grouping_case == "gender_alignment": # takes chars
            for alignment in ["female", "male", "no", "undefined"]:
                if alignment == "female":
                    sub_group = ["F", "F | Other"]
                elif alignment == "male":
                    sub_group = ["M", "M | Other", "M | F | Other"]
                elif alignment == "no":
                    sub_group = ["Other"]
                elif alignment == "unspecified":
                    sub_group = ["Ambig", "Unknown"]
                groups[grouping_case] = groups[grouping_case].mask(
                    groups["gender"].isin(sub_group), other=f"{alignment} alignment"
                )
        elif grouping_case == "race_combo_category": # takes ships
            groups.pop(grouping_case) # don't need that in this one
            for categ in ["white-involved", "EA-involved", "non-white", "non-white/non-EA"]:
                groups[categ] = None

                # white involved & EA involved
                if "involved" in categ:
                    if "white" in categ:
                        tag = "White"
                    elif "EA" in categ:
                        tag = "(?:^|\s)E Asian" #  so we don't catch SE Asians
                    # race combo must contain white/ea
                    groups[categ] = groups[categ].mask(
                        groups["race_combo"].str.contains(tag),
                        other=True
                    )
                # non white & non white or EA
                elif "non" in categ:
                    tags = ["White|Eu Ind"] # excluding anna & elsa cause they white
                    if "EA" in categ:
                        tags += ["(?:^|\s)E Asian"] # so we don't catch SE Asians
                    else:
                        tags += ["There is no second tag"]
                    # race combo must not contain white and/or EA, nor NH, unknown or ambig
                    groups[categ] = groups[categ].mask(
                        ~(
                            (groups["race_combo"].str.contains(tags[0])) | (
                            groups["race_combo"].str.contains(tags[1])) | (
                            groups["race_combo"].str.contains("N.H.")) | (
                            groups["race_combo"].str.contains("Unknown")) | (
                            groups["race_combo"].str.contains("Ambig"))
                        ),
                        other=True
                    )
        elif grouping_case in ["multiracial", "interracial"]:
            if grouping_case == "multiracial":
                column = "race"
                tag = "multi"
            else:
                interracial_ambig_pairings = [
                    "Power Rangers - Kimberly Ann 'Kim' Hart | Pink Ranger x Trini Kwan | Yellow Ranger", 
                    # kim has been played by a half-indian lady & is otherwise white -> these guys are interracial!

                    "Voltron - Adam x Shiro", # adam don't *look* east asian so Imma assume they're interracial

                    # any genshin ship with kaeya & a white man in it
                    "Genshin Impact | 原神 - Albedo x Kaeya",
                    "Genshin Impact | 原神 - Diluc & Kaeya",
                    "Genshin Impact | 原神 - Diluc x Kaeya",
                
                    # any NH/ambig human relationship in homestuck
                    "Homestuck - Calliope x Roxy Lalonde",
                    "Homestuck - Kanaya Maryam x Rose Lalonde",

                    "The Owl House - Eda Clawthorne x Raine Whispers",
                    # unless we think raine might be just a very tan white person idk
                ]

                column = "race_combo"
                tag = "\/"
            # interracial/multiracial
            groups[grouping_case] = groups[grouping_case].mask(
                # contains / indicating two diff race tags
                (groups[column].str.contains(tag)) & (
                    # and either is not ambig or unknown 
                    # (as ambig/unknown member may be same race as other one)
                    (~((groups[column].str.contains("Ambig")) | (groups[column].str.contains("Unknown")))) | (
                    # or is one of our listed pairings that have an ambig member but we know are interracial
                    groups["Fandom_Relationship"].isin(interracial_ambig_pairings))
                ),
                other=grouping_case
            )
            # non-~
            groups[grouping_case] = groups[grouping_case].mask(
                # does not contain two race tags
                (~groups[column].str.contains(tag)) & (
                    # and is not ambig or unknown
                    ~((groups[column].str.contains("Ambig")) | (groups[column].str.contains("Unknown")))
                ),
                other=f"non-{grouping_case}"
            )
            # ambiguous
            groups[grouping_case] = groups[grouping_case].mask(
                # contains an ambig or unknown tag
                ((groups[column].str.contains("Ambig")) | (groups[column].str.contains("Unknown"))) & (
                # and is not in our known interracial ambig pairings
                ~groups["Fandom_Relationship"].isin(interracial_ambig_pairings)),
                other="ambiguous"
            )
        elif grouping_case == "east_west": # must have countries data joined on (& only contain big 6)
            western_countries = ["USA", "UK", "Canada"]
            eastern_countries = ["Japan", "South Korea", "China"]
            groups[grouping_case] = groups[grouping_case].mask(
                groups["country_of_origin"].isin(western_countries), other="western_countries"
            )
            groups[grouping_case] = groups[grouping_case].mask(
                groups["country_of_origin"].isin(eastern_countries), other="eastern_countries"
            )
        else: 
            print(f"Please enter a valid case. Received: {case}")

        return groups # df with additional column

    elif "_subset" in case: # retrieve only requested subset of df & return
        grouping_case = case[:-7]

        # using group_by_ recursion
        if "male" in grouping_case: # female or male (char data)
            # add a gender alignment column
            subset = prep_data(new_df, "group_by_gender")
            subset = subset.where(subset["gender_alignment"] == f"{grouping_case} alignment").dropna(how="all")
            subset.pop("gender_alignment")
        elif grouping_case in ["white-involved", "EA-involved", "non-white", "non-white/non-EA"]: # (ship data)
            # add category column
            subset = prep_data(new_df, "group_by_race_combo_category")
            subset = subset.where(subset["race_combo_category"] == grouping_case).dropna(how="all")
            subset.pop("race_combo_category")
        elif grouping_case in ["eastern_countries", "western_countries"]:
            # get big countries & add east/west column
            if "east_west" not in new_df.columns:
                subset = prep_data(prep_data(new_df, "big_countries_subset"), "group_by_east_west")
            else: subset = new_df
            # get only requested part
            subset = subset.where(subset["east_west"] == grouping_case).dropna(how="all")
            subset.pop("east_west")

        # simple exclusions based on existing columns
        elif "minority" in grouping_case: # _genders or _races (char data)
            column = grouping_case[9:-1]
            if column == "gender":
                exclusions = ["M", "F"]
            elif column == "race":
                exclusions = ["White", "E Asian", "N.H.", "Ambig", "Unknown",]
            subset = new_df.mask(
                new_df[column].isin(exclusions)
            ).dropna(how="all")
        elif grouping_case in ["mlm", "wlw", "het"]:
            # we're leaving out any other combos for now -> add if new relevant ships are added later
            if grouping_case == "mlm":
                labels = [
                    "M / M", 
                    "M / M | Other", 
                    "M | Other / M", 
                    "M | Other / M | Other", 
                    "M | F | Other / M | F | Other",
                ]
            elif grouping_case == "wlw":
                labels = [
                    "F / F", 
                    "F / F | Other", 
                    "F | Other / F", 
                    "F | Other / F | Other", 
                ]
            elif grouping_case == "het":
                labels = [
                    "M / F",
                    "F / M",
                ]
            subset = new_df.where(
                (new_df["gender_combo"].isin(labels)) & ~(new_df["ship_name"].str.contains("&"))
            ).dropna(how="all")
        elif grouping_case == "other_gender_combo":
            exclusions = [
                    "M / M", 
                    "M / M | Other", 
                    "M | Other / M", 
                    "M | Other / M | Other", 
                    "M | F | Other / M | F | Other",
                    "F / F", 
                    "F / F | Other", 
                    "F | Other / F", 
                    "F | Other / F | Other", 
                    "M / F",
                    "F / M",
                ]
            subset = new_df.where(
                ~(new_df["gender_combo"].isin(exclusions)) & ~(new_df["ship_name"].str.contains("&"))
            ).dropna(how="all")
        elif grouping_case in ["rpf", "fictional"]: # must have joined-on rpf data
            if grouping_case == "rpf":
                rpf = True
            else: rpf = False
            subset = new_df.where(new_df["rpf"] == rpf).dropna(how="all")
        elif grouping_case == "big_countries": # must have joined-on country data
            # our six biggest fandom-origins
            big_countries = ["USA", "UK", "Canada", "Japan", "South Korea", "China"]
            subset = new_df.where(new_df["country_of_origin"].isin(big_countries)).dropna(how="all")
        elif "_country" in grouping_case: # must have joined-on country data & case specify a valid country
            # get data for a given country
            subset = new_df.where(new_df[country] == grouping_case[:-8]).dropna(how="all")
        elif "_continent" in grouping_case: # must have joined-on country data & case specify a valid country
            # get data for a given country
            subset = new_df.where(new_df["continent"] == grouping_case[:-10]).dropna(how="all")
        # TODO how to deal with country of origin/continent column being renamed for fandom vs chars?
        else: 
            print(f"Please enter a valid case. Received: {case}")

        return subset # shortened df

    elif "_by_" in case: # count dimension by subgroup & return as df
        # extract requested items from case
        split_case = split("_by_", case)
        # checking input was correct
        if len(split_case) != 2: 
            print(f"Requested data should take the following format: [dimension]_by_[subgroup]. Received: {case}")
            return None
        dimension = split_case[0]
        sub_group = split_case[1]

        # all possible values of the requested dimension
        index = list(new_df[dimension].unique())
        # use as index for df
        cross_df = pd.DataFrame(index=index)

        # if it's an added column, add that first
        if sub_group in ["gender_alignment","race_combo_category","multiracial","interracial","east_west"]:
            new_df = prep_data(new_df, f"group_by_{sub_group}")
        
        # iterate through all sub groups in requested column
        for value in list(new_df[sub_group].unique()):
            # retrieve only this sub group's data
            subset = new_df.where(new_df[sub_group] == value).dropna()
            # count its requested dimension & add series as column to df
            cross_df[value] = prep_data(new_df,f"{dimension}_count")

        return cross_df

    else: # if smth went wrong & it didn't get caught by any of our cases
        print("Why did it not catch on anything?", case)
        return None

    # TODO:
    # gender combo subsets (mlm, wlw, het, other, ambig) (ship data) ✅
    # group_by_queer (queer, non-queer, ambig) (char data)
    # group_by_attraction (male-attracted, female-attracted, other-attracted, ambig, acearo) (char data)

    # subset of all queer characters?
        # orientation tag must be in ["bi", "gay", "acearo", "queer_unspecified"] 
        # or gender tag must contain "Other"
        # and then unspecified chars whose gender tag does not contain "Other"
        # and then str8 chars whose gender tag does not contain "Other"

        
    

# helper
def make_percent(number, total):
    """turns a number into its % of total (rounded to 2 decimal places)"""
    return round((number / total) * 100, 2)

