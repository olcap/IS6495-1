# Simple sample hotel reservation system (group project assignment)

### This is a group project done by Pete Helgren and Tristan Olcott at the University of Utah.

**Integrity Statement:** This entire project was done without any generative AI.  This has not been copied from any website or repository.  This is all original work done by Tristan and Pete with the use of in-class code alongs, sample code and external resources used only to check for syntax errors or runtime errors.  The structure and ideas reflected in the code are the result of thinking critically about what a hotel reservation system should do.  It is by no means exhaustive in scope.  It meets the basic requirements spelled out in the rubric, plus some ideas of our own.

We started with a basic design of three tables with CRUD capabilities as well as the ability to export and import the data in csv format.  The assignment was: **Hotel Reservation System** - Create a reservation system which books hotel rooms. It charges various rates for particular types of the hotel. Hotel rooms have penthouse suites which cost more. Keep track of when rooms will be available and can be scheduled.

The three tables were:

1.  Rooms -  Identified by ID, it contained a room description, a room type and a room rate
2.  Room Inventory -  Each of the defined rooms were assigned to a floor using the ID as a foreign key and had a flag to indicate if the room was available or not.  The availability flag is used to ndicate that a particular room was out of commission (trashed by a wild party, had a maintenance issue, etc)
3.  Bookings  - This table recorded the date range that the book in inventory was booked for.

We then broke our code into four separate files to ease the maintenance:

- Hotel API's (hotel_apis.py) - These API's are essentially wrappers over the CRUD routines.  Rather than clutter the table classes with additional code, the api's encapsulate distinct functions that can be used by the UI to display table data and format data before being processed by the CRUD functions.
- Hotel UI (hotel_ui.py) - The hotel UI code separates the menu function calls from the menu code itself primarily to ease the maintenance of the code base.  The functions within the UI then call the wrapper api's to do the heavy lifting.  The hotel UI provides all the prompts for data input and selection.
- Hotel menu (hotel_menu.py) - The menu keeps the UI selection simple.  It consists of functions that list options for maintaining the hotel inventory.  Each menu option then calls a function in the Hotel UI module which, in turn, calls a wrapper api function.
- Export/Import (export_import.py) - The classes and methods allow for a basic backup and recovery feature.  You can also use the import functions to load an initial sample database from the accompanying .csv files

Breaking up the code in this way keeps the code in each module to a minimum while grouping like module functions together.

The table classes basically stand on their own without much need for explanation.  However, a bit more detail on each module will help clarify our approach:

## Hotel API's

Probably the most complex of the modules, it has most of the SQL code that wraps the CRUD routines in the table classes.   In most cases the complexity is around selecting available room types so we'll review that logic here:

We used a CTE to select the currently booked rooms for the date range entered.  Then the CTE was joined with the room inventory table using a left join so that rooms that were available would have NULL values that could be selected.  This made the SQL statements easier to understand and easily reusable.

Calls to the CRUD routines in the tables occur here.  These API's wrap the CRUD methods in the table classes.

## Hotel UI

The hotel UI module contains the functions and logic for the gathering of inputs.  We separated the UI from the menu just to keep things cleaner and easier to maintain.  If you look at the contents of hotel_ui.py, you will see most of the user I/O occurs there, with very few exceptions.  Edits and validation of data should be kept in this module to keep the validation code to a minimum in API module.

## Hotel Menu

The hotel_menu.py contains probably the simplest logic in the application.  It is essentially used to prompt for options and then call the UI methods.  We tried to maintain consistent conventions to make it easy and obvious to use.

## Export/Import

This module contains a set of classes that import and export data to and from the csv files to the database tables.  It can initially be used to load the data.  If you are starting with a "clean" install, run each of the "reset" options on the utility menu to create the database and tables in SQLite

That is about it!  The only requirements are to use the latest version of Python and install the SQLite database browser so you can view the tables to help troubleshoot issues.
