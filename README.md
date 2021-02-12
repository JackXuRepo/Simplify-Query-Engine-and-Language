# Simplify-Query-Engine-and-Language (SQuEAL)
A mock simulator of a basic query engine that takes in .csv files and puts them in tables and databases to store formatted data which can be organized, sorted and allow query processes

## Usage:
**select** [column_1,column_2, ... ,column_n] **from** [table_1,table_2, ... ,table_n] **where** [column_1 operator_1 value_1,column_2 operator_2 value_2, ...,column_n operator_n value_n]

## Example:
**select** author,title,director,movie **from** books,movies **where** author contains 'ab',movie equals 'Star Wars'
