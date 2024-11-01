def edit_ranking_df_columns(input_df_dict:dict, ranking:str):
    """
    takes output dict from make_yearly_df_dict and a ranking string ("femslash"|"overall"|"annual")

    returns a new dict with new dataframes, where:
    - the "new_works", "release_date", and "data_set" columns have been removed, 
    a "year" column has been added, and in the first year of data per set the "change" column 
    has been filled with "new" rather than None values
    - additionally, if ranking="overall":
        all ranks above 100 have been removed, and in the 2014 set, the "change" column 
        has been filled with "old" values where there were None values ("new" values stay intact)
    """

    new_df_dict = {}

    for year in input_df_dict:
        new_df = input_df_dict[year].copy()

        if ranking in ["femslash", "overall", "annual"]:
            # drop new works cause it's an overall ranking
            new_df.pop("new_works")

            # and release date cause we're not tracking that yet
            new_df.pop("release_date")

            # and replace data set name column with just year cause 
            # it's only one data set we're looking at for now
            new_df.pop("data_set")
            new_df["year"] = year

        if (ranking == "femslash" and year == 2014) \
        or (ranking == "overall" and year == 2013) \
        or (ranking == "annual" and year == 2016):
            new_df["change"] = "new" # getting rid of none values
        
            if ranking == "overall":
                # getting rid of extra ranks in 2013
                new_df = new_df.where(new_df["rank_no"] <= 100).dropna()

        if ranking == "overall" and year == 2014:
            new_df["change"] = new_df["change"].where(cond=new_df["change"] == "new", other="old")

        new_df_dict[year] = new_df

    return new_df_dict