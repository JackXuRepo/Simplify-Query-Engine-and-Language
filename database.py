class Table():
    '''A class to represent a SQuEaL table'''
    
    def __init__(self):
        '''(Table) -> NoneType
        Initializes values such as the table ditionary, table column names and
        table row length
        '''
        self._table = {}
        self._columns = []
        self._row_length = 0

    def remove_content(self, column, row):
        '''(Table, str, int) -> NoneType
        Removes a single unit of content from a column in a table
        REQ: row > 0 and row < self._row_length
        REQ: (column in self._columns) == True
        '''        
        self._table[column].pop(row)
        self._row_length = len(self._table[column])

    def remove_row(self, row):
        '''(Table, int) -> NoneType
        Removes an entire row from a table
        REQ: row > 0 and row < self._row_length
        '''     
        for column in self._columns:
            self.remove_content(column, row)

    def is_equal(self, column1, column2, row):
        '''(Table, str, str, int) -> bool
        Checks whether two values on the same row in different columns are equal
        REQ: row > 0 and row < self._row_length
        REQ: (column1 in self._columns) == True
        REQ: (column2 in self._columns) == True
        '''
        if(self._table[column1][row] == self._table[column2][row]):
            return True
        else:
            return False

    def equal_to_value(self, column, value, row):
        '''(Table, str, obj, int) -> bool
        Checks whether a value on a row in a columns is equal to a given value
        REQ: row > 0 and row < self._row_length
        REQ: (column in self._columns) == True
        REQ: type(value) == type(column)
        '''        
        if(self._table[column][row] == value):
            return True
        else:
            return False        

    def is_greater(self, column1, column2, row):
        '''(Table, str, str, int) -> bool
        Checks whether a value on the same row in different columns is greater
        REQ: row > 0 and row < self._row_length
        REQ: (column1 in self._columns) == True
        REQ: (column2 in self._columns) == True
        '''        
        row1 = self.get_row_value(column1, row)
        row2 = self.get_row_value(column2, row)
        if(row1 > row2):
            return True
        else:
            return False

    def greater_than_value(self, column, value, row):
        '''(Table, str, obj, int) -> bool
        Checks whether a value on a row in a columns is greater than a given value
        REQ: row > 0 and row < self._row_length
        REQ: (column in self._columns) == True
        REQ: type(value) == type(column)
        '''
        if(self.get_row_value(column, row) > value):
            return True
        else:
            return False

    def get_row_value(self, column, row):
        '''(Table, str, int) -> obj
        Return the value found in the row of the given column
        REQ: row > 0 and row < self._row_length
        REQ: (column in self._columns) == True
        '''        
        return (self._table[column][row])

    def add_column(self, column_name):
        '''(Table, str) -> NoneType
        Creates an empty column on the table
        '''
        self._columns.append(column_name)
        self._table[column_name] = []

    def add_content(self, column_name, content):
        '''(Table, str, obj) -> NoneType
        Adds a row that contains a value to the column
        '''        
        self._table[column_name].append(content)
        self._row_length = len(self._table[column_name])

    def get_content(self, column_name):
        '''(Table, str) -> list of obj
        Returns all of the content in the given column
        REQ: (column_name in self._columns) == True
        '''
        return (self._table[column_name])

    def add_entire_column(self, column_name, full_content):
        '''(Table, str, list of obj) -> NoneType
        Creates a content with content attached to it
        ''' 
        self._table[column_name] = full_content
        self._columns.append(column_name)
        self._row_length = len(self._table[column_name])

    def remove_column(self, column_name):
        '''(Table, str) -> NoneType
        Completely remove the column from the table
        REQ: (column_name in self._columns) == True
        '''
        self._columns.remove(column_name)
        del self._table[column_name]

    def get_column_names(self):
        '''(Table) -> list of str
        Returns a list with the names of all columns found in this table
        '''
        return(self._columns)

    def get_row_length(self):
        '''(Table) -> int
        Returns the row length of any column
        '''
        return(self._row_length)

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self._table = new_dict
        self._columns = list(self._table.keys())
        random_col = self._columns[0]
        self._row_length = len(self.get_content(random_col))

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return(self._table)


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self):
        '''(Database) -> NoneType
        Initializes the database with a dict containing list of table objects
        and a a list that stores the names of tables
        '''
        self._database = {}
        self._table_names = []

    def add_table(self, key, table):
        '''(Database, str, Table) -> NoneType
        Add a table object to the database
        '''        
        self._database[key] = table
        self._table_names.append(key)

    def remove_table(self, key):
        '''(Database, str) -> NoneType
        Removes a table object from the database
        REQ: (remove_table in self._table_names) == True
        '''        
        del self._database[key]
        self._table_names.remove(key)

    def get_table(self, key):
        '''(Database, str) -> Table
        Retrieve a give table object
        '''        
        return self._database[key]

    def get_table_names(self):
        '''(Database) -> list of str
        Retrieve names of tables found within the database
        '''     
        return self._table_names

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._database = new_dict
        self._table_names = list(self._database.keys())

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._database()