# Pagination and Tests

This project contains a simple pagination algorithm and its corresponding unit tests. The code allows you to calculate and display a range of page numbers, including the ability to show boundaries, skip pages, and handle edge cases.

## Files

- **pagination.py**: This file contains the core logic for pagination, including functions to validate input data, calculate the range of pages, trim out-of-bounds pages, and generate a string representation of the pagination.
- **test_pagination.py**: This file contains unit tests for the functions in `pagination.py`, ensuring that the logic handles various input scenarios and edge cases correctly.

## Features

- **Input Validation**: Ensures that all inputs are valid integers, checks that the current page does not exceed the total number of pages, and verifies that boundaries and "around" values are logical.
- **Page Trimming**: Handles situations where the page range may exceed the total number of pages.
- **Gaps with Ellipses**: Automatically inserts ellipses ("...") in place of skipped pages.
- **Customizable Boundaries and Surrounding Pages**: You can define how many pages should be displayed at the start/end and around the current page.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alonasorochynska/pagination-and-tests.git
   ```
2. Change into the project directory:
   ```bash
   cd pagination-and-tests
   ```
3. (Optional) Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```
## Usage
To use the pagination system, run the pagination.py file directly. For example:

   ```bash
   python pagination.py
   ```

You can modify the generate_pagination() function call at the end of the script with your desired inputs. For example:

   ```bash
   generate_pagination(current_page, total_pages, boundaries, around)
   ```

Where:

- `current_page`: The page currently being viewed.
- `total_pages`: The total number of pages.
- `boundaries`: The number of pages to show at the start and end.
- `around`: The number of pages to show around the current page.

### Example
   ```bash
   generate_pagination(7, 50, 1, 2)
   ```
This will generate a pagination range for page 7, out of a total of 50 pages, with 1 boundary page at the start and end, and 2 pages around the current page.

## Running the Tests
The unit tests are written using the unittest framework and cover all key functions of the pagination logic. To run the tests:

   ```bash
   python -m unittest discover
   ```
Alternatively, you can run the test_pagination.py file directly:

   ```bash
   python test_pagination.py
   ```

<hr>

This README.md provides a detailed explanation of the project, its usage, and the testing process, making it easier for other developers to understand and use the code.