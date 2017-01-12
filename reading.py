# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.


# Write the read_table and read_database functions below
def read_table(file):
    '''(str) -> Table
    Generates a table object by reading a given the name of a .csv file 
    '''
    # create a new table object
    table = Table()
    # open and read the csv file
    filehandle = open (file, 'r')
    all_lines = filehandle.readlines()
    filehandle.close
    # first line in the file contains the names of columns, clean the line and
    # put the names into a list
    column_names = all_lines[0].strip('\n').split(',')
    # obtain how many columns are there and remove the first line of the line
    # read in so it only leaves data that is to be stored inside those columns
    column_length = len(column_names)
    all_lines.remove(all_lines[0])
    # Loop through all columns and create a new column for each column
    for column in range (0, column_length):
        table.add_column(column_names[column])
        # Add row content one by one to the current column
        for line in all_lines:
            # Avoid empty lines to be added to the column
            if(not(line.strip() == '')):
                # Split each line into a list and add the value at element of
                # list matching to that of the column
                row_content = line.strip('\n').split(',')
                table.add_content(column_names[column], row_content[column])
    return table
    
def read_database():
    '''() -> Database
    Reads in a formatted .csv text file and uses the data to generate a database
    object
    '''
    database = Database()
    file_list = glob.glob('*.csv')
    for file in file_list:
        # Create a table for each file given
        table = read_table(file)
        # Add table to database
        key = file.replace('.csv', '')
        database.add_table(key, table)
    return database
