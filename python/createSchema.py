import pyodbc
import os



def connect_to_iris():
    connection = get_connection_config()
    
    # Connect to InterSystems IRIS using PyODBC
    connection_string = 'DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}'\
        .format(connection['driver'], connection['ip'], int(connection['port']),\
         connection['namespace'], connection['username'], connection['password'])
    pyodbc_connection = pyodbc.connect(connection_string)

    # For python 3 and above.
    pyodbc_connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
    pyodbc_connection.setencoding(encoding='utf-8')

    # If you are using python 2 or before, replace the setencoding() and setdecoding() methods above
    # with the commented out implementation below:

    # pyodbc_connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8', to=str)
    # pyodbc_connection.setencoding(str, encoding='utf-8')

    print("Connected to InterSystem IRIS")
    return pyodbc_connection

def get_connection_config():
    with open("../connections.config") as f:
        f = f.read()
        f = f.strip()
        f = f.split("\n")
        dict = {}
        for line in f:
            line = line.split(":")
            dict[line[0].strip()] = line[1].strip()
        return dict

# Remove old table if exist
def delete_old_table(cursor, table_name):
    drop_table = "DROP TABLE {}".format(table_name)
    cursor.execute(drop_table)


def create_employee(connection):
    # Create cursor
    cursor = connection.cursor()

    # Paste create statement below

    try:
        cursor.execute(create_employee)
    except Exception as e:
        delete_old_table(cursor, "Demo.Employee")
        cursor.execute(create_employee)

    connection.commit()
    print("created table successfully")

def run():
    # Get connections for PyODBC
    pyodbc_connection = connect_to_iris()

    # Populate and retrieve data using PyODBC
    create_employee(pyodbc_connection)



if __name__ == '__main__':
    run()
