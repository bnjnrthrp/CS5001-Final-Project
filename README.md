# Final Project Report

* Student Name: Benjamin Northrop
* Github Username: bnjnrthrp
* Semester: Fall 2023
* Course: CS5001



## Description 
My company trains professional aviators. Our course is approximately 180 days long, with each day being a module of some combination of flights in a helicopter, training scenarios in a simulator, or instruction in a classroom. The classroom instruction can also be broken down into two categories - self-taught and instructor-led.

The primary scheduling tool is a home-built Excel file that we call the "Barnyard", named after the call-sign of its creator. However, every couple years, the syllabus changes slightly as our curriculum managers add, change, or remove portions of the course. Incorporating these updates is labor-intensive and prone to mistakes.

This tool is designed to be a stepping stone to allow for automatic incorporation of a new syllabus into the Barnyard tracker based off of a source document that is provided in a standard format.
This program will allow non-Excel savvy schedule writers to quickly and reliably incorporate syllabus changes.

Overall, we expect this tool to reduce the labor-requirement to build a new schedule by 90%, as it removes the necessity for someone to go line-by-line and manually verify or edit modules of events.

## Key Features
(All examples will have the actual data in the test_files folder under the names 'example_input_x.csv', ASCII printouts have been provided for a general picture, but if formatting is an issue please refer to the tutorial files).

The program will take the CSV file input, clean the sheet to pull out the raw data while ignoring some of the calculations that are included inside (such as the sum of training hours per day). The normal Excel "block" that would constitute a day will have a merged header, which specifies the day of activities. The next row has the headings for the columns, specifying the type, event code, and hours to complete. The number of rows in each block is typically 6 rows, but that is not guaranteed. At the bottom, they have summed the hours column. (For actual example, see example_input_2.csv)
|                 DAY 2          | 
| TYPE           | EVENT   | HRS |
| CAI            | P1.080  | 2.0 |
| CAI            | P1.090  | 1.0 |
| CAI            | P1.100  | 1.0 |
| ICW            | P2.110  | 0.5 |
|                |         |     |
|                |         |     |
| TRAINING HOURS |         | 4.5 |


Additionally, some events are grouped together in a range rather than listed individually, and that appears as a 2 row entry with the first row showing the type and first event, with no hours, the second row leave the type blank, the final event, and the total hours for the group. The identifier for this "runon" case is a hyphen in the first line. 

|                 DAY 1          | 
| TYPE           | EVENT   | HRS |
|----------------|---------|-----|
| CAI            | P1.060  | 0.5 |
| ICW            | P2.010- |     |
|                | P2.070  | 6.5 |
|                |         |     |
|                |         |     |
|                |         |     |
|                |         |     |
| TRAINING HOURS |         | 7.0 |

The first step in the processing will normalize the raw data - it first determines which day of events it is working with and maps it to each associated event. Then it searches for any runon events and combines those lines to create a single line with all the data. Finally, it removes any blank lines and the summation lines, leaving us with a single standard document to work with for the data transformation. Using the above 2 days as an example, the intermediate step result looks like this:

| DAY | TYPE   | EVENT         | HRS |
|-----|--------|---------------|-----|
| 1   | CAI    | P1.060        | 0.5 |
| 1   | ICW    | P2.010-P2.070 | 6.5 |
| 2   | CAI    | P1.080        | 2   |
| 2   | CAI    | P1.090        | 1   |
| 2   | CAI    | P1.100        | 1   |
| 2   | ICW    | P2.110        | 0.5 |
| 2   | ICW    | P2.120        | 1   |
| 2   | JMPS 1 | P2.160        | 2   |

The final transformation is merging all of the same-day events into a matrix that combines like-type events and same-day events into a single cell or line, respectively. The use of dictionaries and lists helps to consolidate all this data into a final output that looks like (may need to expand the screen for formatting.): 

| DAY | ICW                | PTT | CAI                        | IGR | LAB    | MISC    | HRS | LOCATION | FLT | SIM |
|-----|--------------------|-----|----------------------------|-----|--------|------   |-----|----------|-----|-----|
| 1   | ICW P2.010-P2.070  |     | CAI P1.060                 |     |        |         | 7   |          |     |     |
| 2   | ICW P2.110, P2.120 |     | CAI P1.080, P1.090         |     | JMPS 1 |         | 7.5 |          |     |     |


