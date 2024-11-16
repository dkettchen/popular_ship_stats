from plotly.subplots import make_subplots

def make_subplots_by_year(num_of_years:int, num_of_columns:int=False, by_years:bool=False):
    """
    makes a subplot figure with the appropriate layout per number of years given

    (currently implemented:)
    - 3x3 grid for 9 years (type: domain)
    - 2x5 grid for 10 years (type: domain)
    - 2x4 grid for 7 & 8 years (type: domain)
    - if num_of_columns provided: 
        if by_years is True:
        - num_of_years x num_of_columns grid (type: table)
        otherwise:
        - num_of_years/num_of_columns (rounded up) x num_of_columns grid (type: table)
        - either way the spacing between plots will be reduced to 0.01
    """

    if num_of_columns and not by_years: # if we want to distribute the years across custom column num
        row = num_of_years / num_of_columns
        if row != int(row):
            row += 1
        row = int(row)
        column = num_of_columns
        type_dict = {"type": "table"}
    elif num_of_columns: # if we want a years x columns grid
        row = num_of_years
        column = num_of_columns
        type_dict = {"type": "table"}
    else: # preset grid shapes per year num (type:domain)
        if num_of_years == 9:
            row = 3
            column = 3
        elif num_of_years in [10, 8,7,6,5,4]: # 2 rows
            row = 2
            if num_of_years % 2 == 0:
                column = int(num_of_years / 2)
            else: 
                column = int((num_of_years / 2) + 1)
        else:
            row = 1
            column = num_of_years
        type_dict = {"type": "domain"}

    spec_row = [type_dict for _ in range(column)]
    spec_list = [spec_row for _ in range(row)]

    if num_of_columns:
        fig = make_subplots(
            rows=row, cols=column, specs=spec_list, 
            horizontal_spacing=0.01, vertical_spacing=0.01
        )
    else: 
        fig = make_subplots(rows=row, cols=column, specs=spec_list)

    return fig

def make_subplots_by_year_new_wip(
        num_of_years:int, ranking:str, 
        by_columns:int=False, by_years:bool=False, 
        type_dict:str=None
):
    """
    creates a figure with relevant grid of subplots

    - if only given num_of_years & ranking:
        - if end date is 2023, creates a 2x5 grid (to fit up to 10 years)
        - if end date is 2024 or 2025, creates a 3x4 grid (to fit up to 12 years)
        - type will be set to {"type": "domain"} by default
    - if given a by_columns number:
        - creates a grid of that number of columns 
            - if by_years=False(default): with the rows necessary to fit the years (ie rounded up)
            - if by_years=True: with a number of rows equal to the numb_of_years
        - type will be set to {"type": "table"} by default
        - spacing between tables will be set to 0.01
    """

    if not type_dict: # if no given type_dict
        if by_columns: # table
            type_dict = {"type": "table"}
        else: # domain
            type_dict = {"type": "domain"}
    
    if ranking == "femslash": # started 1 year after 2013 (2014)
        num_of_years += 1
    elif ranking == "annual": # started 3 years after 2013 (2016)
        num_of_years += 3

    if by_columns: # given column number
        column = by_columns
        if by_years: # one row per each year
            row = num_of_years
        elif by_columns: # rows that fit years
            row = num_of_years / by_columns
            if row != int(row): # if not whole number
                row += 1 # rounding up
            row = int(row)
    elif num_of_years in [7,8]: # 2x4
        column = 4
        row = 2
    elif num_of_years == 9: # 3x3
        column = 3
        row = 3
    elif num_of_years == 10: # 2x5
        column = 5
        row = 2
    elif num_of_years in [11,12]: # 3x4
        column = 4
        row = 3

    spec_row = [type_dict for _ in range(column)]
    spec_list = [spec_row for _ in range(row)]

    if by_columns:
        fig = make_subplots(
            rows=row, cols=column, specs=spec_list, 
            horizontal_spacing=0.01, vertical_spacing=0.01
        )
    else: 
        fig = make_subplots(rows=row, cols=column, specs=spec_list)

    return fig