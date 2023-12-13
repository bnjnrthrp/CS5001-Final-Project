"""
Final Project: Library of syllabus manipulation files

Course: CS 5001
Student: Benjamin Northrop

This library of functions will allow the user to process CSV files as they pertain to
a flight training syllabus. There are several helper functions, and the majority are for manipulating CSV data
to prepare it for the consolidate days function.

The various headings, event types, and flight events match those provided by the file and this formatting is required
for proper handling.


"""
from typing import Tuple

HEADINGS = ['DAY', 'TYPE', 'EVENT', 'HRS']
EVENT_TYPES = ['DAY', 'ICW', 'PTT', 'CAI', 'IGR',
               'LAB', 'MISC', 'HRS', 'LOCATION', 'FLT', 'SIM']
FLIGHT_EVENTS = ['FAM', 'SAR', 'DIP', 'NAT', 'INS', 'TAC']
SIM_EVENTS = ['OFT', 'WTT', 'CST']
CLASS_TYPES = ['ICW', 'CAI', 'IGR']
LAB_TYPES = ['JMPS', 'NATS', 'IMAT', 'SAC']
PTT_EVENT = ['PTT', 'DTTT']
IGNORE_EVENTS = ['MSN']
# Deceptive ground courses that would otherwise map as a flight
MISNOMER_CLASSES = ['FAM 0', 'FAM A', 'FAM B', 'FAM C', 'SAR CURTAIN']


def distribute_days(syllabus: Tuple[list]) -> tuple:
    """Takes a syllabus as a tuple of lists, finds out what day is associated with
    the following lines of events, then adds a column at the beginning for each 
    of those lines.

    Args:
        syllabus (tuple): The syllabus as a tuple of lists, each list being 
        a line of the csv file.

    Examples:
        >>> distribute_days((['DAY 1', '', ''], ['CAI', 'P1.060', '0.5'], ['ICW', 'P2.010-', '']))
        (['1', 'CAI', 'P1.060', '0.5'], ['1', 'ICW', 'P2.010-', ''])

        >>> example_syllabus = (['DAY 1', '', ''], ['', 'P2.070', '6.5'], ['DAY 2', '', ''], ['CAI', 'P1.080', '2'])
        >>> distribute_days(example_syllabus)
        (['1', '', 'P2.070', '6.5'], ['2', 'CAI', 'P1.080', '2'])

        >>> no_data = ()
        >>> distribute_days(no_data)
        ()

    Returns:
        tuple: The syllabus transformed so that the day heading is
        transposed to be included in the row.
    """
    day = 0
    copy = list(syllabus)
    adjusted_line = []
    adjusted_syllabus = []

    for line in copy:
        # Checks if it's a new syllabus day as it goes down the table
        if "day" in line[0].casefold():
            # Stores the day from the list item "['Day 1', '', '']" -> 1
            day = line[0].split()[1]
        # If not a new day, then adds a new list with stored day, then extends the remaining list items.
        else:
            adjusted_line = [day]
            adjusted_line.extend(line)
            adjusted_syllabus.append(adjusted_line)

    return tuple(adjusted_syllabus)


def consolidate_events(syllabus: tuple) -> tuple:
    """Take a syllabus, find each day that has an event continuing into the line beneath
    it, and combines those into a single line. A runon is defined when the event in a list ends with '-' and
    there's a continuation into the next list in the syllabus. For example, a runon would look like 
    ```
    (['1', 'ICW', 'P2.010-', ''], 
    ['1', '', 'P2.070', '6.5']) 
    ```
    Notice how the P2.010 event extends into the following list. 
    Limitations: This will leave a hanging runon as-is.

    Args:
        syllabus (tuple): The syllabus to be manipulated

    Examples:
        >>> example_syllabus = (['1', 'ICW', 'P2.010-', ''], ['1', '', 'P2.070', '6.5'], ['2', 'CAI', 'P1.080', '2'])
        >>> consolidate_events(example_syllabus)
        (['1', 'ICW', 'P2.010-P2.070', '6.5'], ['2', 'CAI', 'P1.080', '2'])

        # hanging runon will return it as-is. No error, but does not remove the hanging '-'
        >>> example_syllabus = (['1', 'ICW', 'P2.010-', ''],)
        >>> consolidate_events(example_syllabus)
        (['1', 'ICW', 'P2.010-', ''],)

    Returns:
        tuple: The corrected tuple with multi-line events removed.
    """
    rtn = []
    copy = list(syllabus)
    # For each line in the syllabus, checks if it will run-on into the line after it.
    index = 0
    while index < len(copy):
        event = copy[index]
        # If the index is at the very end, just add the final item
        if index == len(copy) - 1:  # -1 is to fix off-by-one index
            rtn.append(event)
            index += 1

        elif check_runon(event):
            # If a runon event is detected, it stores the following event and calls the combine_events function
            next_event = copy[index + 1]
            combined_event = combine_events([event, next_event])
            # Attaches the combined event to the rtn
            rtn.append(combined_event)
            index += 2  # Skips a line in the index, which is the second half of the consolidated event

        elif event[1] == "":
            previous_event = copy[index - 1]
            combined_event = combine_events([previous_event, event])
            rtn.pop()
            rtn.append(combined_event)
            index += 1

        elif event[2] == "":
            previous_event = copy[index - 1]
            combined_event = combine_events([previous_event, event], type=True)
            rtn.pop()
            rtn.append(combined_event)
            index += 1

        else:
            # If not the end of the syllabus and the event doesn't runon to the next line, add it to the rtn list.
            rtn.append(copy[index])
            index += 1

    return tuple(rtn)  # Returns once we reach the end of the syllabus


