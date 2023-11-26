""" 
Final Project: File "View" For the Application
===========================
Course:   CS 5001
Student:  Benjamin Northrop

This file contains functions to help with manipulating CSV files.
"""

import csv
import sys
from syllabus_lib import EVENT_TYPES


def read_csv(file_path: str) -> tuple:
    """
    Reads in a file and returns a tuple with each line as a string.
    Each line will have leading and trailing whitespace removed.
    Empty lines are removed.

    Examples:
    >>> read_csv("")
    ()

Args:
    file_path (str): The path of the file to be read

Returns:
    tuple: A tuple with each line of the file as a string.

    """
    rows = []
    try:
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            table = csv.reader(csvfile, delimiter=',')
            for row in table:
                try:
                    rows.append(row)
                except ValueError:
                    pass
    except FileNotFoundError:
        print(f"{file_path} not found!")
    except IOError as io:
        print(io)
    return tuple(rows)


def write_csv(file_path: str, data: tuple) -> None:
    """Writes a csv in the form of a tuple and writes it to a file.

    Args:
        file_path (str): The destination file location
        file (tuple): The csv file

    Returns:
        None
    """
    with open(file_path, 'w', newline='') as csvfile:
        field_names = EVENT_TYPES
        csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)

        csv_writer.writeheader()
        for row in data:
            csv_writer.writerow(row)
