from visualisation.vis_utils.diagram_utils.calculate_trendline import calculate_trendline, calculate_standard_deviation

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

# test trendline