def check_runon(event: list, delimiter: str = '-') -> bool:
    """Checks if an event continues into the row beneath it.
    Denoted by the last character of the first line as '-'

    Args:
        event_day (list): line of the list to be checked

    Examples:
        # With whitespace
        >>> check_runon([1, 'ICW', 'P2.010- ', ''])
        True

        >>> check_runon([1, 'ICW', 'P2.010', ''])
        False

        # Without Whitespace
        >>> check_runon([1, 'ICW', 'P2.010-', ''])
        True

        # Alternate delimiter
        >>> check_runon([1, 'ICW', 'P2.010:', ''], ':')
        True

    Returns:
        bool: True if the last symbol matches the delimiter, False otherwise
    """
    # Pull the event code and strip off any whitespace on the edges.
    event_code = event[2].strip()

    return event_code.endswith(delimiter)


def combine_events(events: list, delimiter: str = '-', type: bool = False) -> list:
    """Takes 2 lines of events that have a runon code, and returns the combined event. Only combined 2 lines worth of events.
    Will only take the event number and time to complete from the second event. Does not ignore whitespace, punctuation, etc.
    Does not validate that the two events are compatible.

    Args:
        events (list): list of 2 event lines to be combined.
        delimiter (str): defaults to '-', identifies the specific delimiter for the range
        type (bool): when True, combines the 1 index column (type category) rather than the class codes.
            Used for when combining JMPS evends, SHEELD LAB, etc, OFT NATOPS CHECK

    Examples:
        >>> sample_events = [[1, 'ICW', 'P2.010-', ''], [1, '', 'P2.070', '6.5']]
        >>> combine_events(sample_events)
        [1, 'ICW', 'P2.010-P2.070', '6.5']

        >>> sample_events = [[1, 'ICW', 'P2.010-   ', ''], [1, '', '', '6.5']]
        >>> combine_events(sample_events)
        [1, 'ICW', 'P2.010-', '6.5']

        >>> sample_events = [[1, 'ICW', 'P2.010-', ''], [1, '', '', '6.5'], [1, '', 'P2.100', '1.0']]
        >>> combine_events(sample_events)
        Traceback (most recent call last):
        ...
        ValueError: The provided list must contain just 2 events

        >>> sample_events = [[1, 'OFT ', '12.080', '6.0'], [1, 'NATOPS X', '', '']]
        >>> combine_events(sample_events, type=True)
        [1, 'OFT NATOPS X', '12.080', '6.0']

    Returns:
        list: The combined list in one line
    """
    if len(events) != 2:
        raise ValueError("The provided list must contain just 2 events")

    # Allows capture of event-time which may be on the top row for single event over multiple lines, or
    # bottom row if it's a run-on event over multiple lines.
    time = events[0][3]
    if time == "":
        time = events[1][3]

    # Determines which column we want to combine events for. Column 2 (event code) is default, but
    # shifts to column 1 (type) for single events over multiple lines i.e. OFT NATOPS X
    column = 2
    if type:
        column = 1

    copy = events.copy()[0]
    first_string = events[0][column].strip()
    second_string = events[1][column].strip()

    # Catches edge case if a run-on event is missing the delimiter and it was discovered retroactively
    if not first_string.endswith(delimiter) and not type:
        first_string += delimiter

    # Edge case of single event running on to next line, replaces the whitespace that was removed above.
    elif not first_string.endswith(delimiter) and type:
        # Re-add the space back behind the first string
        first_string += " "

    copy[column] = first_string + second_string
    copy[3] = time

    return copy


