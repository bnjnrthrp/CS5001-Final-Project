"""
Final Project: Library of CSV functions

Course: CS 5001
Student: Benjamin Northrop

Various helper functions to process more generic CSV files
These functions will check for and remove cells with invalid characters,
remove blank rows, and remove lines that have specific words chosen by the user.
Most of these functions are used within a runner called clean_data, which will clean the data
for further processing.

CSV files can be of any format regarding number of columns and rows.
"""
import string
from typing import List

CHARACTERS = string.ascii_letters + string.digits + ' ' + string.punctuation


def check_valid_characters(words: str) -> bool:
    """
    Checks the word to ensure it contains only valid alphanumeric characters
    and punctuation symbols, returns True if all characters valid.

    Args:
        words (str): the word(s) to be checked

    Examples:
        >>> check_valid_characters('test123!@#')
        True
        >>> check_valid_characters('TRAINING HOURS')
        True
        >>> check_valid_characters('ï»¿')
        False
        >>> check_valid_characters('TRAINING HOURSï»¿')
        False


    Returns:
        bool: True if all characters are alphanumeric or punctuation symbols.
    """
    for letter in words:
        if letter not in CHARACTERS:
            return False
    return True


def clean_row(row: list) -> list:
    """Take a row of CSV, cleans the data, and returns a list

    Args:
        row (list): each item in the string corresponds to a column in the table

    Examples:
        >>> clean_row(['DAY_1', '', ''])
        ['DAY_1', '', '']
        >>> clean_row(['ï»¿', '1', '2'])
        ['', '1', '2']

    Returns:
        list: the cleaned row
    """
    rtn = []
    for val in row:
        if check_valid_characters(val):
            rtn.append(val)
        else:
            rtn.append('')
    return rtn


def check_blank_row(row: tuple) -> bool:
    """Checks if the list contains only blank values. Returns a bool.
    Strips white space from input rows.

    Args:
        row (list): list of strings, each index corresponds to a column in the table

    Examples:
        >>> check_blank_row(['DAY 1', '', ''])
        False
        >>> check_blank_row(['', '', ''])
        True
        >>> check_blank_row([' ', '-', ''])
        False

    Returns:
        bool: True, if all items are blank
    """
    # For loop into each part of the line split
    for val in row:
        # if not empty, return False
        if str(val).strip() != "":
            return False
    # if it makes it through, return True
    return True


def remove_blank_lines(rows: tuple) -> tuple:
    """Takes an list of rows, removes the blank rows, and returns the cleaned list

    Args:
        rows (list): The csv file, in the format of a 2 dimensional list, where each line
        is the first dimension of list

    Examples:
        >>> remove_blank_lines((['abc', '', ''], ['', '', ' '], ['', 'test', 'line 3']))
        (['abc', '', ''], ['', 'test', 'line 3'])
        >>> remove_blank_lines((['abc', 1, ''], ['', 2, ''], [3, 'test', 'line 3']))
        (['abc', 1, ''], ['', 2, ''], [3, 'test', 'line 3'])
        >>> remove_blank_lines([['', '', ''], ['', '', ''], ['', '', '']])
        ()

    Returns:
        list: The cleaned file, a 2 dimensional list
    """
    rtn = []
    for row in rows:
        if not check_blank_row(row):
            rtn.append(row)
    return tuple(rtn)


def clean_data(data: tuple) -> tuple:
    """
    Takes a csv file, removes invalid characters, blank lines, consolidates duplicate
    events, and returns a cleaned version of the file

    Args:
        file (tuple): the raw csv data from read file

    Returns:
        tuple: the cleaned up csv file
    """
    rtn = []
    for row in data:
        cleaned_rows = clean_row(row)
        rtn.append(cleaned_rows)
        cleaned_data = remove_blank_lines(rtn)
    return tuple(cleaned_data)


def remove_line(lines: tuple, phrase: List[str]) -> tuple:
    """Takes a list of lines representing the spreadsheet (a 2D list),
    searches for the phrase of interest, and returns all the lines 
    that do not contain the phrase. Phrase of interest is a list of strings to allow for multiple
    phrases of interest in one iteration. 
    Will remove the entire line if any of the phrases are found.
    Ignores case, does not ignore punctuation, and will match even partial matches.

    Examples:
        >>> lst = [['DAY 1', '', ''], ['CAI', 'P1.060', '0.5'], ['TRAINING HOURS', '', '7']]
        >>> remove_line(lst, ['training hours'])
        (['DAY 1', '', ''], ['CAI', 'P1.060', '0.5'])

        >>> lst = [['DAY 1', '', ''], ['CAI', 'P1.060', '0.5'], ['TRAINING HOURS', '', '7']]
        >>> remove_line(lst, ['day 1'])
        (['CAI', 'P1.060', '0.5'], ['TRAINING HOURS', '', '7'])

        >>> lst = [['DAY 1', '', ''], ['CAI', 'P1.060', '0.5'], ['TRAINING HOURS', '', '7']]
        >>> remove_line(lst, ['day 1', 'ca'])
        (['TRAINING HOURS', '', '7'],)

    Args:   
        lines (list): The list that represents the csv table to go through
        phrase (str): The phrase of interest that we want to remove

    Returns:
        list: The cleaned list with the rows containing the word of interest removed.
    """
    cleaned_list = []
    # Searches line by line, and then goes into each individual item in the list
    for line in lines:
        # For each line, search for the phrase.
        keyword_not_found = True
        for item in line:
            for keyword in phrase:
                if keyword.casefold() in item.casefold():
                    keyword_not_found = False
        if keyword_not_found:
            cleaned_list.append(line)

    return tuple(cleaned_list)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
