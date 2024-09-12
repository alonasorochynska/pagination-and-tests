def validate_input_data(current_page: int, total_pages: int, boundaries: int, around: int) -> None:
    if any(not isinstance(value, int) or value <= 0 for value in [current_page, boundaries, total_pages]):
        raise ValueError("Current page, boundaries and total pages must be positive integers.")

    if not isinstance(around, int) or around < 0:
        raise ValueError("Around must be greater than or equal to zero.")

    if boundaries > total_pages or current_page > total_pages:
        raise ValueError("Current page and boundaries must not be greater than total pages.")

    if current_page - around < 1 and current_page + around > total_pages:
        raise ValueError("The current page with the specified around value exceeds total amount of pages.")


def trim_pages(pages: list[int], total_pages: int) -> list[int]:
    if pages[0] < 1:
        pages = pages[1 - pages[0]:]

    if pages[-1] > total_pages:
        pages = pages[:total_pages - pages[0] + 1]

    return pages


def create_string_values_and_insert_dots(all_pages: list[int]) -> list[str]:
    result_list = []

    for index, page in enumerate(all_pages):
        if index > 0:
            previous_page = all_pages[index - 1]
            if page != previous_page + 1:
                result_list.append("...")
        result_list.append(str(page))

    return result_list


def calculate_range_of_pages(current_page: int, total_pages: int, boundaries: int, around: int) -> None:
    initial_and_next_pages = list(range(1, boundaries + 1))
    current_and_surrounding_pages = list(range(current_page - around, current_page + around + 1))

    if current_and_surrounding_pages[0] < 1 or current_and_surrounding_pages[-1] > total_pages:
        current_and_surrounding_pages = trim_pages(current_and_surrounding_pages, total_pages)

    last_and_previous_pages = list(range(total_pages - boundaries + 1, total_pages + 1))
    all_pages = sorted(set(initial_and_next_pages + current_and_surrounding_pages + last_and_previous_pages))
    all_pages = create_string_values_and_insert_dots(all_pages)

    print(" ".join(all_pages))


def generate_pagination(*pagination_data: int) -> None:
    if len(pagination_data) != 4:
        raise ValueError("Pagination data must have exactly four items.")

    current_page, total_pages, boundaries, around = pagination_data
    validate_input_data(current_page, total_pages, boundaries, around)
    calculate_range_of_pages(current_page, total_pages, boundaries, around)


if __name__ == "__main__":
    generate_pagination(7, 50, 1, 2)