This matrix is vital for the Barnyard to function, as it has another built-in tool that uses this matrix for creating schedules. 

## Guide
The project is run through the command terminal. The standard method is for the input CSV file to be in the same folder as this python program, and the output will be written in the same folder. You may change the source and destination folders using relative path from the command prompt's current folder.

Run the file by calling the main file doc_daily_planner.py, a '-f' flag followed by the input file name. There is an optional '-o' output flag so that you may specify the output file name. The default output file name is 'syllabus.csv'.

You may also call a help menu with the flag '-h' or '--help' which will bring up the help menu with descriptions of each argument. Examples:

Creating a file with custom output name
```
python doc_daily_planner.py -f input_file.csv -o output_results.csv
```

Creating a file with default output name
```
python doc_daily_planner.py -f input_file.csv
```

Asking for help menu
```
python doc_daily_planner.py -h
```


## Installation Instructions
To run the files locally, you'll need to download the following 4 files that are used to run the program:
- doc_daily_planner.py
- csv_lib.py
- syllabus_lib.py
- file_view.py
  
There are no external dependencies required for the project, however it will import the following built-in libraries as part of the program:
- sys
- string
- typing
- csv


## Code Review
The first step gets the file input and desired output file names, attempts the open the file and read the lines. From there, we have a lot of cleaning and adjusting of the data to put it in our desired shape.

The first step is cleaning the CSV data and formatting, which uses the functions in csv_lib.py. clean_data() is basically a runner for several helper functions:
``` python
def clean_data(data: tuple) -> tuple:
    rtn = []
    for row in data:
        cleaned_rows = clean_row(row)
        rtn.append(cleaned_rows)
        cleaned_data = remove_blank_lines(rtn)
    return tuple(cleaned_data)
```
clean_rows() searches for invalid characters. This could be anything non-alphanumeric or symbolic that you'd expect in an english document.
If a row contains invalid characters, it removes the content of the invalid cells but lets the others remain. The return from this phase then gets sent to a temporary list, which then has any blank rows removed. The final return is considered the "cleaned" data in the sense that all the characters are valid and all of the empty rows are removed.

Next, we have to do a more refined filter to remove some of the processed data embedded in the original file. Examples were: each day "block" has its own individual header row, as well as a row at the bottom summing the total number of hours spent on a single day. These were superfluous and needed to be deleted. We can control what phrases get removed by editing the ROWS_TO_DELETE constant, so we can avoid editing the code directly.

``` python
def remove_line(lines: tuple, phrase: List[str]) -> tuple:
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
```

The final output of this cleaned data is the completion of the csv modifications, as it was pretty generic data cleaning and could be used in other applications. There is no specific shape requirement for the size of the file up to this point, but now we are going into our program-specific structure and using the syllabus_lib file for final processing.

At this point, each block of "days" has a title cell announcing "Day Z" where Z is the day number. It's the only cell in that row. The following cells are all event types and codes that are on that specific day. We know we've reached the end of the day's events when we reach the "Day Z+1" header on the next line.

Our next step is to normalize the data so that instead of linking each line of events to a separate line that specifies the day, we distribute the day to each line of events, so we grow from 3 columns to 4, and make "Day" the 1st column. 

The second step of this normalization is to consolidate the events that show an overrun in the cells with the consolidate_events() function.

Here's the example from above that shows the run-on between two lines
| 1   | ICW            | P2.010- |     |
| 1   |                | P2.070  | 6.5 |

This uses two helper functions, check_runon() and combine_events() to go line by line and see if there's a runon indicator (defaulted to the delimiter '-'), and then combine any 2 events into a single event line. This normalized syllabus is now ready for the final transformation: compressing the entire syllabus so that each line is just 1 day of events.

The consolidate_days() function initializes a blank dictionary for each new day via a day counter. When the program reaches a line with a day that doesn't match the day counter, the program knows it's reached a new day. Abbreviating the code that provides the context, the day counter method works specifically here:

