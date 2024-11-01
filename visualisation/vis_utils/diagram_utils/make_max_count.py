def make_max_count(num_of_years:int):
    """
    determines max count (number of columns) depending on the number of years passed in (to match 
    the relevant sub plot layout)

    currently implemented numbers of years: 9 & 10
    """

    if num_of_years == 9:
        max_count = 3
    elif num_of_years == 10:
        max_count = 5
    elif num_of_years in [7,8]:
        max_count = 4

    return max_count