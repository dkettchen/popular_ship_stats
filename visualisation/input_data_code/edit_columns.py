def edit_ranking_df_columns(input_df_dict:dict, ranking:str):
    """
    takes output dict from make_yearly_df_dict

    returns a new dict with new dataframes, where (currently implemented:)
    - if ranking="femslash":
        the "new_works", "release_date", and "data_set" columns have been removed, 
        a "year" column has been added, and in the 2014 set, the "change" column has been 
        filled with "new" rather than None values
    - if ranking="overall":
        the "new_works", "release_date", and "data_set" columns have been removed, 
        a "year" column has been added, and in the 2013 set, the "change" column has been 
        filled with "new" rather than None values, and all ranks above 100 have been removed
    """

    new_df_dict = {}

    for year in input_df_dict:
        new_df = input_df_dict[year].copy()

        if ranking in ["femslash", "overall"]:
            # drop new works cause it's an overall ranking
            new_df.pop("new_works")

            # and release date cause we're not tracking that yet
            new_df.pop("release_date")

            # and replace data set name column with just year cause 
            # it's only one data set we're looking at for now
            new_df.pop("data_set")
            new_df["year"] = year

        if (ranking == "femslash" and year == 2014) \
        or (ranking == "overall" and year == 2013):
            new_df["change"] = "new" # getting rid of none values
        
            if ranking == "overall":
                # getting rid of extra ranks in 2013
                new_df = new_df.where(new_df["rank"] <= 100).dropna()

        new_df_dict[year] = new_df

    return new_df_dict