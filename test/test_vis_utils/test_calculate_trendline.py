from visualisation.vis_utils.diagram_utils.calculate_trendline import (
    calculate_standard_deviation, 
    calculate_mean,
    calculate_covariance,
    calculate_slope,
    calculate_trendline, 
)

class TestStandardDeviation:
    def test_returns_float(self):
        input = [1,2,3,4]
        result = calculate_standard_deviation(input)
        assert type(result) == float

    def test_does_not_mutate_input(self):
        input = [1,2,3,4]
        calculate_standard_deviation(input)
        assert input == [1,2,3,4]

    def test_returns_none_for_empty_list(self):
        result = calculate_standard_deviation([])
        assert result == None

    def test_returns_zero_for_single_number_list(self):
        input = [4]
        result = calculate_standard_deviation(input)
        assert result == 0

    def test_returns_zero_for_same_number_list(self):
        input = [3,3,3]
        result = calculate_standard_deviation(input)
        assert result == 0

    def test_returns_population_standard_dev_by_default(self):
        # example off wikipedia
        input = [2,4,4,4,5,5,7,9]
        result = calculate_standard_deviation(input)
        assert result == 2

    def test_returns_sample_standard_dev_if_population_false(self):
        # ditto
        input = [2,4,4,4,5,5,7,9]
        result = calculate_standard_deviation(input, population=False)
        assert result == 2.14

    def test_returns_appropriate_number_for_different_number_list(self):
        # found some examples on the internet
        input_1 = [3,2,5,6]
        result_1 = calculate_standard_deviation(input_1)
        assert result_1 == 1.58
        input_2 = [6,6, 10,10,10, 12,12,12,12, 14,14,14,14,14, 24,24,24,24]
        result_2 = calculate_standard_deviation(input_2)
        assert result_2 == 5.73
        input_3 = [9, 2, 5, 4, 12, 7, 8, 11, 9, 3, 7, 4, 12, 5, 4, 10, 9, 6, 9, 4 ]
        result_3 = calculate_standard_deviation(input_3, False)
        assert result_3 == 3.06
        input_4 = [92, 95, 85, 80, 75, 50]
        result_4 = calculate_standard_deviation(input_4, False)
        assert result_4 == 16.23
        input_5 = [18, 22, 19, 25, 12]
        result_5 = calculate_standard_deviation(input_5, False)
        assert result_5 == 4.87

class TestMean:
    def test_returns_float(self):
        input = [1,2,3,4]
        result = calculate_mean(input)
        assert type(result) == float

    def test_does_not_mutate_input(self):
        input = [1,2,3,4]
        calculate_mean(input)
        assert input == [1,2,3,4]

    def test_returns_none_for_empty_list(self):
        result = calculate_mean([])
        assert result == None

    def test_returns_same_number_for_single_number_list(self):
        input = [4]
        result = calculate_mean(input)
        assert result == 4

    def test_returns_same_number_for_same_number_list(self):
        input = [3,3,3]
        result = calculate_mean(input)
        assert result == 3

    def test_returns_mean_of_2_number_list(self):
        input = [1,3]
        result = calculate_mean(input)
        assert result == 2

    def test_returns_mean_of_3_number_list(self):
        input = [2,3,4]
        result = calculate_mean(input)
        assert result == 3

    def test_returns_mean_of_longer_lists(self):
        # examples off the internet
        input_1 = [8, 9, 5, 6, 7]
        result_1 = calculate_mean(input_1)
        assert result_1 == 7
        input_2 = [6, 11, 7]
        result_2 = calculate_mean(input_2)
        assert result_2 == 8
        input_3 = [3, 7, 5, 13, 20, 23, 39, 23, 40, 23, 14, 12, 56, 23, 29]
        result_3 = calculate_mean(input_3)
        assert result_3 == 22

    def test_returns_mean_for_negative_numbers(self):
        # example off the internet
        input = [3, -7, 5, 13, -2]
        result = calculate_mean(input)
        assert result == 2.4

    def test_returns_sum_divided_by_given_length_if_provided(self):
        input = [1,2,3,4]
        result = calculate_mean(input, 5)
        assert result == 2

class TestCovariance:
    def test_returns_float(self):
        input_1 = [1,2,3,4]
        input_2 = [1,2,3,4]
        result = calculate_covariance(input_1, input_2)
        assert type(result) == float

    def test_does_not_mutate_input(self):
        input_1 = [1,2,3,4]
        input_2 = [5,6,7,8]
        calculate_covariance(input_1, input_2)
        assert input_1 == [1,2,3,4]
        assert input_2 == [5,6,7,8]

    def test_returns_none_for_empty_list(self):
        result = calculate_covariance([], [])
        assert result == None

    def test_returns_correct_covariance(self):
        # from examples off the internet
        input_1_1 = [1692, 1978, 1884, 2151, 2519]
        input_1_2 = [68, 102, 110, 112, 154]
        result_1 = calculate_covariance(input_1_1, input_1_2)
        assert result_1 == 9107.30

        input_2_1 = [1.2, 1.8, 2.2, 1.5]
        input_2_2 = [3.1, 4.2, 5.0, 4.2]
        result_2 = calculate_covariance(input_2_1, input_2_2)
        assert result_2 == 0.31

        input_3_1 = [2.1, 2.5, 4.0, 3.6]
        input_3_2 = [8, 12, 14, 10]
        result_3 = calculate_covariance(input_3_1, input_3_2)
        assert result_3 == 1.53

class TestSlope:
    def test_returns_float(self):
        input_1 = [1,2,3,4]
        input_2 = [1,2,3,4]
        result = calculate_slope(input_1, input_2)
        assert type(result) == float

    def test_does_not_mutate_input(self):
        input_1 = [1,2,3,4]
        input_2 = [5,6,7,8]
        calculate_slope(input_1, input_2)
        assert input_1 == [1,2,3,4]
        assert input_2 == [5,6,7,8]

    def test_returns_none_for_empty_list(self):
        result = calculate_slope([], [])
        assert result == None

    def test_returns_slope_within_range_it_should_be(self):
        # using a calculator I found online

        # example data I found online
        input_1_1 = [1, 2, 3.5, 4, 6, 7, 8, 9]
        input_1_2 = [8, 7, 7, 5.5, 5, 3.5, 2.5, 2.5]
        result_1 = calculate_slope(input_1_1, input_1_2)
        assert result_1 < -0.7225 + 0.06521
        assert result_1 > -0.7225 - 0.06521

        input_2_1 = [2,5,6,8,2,0]
        input_2_2 = [0,1,2,3,4,5]
        result_2 = calculate_slope(input_2_1, input_2_2)
        assert result_2 < -0.1896 + 0.2977
        assert result_2 > -0.1896 - 0.2977

        input_3_1 = [0,1,2,3,4]
        input_3_2 = [1,0,0,0,0]
        result_3 = calculate_slope(input_3_1, input_3_2)
        assert result_3 < -0.2000 + 0.1155
        assert result_3 > -0.2000 - 0.1155

        input_4_1 = [1,2,3,4]
        input_4_2 = [0,4,2,7]
        result_4 = calculate_slope(input_4_1, input_4_2)
        assert result_4 < 1.900 + 0.9327
        assert result_4 > 1.900 - 0.9327

    def test_returns_expected_slope_number(self):
        #example I found online
        input_1 = [1, 2, 3]
        input_2 = [3,5,6.5]
        result = calculate_slope(input_1, input_2)
        assert result == 1.75



# y intercept refers to where on y axis the line passes through!