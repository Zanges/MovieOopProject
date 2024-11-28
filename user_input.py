""" helper functions for getting user input with validation """
from datetime import datetime


def get_valid_release_year() -> int:
    """ Get a valid release year """
    valid_input = False
    while not valid_input:
        try:
            release_year = datetime.strptime(input("Enter release year (YYYY): "), "%Y")
        except ValueError:
            print("Invalid date format")
            continue
        if release_year.year < 1900:
            print("Release year must be after 1900")
            continue
        if release_year.year > datetime.now().year:
            print("Release year cannot be in the future")
            continue
        valid_input = True
    return release_year.year


def get_valid_rating() -> float:
    """ Get a valid rating """
    valid_input = False
    while not valid_input:
        user_input = input("Enter rating (0.0-10.0): ")
        try:
            rating = float(user_input)
        except ValueError:
            print("Rating must be a number between 0.0 and 10.0")
            continue
        if not 0.0 <= rating <= 10.0:
            print("Rating must be between 0.0 and 10.0")
            continue
        valid_input = True
    return rating


def get_valid_asc_desc() -> bool:
    """ Get valid input for ascending/descending """
    valid_input = False
    while not valid_input:
        reverse_input = input("Sort in descending order? ([A]scending/[D]escending)<Enter for ascending>: ")
        if reverse_input.lower() in {"a", "asc", "ascending", ""}:
            return True
        if reverse_input.lower() in {"d", "desc", "descending"}:
            return False
        print("Invalid input")
    return False # should never reach this point, but default to descending


def get_valid_start_end_year(arg: str) -> int:
    """ Get valid input for start and end year """
    valid_input = False
    while not valid_input:
        user_input = input(f"Enter {arg} (leave blank for no {arg}): ")
        if not user_input:
            if arg == "start":
                year = 1900
            else:
                year = datetime.now().year
            valid_input = True
        try:
            year = int(user_input)
        except ValueError:
            print("Year must be a number")
            continue
        if year < 1900 or year > datetime.now().year:
            print("Year must be between 1900 and the current year")
            continue
        valid_input = True
    return year


VALIDATORS = {
    "Release Date": get_valid_release_year,
    "Rating": get_valid_rating,
    "Min Rating": get_valid_rating,
    "New Rating": get_valid_rating,
    "Ascending/Descending": get_valid_asc_desc,
    "Start Year": lambda: get_valid_start_end_year("start"),
    "End Year": lambda: get_valid_start_end_year("end"),
}


def get_valid_arguments(arg_names: list[str]) -> list:
    """ Get valid arguments for a command """
    args = []
    for arg in arg_names:
        if arg in VALIDATORS:
            args.append(VALIDATORS[arg]())
        else:
            user_input = input(f"Enter {arg}: ")
            if not user_input:
                print(f"{arg} cannot be empty")
                continue
            args.append(user_input)
    return args
