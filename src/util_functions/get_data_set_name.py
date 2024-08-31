def get_data_set_name(filepath):
    """
    takes a main data set filepath, checks which data set (currently only ao3 2013-2023 ones)
    it is from and returns that data set's key name
    """

    data_sets_list = [
        "AO3_2013_overall",
        "AO3_2014_femslash",
        "AO3_2014_overall",
        "AO3_2015_femslash",
        "AO3_2015_overall",
        "AO3_2016_data",
        "AO3_2016_femslash",
        "AO3_2016_overall",
        "AO3_2017_data",
        "AO3_2017_femslash",
        "AO3_2017_overall",
        "AO3_2019_data",
        "AO3_2019_femslash",
        "AO3_2019_overall",
        "AO3_2020_data",
        "AO3_2020_femslash",
        "AO3_2020_overall",
        "AO3_2021_data",
        "AO3_2021_femslash",
        "AO3_2021_overall",
        "AO3_2022_data",
        "AO3_2022_femslash",
        "AO3_2022_overall",
        "AO3_2023_data",
        "AO3_2023_femslash",
        "AO3_2023_overall"
    ]

    data_set = None

    for name in data_sets_list:
        if name[4:] in filepath:
            data_set = name

    return data_set