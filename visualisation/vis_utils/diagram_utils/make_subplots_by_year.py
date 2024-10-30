from plotly.subplots import make_subplots

def make_subplots_by_year(num_of_years:int, num_of_columns:int=False, by_years:bool=False):
    """
    makes a subplot figure with the appropriate layout per number of years given

    (currently implemented:)
    - 3x3 grid for 9 years (type: domain)
    - 2x5 grid for 10 years (type: domain)
    - if num_of_columns provided: 
        if by_years is True:
        - num_of_years x num_of_columns grid (type: table)
        otherwise:
        - num_of_years/num_of_columns (rounded up) x num_of_columns grid (type: table)
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
        elif num_of_years == 10:
            row = 2
            column = 5
        type_dict = {"type": "domain"}

    spec_row = [type_dict for _ in range(column)]
    spec_list = [spec_row for _ in range(row)]

    fig = make_subplots(rows=row, cols=column, specs=spec_list)

    return fig