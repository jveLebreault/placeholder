from configparser import ConfigParser
import os
import os.path as path
import sqlite3
import csv

def load_config() -> ConfigParser:
    config = ConfigParser()
    config.read('config.ini')
    return config

def get_csv_paths (directories: list) -> list:
    return [path.join(root, name) for directory in directories 
        for root, dirs, files in os.walk(directory)
            for name in files if name.endswith('.csv')]

def connect_to(database_config):
    if database_config['type'] == 'sqlite':
        return sqlite3.connect(database_config['uri'])
    else:
        raise NotImplementedError()

def insert_csv(table_name: str, csv_reader: csv.DictReader, c):
    fieldnames_count = len(csv_reader.fieldnames)
    params = ["?" if fieldnames_count == 1 or i == (fieldnames_count - 1) else "?, " 
                for i, fieldname in enumerate(csv_reader.fieldnames)]
    insert_statement = "INSERT INTO {} VALUES ".format(table_name)
    insert_statement += "( "+ ''.join(params)+ " ) "
    values = [tuple(row.values()) for row in csv_reader]

    c.executemany(insert_statement, values)
    print('INSERT:\n'+insert_statement)
    print('VALUES: '+str(values))



def write_csv_to(connection, csv_reader: csv.DictReader, file_path: str):
    filename = os.path.basename(file_path).split('.csv')[0]
    print(filename)
    table_creation = "CREATE TABLE IF NOT EXISTS {} "
    table_fields = ""
    fieldnames = csv_reader.fieldnames
    if fieldnames is not None:
        for i in range(len(fieldnames)):
            if i == 0:
                table_fields = " {} TEXT PRIMARY KEY, "
            elif i == (len(fieldnames) - 1):
                table_fields +=" {} TEXT"
            else:
                table_fields += " {} TEXT, "
            
        table_creation += "(" + table_fields + ") "
        print(table_creation.format(filename, *fieldnames))
        #query_params = (*fieldnames,)
        # print(table_creation.format(filename, *fieldnames))
        
        cursor = connection.cursor()
        cursor.execute(table_creation.format(filename, *fieldnames))

        insert_csv(filename, csv_reader, cursor)



        


    


print('***********\nFILEPATH: ', os.path.realpath(__file__) )

config = load_config()

directories = config.get('csv', 'directories').split(',')

csv_paths = get_csv_paths(directories)

connection = connect_to(config['database'])

for file_path in csv_paths:
    with open(file_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        write_csv_to(connection, reader, file_path)

connection.commit()
connection.close()

print(csv_paths)
print(config['database'])