``` python
day_counter = 0
if day_counter != current_line[0]:
    day_counter = current_line[0]
    day_dict = initialize_syllabus_dict(EVENT_TYPES)
```
The way we associate all of these into the same day is that each line becomes a dictionary with the key "Day" having the value of its associated day. Then, the remaining categories each become keys and the values are initialized as individual lists. The primary categories we could have are:
['DAY', 'ICW', 'PTT', 'CAI', 'IGR', 'LAB', 'MISC', 'HRS', 'LOCATION', 'FLT', 'SIM']

initialize_syllabus_dict(EVENT_TYPES) returns:
{'DAY': [],
'ICW': [],
'PTT': [], 
'CAI': [], 
'IGR': []
.
.
.} (you get the idea)


We then go line by line and append the event codes onto the respective list to avoid overwriting anything when we come across two of the same event types within a single day. 
These can be modified at the top with the EVENT_TYPES constant.

Some of these don't have any use yet, such as "LOCATION." The current data provided doesn't specify locations for where to do events, but the final Excel tool that will use this data may use this field, so it is left in there.


After it finishes consolidating a line, it preemptively checks the following line to see if a new day is coming or not. This solves the issue of moving on to a new day before outputting the now built day's worth of events in a line.
``` python
next_line = syllabus[index + 1]
    if current_line[0] != next_line[0]:
        rtn.append(day_dict)
    index += 1
```

Finally, once that is all complete, we write to the new file and use the csv library to assist us in writing each line from the dictionaries.

The final output may look a little strange, since all cells that were empty essentially has brackets and quotes. This is ok, because at this point we are ready to import into Excel and some quick find/replace options would quickly remove these characters.


### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off. 

One of the major changes was keeping track of the data's current state as it went from cleaning function to cleaning function. Each time data is manipulated is an opportunity for data to be lost or corrupted, so ensuring that the data values remained as unaffected as possible was a challenge. 

I mitigated this by breaking the different tasks into multiple miniature programs, so the csv lib has a "main" runner (clean_data) and syllabus_lib has normalize_syllabus. These could have been called individually by main, but for the sake of abstraction I wanted to break them apart because it provided good checkpoints for the data as it was returned from those function runners.

Additionally, I used different variable assignments for each stage of the data cleaning/transformation process. This was for readability and to make debugging easier, as you could more intuitively insert debug print statements.

The other major challenge was consolidating each day together, and ensuring each category got to the right key in the dictionary. The issue was that the desired data could be in one of two columns: The Event_Code was only used for specific classes in the ICW, CAI, and IGR categories, because it specified the class code to be used. However, for all other events (flights, simulators, PTT, etc), the event code does not get used in practice, but instead the event_type contains the "title" such as FAM 1, OFT 3, etc. As a result, I broke up these different categories as we went through an if/else decision tree: 

``` python 
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


day_dict[title].append(event_code)
```

In essence, it goes through a flow chart like below (this one has been abbreviated)
``` mermaid
flowchart TD
    A[normalized_syllabus] --> B(consolidate_days)
    B --> C{Determine category}
    C --> D{SIM_EVENTS i.e. OFT, TOFT}
    D --> |Not SIM|E{FLT_EVENTS i.e. FAM, SAR, DIP}
    E --> |Not FLT|F{CLASSROOM i.e. IGR, CAI}
    D -->|Yes\nevent_code = title, title = 'FLT'| G(add to day_dict)
    E -->|Yes\nevent_code = title, title = 'SIM'| G(add to day_dict)
    F -->|Yes\ntitle is first 3 of CLASSROOM| G(add to day_dict)
    G -->H[return day_dict]
```

Each of these days is built using a list of dictionaries. Unfortunately, due to work timelines wanting this project to be completed sooner rather than later, I began this project prior to our class on Classes and Object Oriented Programming. I considered creating a Class Class so each syllabus day was an instance of it, but I wasn't as confident in how I would write these objects into the file, whereas the documentation for csv had built in support for writing dictionary files. Down the road, the intent is to refactor the code to create a class and use it as a means to explore OOP.

