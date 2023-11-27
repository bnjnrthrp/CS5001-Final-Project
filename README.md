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
Highlight some key features of this project that you want to show off/talk about/focus on. 

(All examples will have the actual data in the Examples folder under the names 'tutorial_x.csv', ASCII printouts have been provided for a general picture, but if formatting is an issue please refer to the tutorial files).

The program will take the CSV file input, clean the sheet to pull out the raw data while ignoring some of the calculations that are included inside (such as the sum of training hours per day). The normal Excel "block" that would constitute a day will have a merged header, which specifies the day of activities. The next row has the headings for the columns, specifying the type, event code, and hours to complete. The number of rows in each block is typically 6 rows, but that is not guaranteed. At the bottom, they have summed the hours column. 
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
How do we run your project? What should we do to see it in action? - Note this isn't installing, this is actual use of the project.. If it is a website, you can point towards the gui, use screenshots, etc talking about features. 

The project is run through the command terminal. The standard method is for the input CSV file to be in the same folder as this python program, and the output will be written in the same folder.

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

returns
```


## Installation Instructions
If we wanted to run this project locally, what would we need to do?  If we need to get API key's include that information, and also command line startup commands to execute the project. If you have a lot of dependencies, you can also include a requirements.txt file, but make sure to include that we need to run `pip install -r requirements.txt` or something similar.

To run the files locally, you'll need to download all the library files that are used in conjunction with doc_daily_planner.py. The files needed are:
- doc_daily_planner.py
- csv_lib.py
- syllabus_lib.py
- file_view.py
  
There are no dependencies required for the project, however it does import the following libraries automatically:
- sys
- string
- typing
- csv


## Code Review
Go over key aspects of code in this section. Both link to the file, include snippets in this report (make sure to use the [coding blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code)).  Grading wise, we are looking for that you understand your code and what you did. 

### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off. 


## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

There are some features to be added later, if desired, to make the program more robust. One major hurdle that currently is solved with pre-processing is taking the published input data from a "monthly calendar" structure into a single major column that this program processes. The main structure is a width of 15 columns, where each group of 3 columns is a single day's worth of events. These columns of 15 then go down the rows in groups of 5 to show a generic "work-week" shape structure. Currently, iterating to the right side of the CSV file creates additional complexity that is not supported, and the users must first manually change the file into a single column of a group of 3.

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.