from math import sqrt
from numpy import cov

# TODO test these

def calculate_standard_deviation(numbers:list, population:bool=True): # tested
    """
    takes a list of numbers

    returns their standard deviation number
    """
    if len(numbers) == 0:
        return None

    # if numbers is not entire population, but only a sample
    # we divide by len(numbers) - 1 instead of len(numbers)
    if population:
        length = len(numbers)
    else:
        length = len(numbers) - 1

    # take mean of all numbers
    average = calculate_mean(numbers)

    # calculate distance from mean of each number
    deviations = []
    for num in numbers:
        distance = (num - average)*(num - average) # these should always be positive or 0
        deviations.append(distance)

    # take mean of all deviations
    variance = calculate_mean(deviations, length)

    # standard deviation
    standard_deviation = round(sqrt(variance), 2)

    return standard_deviation

def calculate_mean(numbers:list, length:int=None): # tested
    """
    calculates the mean average of the numbers list using the length of the list by default 
    or the length provided if any, and rounds it to two decimal places
    """
    if len(numbers) == 0:
        return None

    if not length:
        length = len(numbers)

    average = round((sum(numbers) / length), 2)
    return average

def calculate_covariance(numbers_1:list, numbers_2:list): # tested
    """
    calculates covariance of two input lists and returns relevant number rounded to two decimal places
    """
    # apparently covariance is only about whether it's positive or negative??? 
    # to indicate whether the two numbers move in same direction or inversely??
    if len(numbers_1) == 0 or len(numbers_2) == 0:
        return None
    
    covariance = round(float(cov(numbers_1, numbers_2)[0,1]), 2)
    return covariance

def calculate_slope(x_axis_values:list, y_axis_values:list): # tested
    """
    calculates slope number for trendline of x and y axis input

    returns slope number
    """
    if len(x_axis_values) == 0 or len(y_axis_values) == 0:
        return None

    n = len(x_axis_values)

    sum_of_values_product = 0
    for index in range(n):
        sum_of_values_product += x_axis_values[index] * y_axis_values[index]

    a = n * sum_of_values_product # n * (sum of (x value * corresponding y value))

    b = sum(x_axis_values) * sum(y_axis_values) # (sum of x values) * (sum of y values)

    sum_of_squared_x_axis_values = 0
    for value in x_axis_values:
        sum_of_squared_x_axis_values += value * value

    c = n * sum_of_squared_x_axis_values # n * (sum of (x value * x value))

    d = sum(x_axis_values) * sum(x_axis_values)

    m = (a - b) / (c - d)

    return m

def calculate_y_intercept(x_axis_values:list, y_axis_values:list, slope:float): # tested
    """
    calculates y intercept for passed-in values, returns y intercept number
    """
    # y intercept refers to where on y axis the line passes through!

    if len(x_axis_values) == 0 or len(y_axis_values) == 0:
        return None

    x_mean = calculate_mean(x_axis_values)
    y_mean = calculate_mean(y_axis_values)

    y_intercept = y_mean - slope * x_mean

    return y_intercept


def calculate_trendline(x_axis_values:list, y_axis_values:list):
    """
    takes x and y axis' values 

    calculates their trendline

    returns a list of new y values to use for the trendline on the graph
    """
    if len(x_axis_values) == 0 or len(y_axis_values) == 0:
        return None

    # slope
    a = calculate_slope(x_axis_values, y_axis_values)

    # y-intercept
    b = calculate_y_intercept(x_axis_values, y_axis_values, a)

    # linear trendline
    # y_axis_values = a * x_axis_values + b
    trendline_y_axis_values = []
    for x in x_axis_values:
        new_value = round((a * x + b), 2)
        if new_value < 0: # we can't ever get less than 0 characters
            new_value = 0
        trendline_y_axis_values.append(new_value)

    return trendline_y_axis_values

    # TODO: current issues to fix:

        # in black folks' line's case (most extreme decrease), 
        # the decrease of the actual number is 1 or less each time, so 
        # the trend line should also decrease by 1 or less for each year, rIGHT???
        # but the "slope" is currently -4.72 -> should likely be closer to -1 or -0.smth
        # which bit is incorrect that causes this??

        # I tried changing x deviation to 1 -> from ca 3 that the function spits out and it 
        # literally didn't change the result??? how??

        # these are all the formulas I found online, I think they should be right??
        # r value also looks right (should be between 1 & -1 and is at -0.9 -> seems right!)

        # -> which of the other bits is messing us up? what went wrong here??

        # latin trendline looks right, but all the others seem very off

        # and the vis function won't let me put them on another axis than the main lines while also
        # keeping the main lines visible ToT

        # tldr: for black line, I'd assume the values would go from ca 5 to ca 0, 
        # as it is pretty straight forward of a distribution, yet for some reason they currently go from like 
        # 23 to -18, which is just utterly too extreme for what we're working with???

        # for rest of asia line I'd assume it'd go from ca 4 to ca 3
        # for MENA & indig, I'd assume it'd stay firmly within the 0-1 range

        # maybe it's worth doing TDD about at this point :l
