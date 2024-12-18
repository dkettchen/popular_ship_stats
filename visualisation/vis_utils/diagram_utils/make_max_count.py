def make_max_count(num_of_years:int):
    """
    determines max count (number of columns) depending on the number of years passed in (to match 
    the relevant sub plot layout)

    currently implemented numbers of years: 7, 8, 9 & 10
    """

    if num_of_years == 10:
        max_count = 5
    elif num_of_years in [7,8]:
        max_count = 4
    elif num_of_years in [9,6,5]:
        max_count = 3
    elif num_of_years == 4:
        max_count = 2
    else: max_count = num_of_years

    return max_count