def standardize_headings(data: Tuple[list]) -> tuple:
    """Validates a syllabus to take non-standard formats and correct it to a standard: Day, Type, Code, Time

    Args:
        data (Tuple[list]): The syllabus data to be processed
        event_types (str): The list of possible event types. Used to differentiate if the column is event codes or types

    Examples:
        >>> events = (['1', 'CAI', 'P1.060', '0.5'], ['1', 'ICW', 'P2.010-P2.070', '6.5'])
        >>> standardize_headings(events)
        (['1', 'CAI', 'P1.060', '0.5'], ['1', 'ICW', 'P2.010-P2.070', '6.5'])

        >>> events = (['1', 'P1.060', 'CAI', '0.5'], ['1', 'P2.010-P2.070', 'ICW', '6.5'])
        >>> standardize_headings(events)
        (['1', 'CAI', 'P1.060', '0.5'], ['1', 'ICW', 'P2.010-P2.070', '6.5'])




    Returns:
        Tuple[list]: The standardized syllabus
    """
    rtn = []
    copy = list(data)
    headings = HEADINGS
    day, event_type, code, hrs = "", "", "", ""
    # Go through each line and find the column that has events
    for item in data[0]:
        try:
            if item.isnumeric():
                day = data[0].index(item)
                continue
        except ValueError:
            continue

        if item in EVENT_TYPES:
            event_type = data[0].index(item)
            if event_type == 2:
                code = 1
            else:
                code = 2

        hrs = 3

    for line in data:
        temp = [line[day], line[event_type], line[code], line[hrs]]
        rtn.append(temp)

    return tuple(rtn)


def normalize_syllabus(data: Tuple[list]) -> Tuple[list]:
    """Runner function that normalizes the syllabus data for final processing using two helper functions. 
    Takes csv data in the form of a tuple, distributes the associated module
    day to each line, and combines run-on lines into single lines. 

    Example:
        >>> sample_csv = (['DAY 1','',''], ['CAI','P1.060','0.5'],['ICW','P2.010-',''],['','P2.070','6.5'])
        >>> normalize_syllabus(sample_csv)
        (['1', 'CAI', 'P1.060', '0.5'], ['1', 'ICW', 'P2.010-P2.070', '6.5'])

    Args:
        file (tuple): The csv data to clean

    Returns:
        tuple: The cleaned syllabus csv file
    """
    # Takes the generic table format and associates each event to its designated module day
    distributed = distribute_days(data)
    standardized = standardize_headings(distributed)
    # Combines runon events into a single line then returns the resulting tuple of lists.
    return consolidate_events(standardized)


def consolidate_days(syllabus: Tuple[list]) -> Tuple[dict]:
    """Compresses the syllabus by converting it from a tuple of lists, with each list being a single event, 
    to a tuple of a list of dictionaries.  Each dictionary is a single day's events, with each key being the 
    type of event and the value a list of all the modules inside it. 

    Args:
        syllabus (Tuple[list]): The syllabus to be consolidated, each list item is a single event. Format ['day', 'type', 'code', 'time']

    Examples: 
        >>> example_syllabus = (['2','ICW','P2.120','1.0'], ['2','JMPS 1','P2.160','2.0'], ['3','ICW','P3.010-P3.100','5.5'], ['3','JMPS 2','P3.110','3.0'])
        >>> consolidate_days(example_syllabus)
        ({'DAY': '2', 'ICW': ['P2.120'], 'PTT': [], 'CAI': [], 'IGR': [], 'LAB': ['JMPS 1'], 'MISC': [], 'HRS': ['1.0', '2.0'], 'LOCATION': [], 'FLT': [], 'SIM': []}, {'DAY': '3', 'ICW': ['P3.010-P3.100'], 'PTT': [], 'CAI': [], 'IGR': [], 'LAB': ['JMPS 2'], 'MISC': [], 'HRS': ['5.5', '3.0'], 'LOCATION': [], 'FLT': [], 'SIM': []})

        >>> example_syllabus = (['19','CAI*','P9.010','0.5'], ['19','ICW','P9.020','0.5'])
        >>> consolidate_days(example_syllabus)
        ({'DAY': '19', 'ICW': ['P9.020'], 'PTT': [], 'CAI': ['P9.010'], 'IGR': [], 'LAB': [], 'MISC': [], 'HRS': ['0.5', '0.5'], 'LOCATION': [], 'FLT': [], 'SIM': []},)

        >>> no_data = ()
        >>> consolidate_days(no_data)
        ()

    Returns:
        Tuple[list]: The consolidated tuple of dictionaries which compresses each event into a single line by its associated schedule day.
    """

    rtn = []
    current_line = []

    index = 0
    day_counter = 0
    # Iterates through the entire document
    while index < len(syllabus):
        try:  # Uses try/exept to handle possible IndexError.
            current_line = syllabus[index]
            title = current_line[1]
            event_code = current_line[2]
            time_required = current_line[3]

            # Check if the day counter matches current event's associated day
            # If false, this indicates we've moved to a new day and need to create a new dictionary
            if day_counter != current_line[0]:
                # Sets the day counter to the day indicated on the event
                day_counter = current_line[0]
            # Initialize the current day's dictionary of events.
                day_dict = initialize_syllabus_dict(EVENT_TYPES)

            day_dict[EVENT_TYPES[0]] = day_counter

            # Maps the different types of events to the correct key in each dictionary.
            # All titles can be identified by their first 3 characters, to standardize the lookups.
            # Will branch individually, set the correct event_code and title variables, then come together at the end.

            if title[:3] in SIM_EVENTS and title not in MISNOMER_CLASSES:
                event_code = title
                title = 'SIM'

            elif title[:3] in FLIGHT_EVENTS and title not in MISNOMER_CLASSES:
                event_code = title
                title = 'FLT'

            elif title[:3] in CLASS_TYPES:
                title = title[:3]

            elif title[:3] in IGNORE_EVENTS:
                event_code = title
                title = 'MISC'

            elif title[:3] in PTT_EVENT:
                event_code = title[4:]
                title = title[:3]
            # Some classes will share a code with the above
            elif title in MISNOMER_CLASSES:
                event_code = title
                title = 'LAB'

            else:  # Catchall for anything that is leftover
                event_code = title
                title = 'LAB'

            # Inputs the final result from decision tree into the dictionary
            day_dict[title].append(event_code)

            # Inputs the time required into the dictionary
            day_dict[EVENT_TYPES[7]].append(time_required)

            # Checks if the next event line is a new day or not.
            next_line = syllabus[index + 1]
            if current_line[0] != next_line[0]:
                # If it's a new day, then we can append the dictionary into the return list before moving on to the next line.
                rtn.append(day_dict)
            index += 1
        # We'll reach an IndexError when we attempt to check the final line against the "next_line".
        # Allows the program to append the final dictionary into the list then exit the loop
        except IndexError:
            rtn.append(day_dict)
            break

    return tuple(rtn)