The final challenge was catching all of the valid variations in how a syllabus code is managed from the root file to the final product. While every event has a unique event code, only classroom events (ICW, CAI, IGR) actually use the event code. The remaining ones have a unique "type" event (JMPS 1, JMPS 2, etc). An additional variation was the root code had cases of requiring multiple lines for one class due to a long type name (OFT NATOPS X), or missing the delimiter required to signify a runon event. We added support to detect and retroactively correct the additional line and combine it appropriately while avoding duplication.


## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc).

To see example runs and test results, check the test_files folder. example_input_1.csv shows a generic input that is contains standard inputs of classes, with examples of a run-on situation and some of the extraneous data (such as training hours).

example_input_2.csv is a more strenuous test, and it contains every type of event in the syllabus. This is the full syllabus for one type of student.

example 3 is the full 180-day syllabus and is the final product of the actual data to be entered. This file is the base syllabus and all other flavors of syllabus are derivative of this one.

## Testing
During each step of the transformation, I used docstring testing to build unit tests prior to iterating the function. Edge cases were focused on odd characters and typos that I would expect to find in the final product that is provided.
Functional testing was broken into two major checkpoints - the intermediate step to ensure the csv_lib was working correctly. 
The file test_data_cleaning.csv shows the output prior to being sent to the consolidate_syllabus() function and was the final check to ensure all of the data from the original file was being processed correctly into an acceptable file for the final function run.

Then the final product to verify that the syllabus_lib was processing the csv_lib output correctly. This was the final consolidation of the days and events and would be checked against the expected result. We tested this by comparing it to a smaller sample, approximately 30 days worth of data (example 1), testing it on 70 days of schedule (example 2), and then the final full product (example 3).

## Missing Features / What's Next
There are some features to be added later, if desired, to make the program more robust. One major hurdle that currently is solved with pre-processing is taking the published input data from a "monthly calendar" structure into a single major column that this program processes. The main structure is a width of 15 columns, where each group of 3 columns is a single day's worth of events. These columns of 15 then go down the rows in groups of 5 to show a generic "work-week" shape structure. Currently, iterating to the right side of the CSV file creates additional complexity that is not supported, and the users must first manually change the file into a single column of a group of 3. 

In syllabus_lib, the function check_runon() supports a specified delimiter to determine the flag for a range of events. It's defaulted to '-' (such as P1.080-P1.120), but could be used in other programs with a different indicator (Example range 1:10). In this iteration of the program, one challenge is carrying the specified delimiter deep enough into the program so that it reaches the check_runon() function. In this design, it is there as a helper function and gets called by consolidate_events(), which in turn gets called by normalize_syllabus(). Having this delimiter argument added to each of the next functions only to be used as an argument to the next seems like an added complexity to the more shallow functions reducing the complexity. In the current scope of the program, this delimiter feature is not required, since the provided CSV will always use '-' as it's delimiter. It remains coded in as a feature should another program use this library.

The final consideration is to figure out how to import these programs into Excel 365 so that it can be used organically by Excel. The current challenge for the typical user is working through how to run the program assuming they are not familiar with the command prompt, etc. Having this embedded into an excel file so that we can import the source file, run this program, and then also run the following Excel VBA scripts to finish post-processing would make it a much more sustainable program by reducing input points by the user.

## Final Reflection
This course has been an amazing experience in building robust software and has shown me the path to go from amateur code-writer towards a professional software engineer. My greatest struggle was creating products that could stand the test of time and be flexible enough to handle inputs from left-field without breaking, and the push for standardization, readable code, and outside-the-box thinking has been enlightening. I particularly enjoyed the group meetings and the guided learning that happened in this, as it gave me a chance to take a peek at how other people write code for the same problem. This different perspective often showed me a better or more efficient way to solve a problem and was just as valuable of a learning experience.

I need to stay consistent in breaking down problems into smaller pieces to avoid creating a giant "main", and to continue working with github to align with professional standards. I also hope to continue working with the command prompt as I go deeper into the computer rather than interfacing with the GUI intermediaries. 