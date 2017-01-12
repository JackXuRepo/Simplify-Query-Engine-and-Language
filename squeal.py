from reading import *
from database import *

# Below, write:
# *The cartesian_product function
def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    REQ: table1.get_row_length > 0

    Generates the cartesian product of two tables matching each row on the first
    table to every possible row in the second table
    >>> t1 = Table()
    >>> t2 = Table()
    >>> d1 = {'abc':['a', 'b', 'c'], 'xyz':['x', 'y', 'z']}
    >>> d2 = {'two':['1', '2'], 'four':['3', '4']}
    >>> t1.set_dict(d1)
    >>> t2.set_dict(d2)
    >>> ct = cartesian_product(t1, t2)
    >>> ct.get_dict() == {'two': ['1', '2', '1', '2', '1', '2'], 
    'xyz': ['x', 'x', 'y', 'y', 'z', 'z'], 
    'four': ['3', '4', '3', '4', '3', '4'], 
    'abc': ['a', 'a', 'b', 'b', 'c', 'c']}
    True
    '''
    new_table = Table()
    # obtain the names (as lists) of columns in both table1 and table2
    table1_columns = table1.get_column_names()
    table2_columns = table2.get_column_names()
    # obtain their lengths
    table1_row_length = table1.get_row_length()
    table2_row_length = table2.get_row_length()
    # Apply cartesian product to each column in table1
    for column in table1_columns:
        # get current row content for current column
        content = table1.get_content(column)
        # empty list to store row content after the cartesian product applies
        # to this column
        updated_content = []
        # repeats the row value at each column of the table by row length of
        # the second table to match each possible outcome
        for row in content:
            for i in range(0, table2_row_length):
                updated_content.append(row)
        # add table1 columns to the updated table
        new_table.add_entire_column(column, updated_content)
    # Apply cartesian product to table2
    for column in table2_columns:
        content = table2.get_content(column)
        # Repeat content for each column in table2 by the row length of table1
        updated_content = content * table1_row_length
        # add table1 columns to the updated table
        new_table.add_entire_column(column, updated_content)
    return new_table


# *All other functions and helper functions
def process_query(query):
    '''(str) -> list of str
    Adds the clauses for query entered in a list

    >>> process_query("select * from t.title,b.buck where a.animal='Look There!'")
    ['*', 't.title,b.buck', "a.animal='Look There!'"]
    '''
    # Remove the tokens from the query str and replace it with a character that
    # is rarely used such as '~'
    query = query.replace('select ', '')
    query = query.replace(' from ', '~')
    query = query.replace(' where ', '~')
    # Separate each clause into elements in a list using the '~' char as delimeter
    query = query.split('~') 
    return query

def process_from(from_data, database):
    '''(str, Database) -> Table

    >>> t1 = Table()
    >>> t2 = Table()
    >>> d1 = {'abc':['a', 'b', 'c'], 'xyz':['x', 'y', 'z']}
    >>> d2 = {'two':['1', '2'], 'four':['3', '4']}
    >>> t1.set_dict(d1)
    >>> t2.set_dict(d2)
    >>> data = Database()
    >>> data.add_table('t1' , t1)
    >>> data.add_table('t2', t2)
    >>> t = process_from('t1', data)
    >>> t.get_dict() == {'xyz': ['x', 'y', 'z'], 'abc': ['a', 'b', 'c']}
    True
    '''
    # get the table names
    table_names = from_data.split(',')
    # let the table be the first element in list if theres only one table name
    # listed
    combined_table = database.get_table(table_names[0])
    # if there are more than one table name do the cartesian product of all
    # of them two at a time
    if (len(table_names) > 1):
        for table in range(1, len(table_names)):
            next_table = database.get_table(table_names[table])
            combined_table = cartesian_product(combined_table, next_table)
    return combined_table

def process_select(select_data, current_table):
    '''(str, Table) -> Table
    >>> t1 = Table()
    >>> d1 = {'two':['1', '2'], 'four':['3', '4']}
    >>> t1.set_dict(d1)
    >>> t2 = process_select('two', t1)
    >>> t2.get_dict() == {'two': ['1', '2']}
    True
    >>> t3 = process_select('*', t1)
    >>> t3.get_dict() == {'two': ['1', '2'], 'four': ['3', '4']}
    '''
    # create a new table
    updated_table = Table()
    # returns current table if all columns are chosen
    if(select_data == '*'):
        updated_table = current_table
        return updated_table
    else:
        # separate each column name into a list
        selected_columns = select_data.split(',')
        # get a list of the columns in the current list
        all_columns = current_table.get_column_names()
        # add a column and its content to the updated table if the column name
        # matches with the column name of the column selected via the clause
        for column in selected_columns:
            for column_s in all_columns:
                if(column == column_s):
                    updated_table.add_entire_column(column, current_table.get_content(column))
        return updated_table

def process_equality(data, table):
    '''(str, Table) -> Table
    processes the '=' clause from the where constraint
    '''
    row_length = table.get_row_length()
    row = 0
    column1= data[0]
    # check if colum1 is being compared to a value
    if(data[1].endswith("'") and data[1].startswith("'")):
        value = data[1].replace("'", '')
        # For all rows if the values of column and given value do not match 
        # then remove entire row
        while(row < row_length):
            equal_or_not = table.equal_to_value(column1, value, row)
            if(equal_or_not == False):
                table.remove_row(row)
                # once row is removed then row lengths become smaller
                row -= 1
                row_length -= 1
            row += 1
    # runs if column is compared to comlumn
    else:
        column2= data[1]
        while(row < row_length):
            equal_or_not = table.is_equal(column1, column2, row)
            if(equal_or_not == False):
                table.remove_row(row)
                row -= 1
                row_length -= 1
            row += 1
    return table

def process_inequality(data, table):
    '''(str, Table) -> Table
    processes the '>' clause in the where constraint
    '''
    row_length = table.get_row_length()
    row = 0
    column1= data[0]
    if(data[1].endswith("'") and data[1].startswith("'")):
        value = data[1].replace("'", '')
        while(row < row_length):
            greater_or_not = table.greater_than_value(column1, value, row)
            if(greater_or_not == False):
                table.remove_row(row)
                row -= 1
                row_length -= 1
            row += 1
                        
    else:
        column2= data[1]
        while(row < row_length):
            greater_or_not = table.is_greater(column1, column2, row)
            if(greater_or_not == False):
                table.remove_row(row)
                row -= 1
                row_length -= 1
            row += 1
    return table

def contains_operator(string, operator):
    '''(str, str) -> Bool
    Given a str and an substring check if the substring is in the str

    >>> contains_operator('a=b,c+4', '=')
    True
    >>> contains_operator('a=b,c+4', '>')
    False
    '''
    # set initial value that determines whether operator is in str to false
    contains = False
    # compare and check if any character in the str equals the operator if so
    # then return True
    for letter in string:
        if (letter == operator):
            contains = True
    return contains

def process_where(select_data, current_table):
    '''(str, Table) -> Table
    determine which process is made
    '''
    # processes equality if given '='
    if(contains_operator(select_data, '=') == True):
        data = select_data.split('=')
        new_table = process_equality(data, current_table)
    # processes inewuality if given '>'
    elif(contains_operator(select_data, '>') == True):
        data = select_data.split('>')
        new_table = process_inequality(data, current_table)
    return new_table

# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results
def run_query(database, query):
    '''(Database, str) -> NoneType
    Runs the query and prints a table using the conditions stated in the query
    
    >>> t1 = Table()
    >>> t2 = Table()
    >>> d1 = {'abc':['a', 'b', 'c'], 'xyz':['x', 'y', 'z']}
    >>> d2 = {'two':['1', '2'], 'four':['3', '4']}
    >>> t1.set_dict(d1)
    >>> t2.set_dict(d2)
    '''
    # store query clauses in a list
    query = process_query(query)
    # process the from clause that also processes the cartesian table
    combined_table = process_from(query[1], database)
    # If there is a where clase then also process it
    if(len(query) > 2):
        where_clauses = query[2].split(',')
        where_table = combined_table
        # If one or more than one condition is given then run where processes for
        # all of them
        for clause in where_clauses:
            where_table = process_where(clause, where_table)
        combined_table = where_table
    # process the select clause
    selected_columns = process_select(query[0], combined_table)
    # this is the final table
    final_table = selected_columns
    # prints the final table
    print_csv(final_table)


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = table.get_row_length()
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))

if(__name__ == "__main__"):
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    database = read_database()
    run_query(database, query)