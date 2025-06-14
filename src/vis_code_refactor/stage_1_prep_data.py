# TODO 
# a func that takes a df of a total data set or a yearly ranking data set,
# and a case
# that then prepares the data requested by the case from the given data set
# ex. "race percent" might give a series of all our race labels along with the % of characters 
# in the given data set that had that label

def prep_data(df, case):
    """
    - case="{column_name}_count" - returns count 
    for each label in relevant column as a series
    - case="{column_name}_percent" - returns rounded percentage of total 
    for each label in relevant column as a series
    - case="{male|female|minority_genders|minority_races|
    white_involved|EA_involved|non_white|non_white_EA}_subset" - returns df with only relevant subset
        - (char data:) male/female include male/female-aligned characters; 
        - (char data:) minority_genders/_races exclude their respective two biggest 
        and any non-relevant groups (aka "M"&"F"; "White","E Asian","N.H.","Ambig","Unknown")
        - (ship data:) white_/EA_involved/non_white/_white_EA classes by 
        whether or not the ship has white and/or east asian (including (multi)) 
        members depending on requested case
    """
    new_df = df.copy()
    total_len = len(new_df)

    # return none for any invalid cases
    srs = None

    # name/ship column to use as total
    for name in [
        "name", # character reference file
        "Name", # character joined ranking file
        "ship_name", # ship reference file
        "Relationship", # (joined) ranking file
        "fandom", # fandom reference file (unless that's index?? I think I set it as index)
    ]:
        if name in new_df.columns:
            break
    
    if "_count" in case: # count by label
        grouping_column = case[:-6]
        srs = new_df.groupby(grouping_column).count()[name]
    elif "_percent" in case: # percentage by label
        grouping_column = case[:-8]
        srs = prep_data(new_df, f"{grouping_column}_count").apply(make_percent, args=(total_len,))
    elif "_subset" in case: # retrieve only requested subset of df & return
        grouping_case = case[:-7]
        if "male" in grouping_case: # female or male (char data)
            column = "gender"
            if grouping_case == "female":
                sub_group = ["F", "F | Other"]
            elif grouping_case == "male":
                sub_group = ["M", "M | Other", "M | F | Other"]
            sub_set = new_df.where(
                new_df[column].isin(sub_group)
            ).dropna(how="all")
        elif "minority" in grouping_case: # _genders or _races (char data)
            column = grouping_case[9:-1]
            if column == "gender":
                exclusions = ["M", "F"]
            elif column == "race":
                exclusions = ["White", "E Asian", "N.H.", "Ambig", "Unknown",]
            sub_set = new_df.mask(
                new_df[column].isin(exclusions)
            ).dropna(how="all")
        elif grouping_case in ["white_involved", "EA_involved", "non_white", "non_white_EA"]: # (ship data)
            column = "race_combo"
            if "involved" in grouping_case:
                if "white" in grouping_case:
                    tag = "White"
                elif "EA" in grouping_case:
                    tag = "E Asian"
                sub_set = new_df.where(
                    new_df[column].str.contains(tag)
                ).dropna(how="all")
            elif "non" in grouping_case:
                tags = ["White"]
                if "EA" in grouping_case:
                    tags += ["E Asian"]
                else:
                    tags += ["There is no second tag"]
                sub_set = new_df.where(
                    (new_df[column].str.contains(tags[0])) | (new_df[column].str.contains(tags[1]))
                ).dropna(how="all")
        # subset of all multi characters?
            # race tag must contain multi
        # subset of all interracial ships?
            # race_combo tag must contain a "/"
        # subset of all queer characters?
            # orientation tag must be in ["bi", "gay", "acearo", "queer_unspecified"] 
            # or gender tag must contain "Other"
            # and then unspecified chars whose gender tag does not contain "Other"
            # and then str8 chars whose gender tag does not contain "Other"

        return sub_set # shortened df

    # specific cases where we wanna count a subset's labels or add items together into one bigger value
        # multi characters vs non-multi vs ambig/unknown
        # interracial vs non-interracial vs ambig/unknown
        # queer vs str8 vs unspecified chars
        # women & men's orientation labels
        
    # TODO
    # more specific cases:
    # - subsets to add from things we can count? 
        # ex no of multi chars or interracial ships or no of canon queer ppl etc
    # - cross references? 
        # ex how many mlm/wlw vs str8 vs acearo vs unspecified women/men we got? 
        # -> first get only gender then get counts of orientations


    return srs

# helper
def make_percent(number, total):
    """turns a number into its % of total (rounded to 2 decimal places)"""
    return round((number / total) * 100, 2)

