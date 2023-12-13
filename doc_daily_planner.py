""" 
Final Project: File "View" For the Application
===========================
Course:   CS 5001
Student:  Benjamin Northrop

This file is the main program that takes a csv input, cleans it, and
writes a matrix-like csv file that is the syllabus for a student
"""
import sys
from file_view import read_csv, write_csv
from csv_lib import clean_data, remove_line
from syllabus_lib import normalize_syllabus, HEADINGS, consolidate_days

ROWS_TO_DELETE = ['CIN', 'training hours', 'type', '**', 'CNATTU', 'WEEK']


def check_args_for_help(args: list) -> bool:
    """
    Checks to see if -h is in the args, if so, prints the help message and returns True.

    Args:
        args (list): A list of command line arguments.

    Returns:
        bool: True if -h is in the args, False otherwise.
    """
    if "-h" in args or "--help" in args:
        print_help()
        return True
    return False


def get_input_file(args: list) -> str:
    """
    Checks to see if -f file_name is in the args, if so, returns the file name,
    or returns an empty string if it is not there.

    On a bad format, such as -f (nothing) or -f followed by a -- or - (another flag),
    raises a ValueError.

    Args:
        args (list): A list of command line arguments.

    Returns:
        str: The file name if it exists in the args and is valid, otherwise an empty string.
    """
    if "-f" in args:
        index = args.index("-f")
        if len(args) > index + 1 and not args[index + 1].startswith("-"):
            return args[index + 1]
        else:
            raise ValueError("Missing filename after -f")
    return ""


def get_output_file(args: list) -> str:
    """
    Checks to see if a -o file_name is in the args, if so returns the file name or
    the empty string if it is not there.

    If -o is provided without a following file name, it uses the default 'syllabus.csv'.

    Args:
        args (list): A list of command line arguments.

    Returns:
        str: A file name if -o is in the args, otherwise an empty string.
    """
    if "-o" in args:
        index = args.index("-o")
        if len(args) > index + 1 and not args[index + 1].startswith("-"):
            return args[index + 1]
    return "syllabus.csv"


def print_help() -> None:
    """
    Prints the help message for the program.
    """
    print(
        "Usage: python doc_stats.py [-h|--help] [-f filename]  [-o filename]")
    print("Options:")
    print("  -f filename: The name of the syllabus to modify.")
    print("  -h or --help: Print this help message and exit")
    print("  -r or --runon: (CURRENTLY UNAVAILABLE) the symbol that delineates what the runon character is (default '-')")
    print("  -o filename: The name of the file to write the output to.",
          "If filename is not provided, but -o is used then the default file",
          "name is syllabus.csv.")


def main(args) -> None:
    """
    Main driver of the program
    """
    # Check for help first
    if check_args_for_help(args):
        return

    # Try to get the file name
    try:
        file = get_input_file(args)
    except ValueError as e:
        print(e)
        print_help()
        return

    # Determine if there's an output file, otherwise set it to default
    output = get_output_file(args)
    # try to open and read file, get the data

    try:
        data = read_csv(file)
    except FileNotFoundError:
        print(f"{file} not found!")
    except IOError as io:
        print(io)

    # Does an initial basic cleaning of the data - remove blank lines, lines with invalid inputs
    cleaned_data_basic = clean_data(data)

    # Remove superfluous rows (training hours and "TYPE, EVENT, HRS" rows)
    cleaned_data_advanced = remove_line(cleaned_data_basic, ROWS_TO_DELETE)

    # Normalizes syllabus lines so each event is tagged with its corresponding day to allow consolidation
    normalized_syllabus = normalize_syllabus(cleaned_data_advanced)

    # Combines days into the final product, ready to print
    consolidated_syllabus = consolidate_days(normalized_syllabus)
    write_csv(output, consolidated_syllabus)
    return


# Need to add action option so we can either build csv or build the syllabus

if __name__ == "__main__":
    main(sys.argv)
