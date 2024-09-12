import sys
import unittest
from io import StringIO
from unittest.mock import patch

from pagination import (
    validate_input_data,
    trim_pages,
    create_string_values_and_insert_dots,
    calculate_range_of_pages,
    generate_pagination
)


class TestValidateInputData(unittest.TestCase):

    def test_negative_current_page(self):
        with self.assertRaises(ValueError):
            validate_input_data(-1, 10, 1, 0)

    def test_zero_current_page(self):
        with self.assertRaises(ValueError):
            validate_input_data(0, 10, 1, 0)

    def test_non_integer_current_page(self):
        with self.assertRaises(ValueError):
            validate_input_data("1", 10, 1, 0)

    def test_negative_total_pages(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, -10, 1, 0)

    def test_zero_total_pages(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, 0, 1, 0)

    def test_non_integer_total_pages(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, "10", 1, 0)

    def test_negative_boundaries(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, 10, -1, 0)

    def test_zero_boundaries(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, 10, 0, 0)

    def test_non_integer_boundaries(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, 10, "1", 0)

    def test_negative_around(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, 10, 1, -1)

    def test_non_integer_around(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, 10, 1, "1")

    def test_boundaries_greater_than_total_pages(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, 5, 6, 2)

    def test_current_page_greater_than_total_pages(self):
        with self.assertRaises(ValueError):
            validate_input_data(6, 5, 1, 2)

    def test_current_page_with_specific_around(self):
        with self.assertRaises(ValueError):
            validate_input_data(1, 5, 1, 5)


class TestTrimPages(unittest.TestCase):

    def test_pages_starting_below_one(self):
        result = trim_pages([-2, -1, 0, 1, 2, 3], 10)
        self.assertEqual(result, [1, 2, 3])

    def test_pages_ending_above_total_pages(self):
        result = trim_pages([8, 9, 10, 11, 12], 10)
        self.assertEqual(result, [8, 9, 10])

    def test_pages_both_out_of_bounds(self):
        result = trim_pages([0, 1, 2, 3, 4, 5, 6, 7, 8], 7)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7])

    def test_pages_within_bounds(self):
        result = trim_pages([1, 2, 3, 4, 5], 5)
        self.assertEqual(result, [1, 2, 3, 4, 5])


class TestCreateStringValuesAndInsertDots(unittest.TestCase):

    def test_pages_without_gap(self):
        result = create_string_values_and_insert_dots([1, 2, 3, 4, 5])
        self.assertEqual(result, ["1", "2", "3", "4", "5"])

    def test_pages_with_one_gap(self):
        result = create_string_values_and_insert_dots([1, 2, 3, 5, 6])
        self.assertEqual(result, ["1", "2", "3", "...", "5", "6"])

    def test_pages_with_multiple_gaps(self):
        result = create_string_values_and_insert_dots([1, 2, 4, 7, 8])
        self.assertEqual(result, ["1", "2", "...", "4", "...", "7", "8"])

    def test_single_page(self):
        result = create_string_values_and_insert_dots([1])
        self.assertEqual(result, ["1"])

    def test_empty_list(self):
        result = create_string_values_and_insert_dots([])
        self.assertEqual(result, [])

    def test_first_gap(self):
        result = create_string_values_and_insert_dots([1, 3, 4, 5])
        self.assertEqual(result, ["1", "...", "3", "4", "5"])

    def test_last_gap(self):
        result = create_string_values_and_insert_dots([1, 2, 3, 4, 6])
        self.assertEqual(result, ["1", "2", "3", "4", "...", "6"])


class TestCalculateRangeOfPages(unittest.TestCase):

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.held

    def test_two_gaps_pagination(self):
        calculate_range_of_pages(5, 10, 1, 2)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1 ... 3 4 5 6 7 ... 10")

    def test_full_range_pagination(self):
        calculate_range_of_pages(5, 10, 10, 1)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1 2 3 4 5 6 7 8 9 10")

    def test_edge_current_page_near_start(self):
        calculate_range_of_pages(2, 10, 2, 1)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1 2 3 ... 9 10")

    def test_edge_current_page_near_end(self):
        calculate_range_of_pages(9, 10, 2, 1)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1 2 ... 8 9 10")

    def test_large_around_value(self):
        calculate_range_of_pages(5, 10, 1, 5)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1 2 3 4 5 6 7 8 9 10")

    def test_zero_around(self):
        calculate_range_of_pages(5, 10, 1, 0)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1 ... 5 ... 10")

    def test_current_page_equals_total_pages(self):
        calculate_range_of_pages(10, 10, 2, 1)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1 2 ... 9 10")

    def test_current_page_is_first(self):
        calculate_range_of_pages(1, 10, 1, 1)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1 2 ... 10")

    def test_single_page(self):
        calculate_range_of_pages(1, 1, 1, 0)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "1")


class TestGeneratePagination(unittest.TestCase):

    def test_too_few_arguments(self):
        with self.assertRaises(ValueError) as context:
            generate_pagination(1, 10, 1)
        self.assertEqual(str(context.exception), "Pagination data must have exactly four items.")

    def test_too_many_arguments(self):
        with self.assertRaises(ValueError) as context:
            generate_pagination(1, 10, 1, 1, 5)
        self.assertEqual(str(context.exception), "Pagination data must have exactly four items.")

    def test_no_arguments(self):
        with self.assertRaises(ValueError) as context:
            generate_pagination()
        self.assertEqual(str(context.exception), "Pagination data must have exactly four items.")


class TestGeneratePaginationFunctionCalls(unittest.TestCase):

    @patch("pagination.validate_input_data")
    @patch("pagination.calculate_range_of_pages")
    def test_main_functions_called_once(self, mock_calculate_range, mock_validate_input):
        generate_pagination(7, 50, 1, 2)
        mock_validate_input.assert_called_once()
        mock_calculate_range.assert_called_once()

    @patch("pagination.create_string_values_and_insert_dots")
    def test_create_string_values_and_insert_dots_called(self, mock_create_string):
        generate_pagination(7, 50, 1, 2)
        mock_create_string.assert_called_once()

    @patch("pagination.trim_pages")
    def test_trim_pages_called_when_needed(self, mock_trim_pages):
        generate_pagination(1, 10, 1, 1)
        mock_trim_pages.assert_called_once()

    @patch("pagination.trim_pages")
    def test_trim_pages_not_called_when_not_needed(self, mock_trim_pages):
        generate_pagination(5, 10, 1, 2)
        mock_trim_pages.assert_not_called()


if __name__ == "__main__":
    unittest.main()