def correct_event(title: str, event_code: str) -> tuple:
    """Takes an input event, and figures out what the event type is

    Args:
        title (str): The full title of the event
        event_code (str): The event code associated with the event

    Examples:
        >>> title = "AC JUMPS"
        >>> event_code = "A5.550"
        >>> correct_event(title, event_code)
        ('FLT', 'AC JUMPS')

        >>> title = "DIP SIM 3"
        >>> event_code = "A14.400"
        >>> correct_event(title, event_code)
        ('SIM', 'DIP SIM 3')


    Returns:
        tuple: The corrected title and event code for the normalized syllabus
    """
    # checks if an aircrew sim or flight event, and breaks off to new decision tree
    if event_code[0] == "A":
        if title[0:4] == "NATS":
            event_code = title
            title = 'LAB'
        elif title[4:7] == "SIM":
            event_code = title
            title = 'SIM'
        elif title[:2] == "AC":
            event_code = title
            title = 'FLT'

    # Checks through pilot events
    elif title[:3] in SIM_EVENTS and title not in MISNOMER_CLASSES:
        event_code = title
        title = 'SIM'

    elif title[:3] in FLIGHT_EVENTS and title not in MISNOMER_CLASSES:
        event_code = title
        title = 'FLT'

    elif title[:3] in CLASS_TYPES:
        title = title[:3]

    elif title[:3] in IGNORE_EVENTS:
        event_code = title
        title = 'MISC'

    elif title[:3] in PTT_EVENT:
        event_code = title[4:]
        title = title[:3]
    # Some classes will share a code with the above
    elif title in MISNOMER_CLASSES:
        event_code = title
        title = 'LAB'

    else:  # Catchall for anything that is leftover
        event_code = title
        title = 'LAB'

    return (title, event_code)


def initialize_syllabus_dict(headings: list) -> dict:
    """Helper function that creates a syllabus dictionary

    Examples:
        >>> example1 = ['DAY', 'TYPE', 'EVENT']
        >>> initialize_syllabus_dict(example1)
        {'DAY': [], 'TYPE': [], 'EVENT': []}

    Args:
        headings (list): The list the contains all the categories you want to track

    Returns:
        dict: A dictionary that has a key for each heading that would go into a table
    """
    # Initialize a blank dictionary
    rtn = dict()
    # Initializes a blank list for each key that is associated with the headings provided
    for heading in headings:
        rtn[heading] = list()

    return rtn


def check_same_day(event1: list, event2: list) -> bool:
    """Checks if two lines (representing events) occur on the same work day

    Examples: 
    >>> arr1 = ['1', 'CAI', 'P1.060', '0.5']
    >>> arr2 = ['1', 'CAI', 'P2.010', '1.0']
    >>> arr3 = ['2', 'CAI', 'P3.000', '1.0']
    >>> check_same_day(arr1, arr2)
    True
    >>> check_same_day(arr2, arr3)
    False

    Args:
        event1 (list): The current event to compare to
        event2 (list): The next day's event to check

    Returns:
        bool: True if the event occurs on the same day, otherwise False
    """
    return event1[0] == event2[0]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
