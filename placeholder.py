from configparser import ConfigParser
from databases.dialects import SqliteDialect
import os.path as path
import csv
import os


BASE_CONFIG_PATH = path.join(os.path.dirname(__file__), 'config.ini')

def importSqlite():
    import sqlite3

def RaiseDatabaseNotSupportedError():
    raise DatabaseNotSupportedError()

SUPPORTED_DATABASE = {'sqlite': importSqlite}

class CsvToDatabase:

    def __init__(self, config_path=None, config_dict: dict = None):
        self.config = load_config(config_path, config_dict)
        self.cvsDirectories = self.config.get('csv', 'directories').split(',')
        self.databaseType = self.config.get('database', 'type')
        self.csvFilePaths = self.getCsvFilesToProcess()
        SUPPORTED_DATABASE.get(self.databaseType, RaiseDatabaseNotSupportedError)()


    def persistFiles(self):
        db_url = self.config.get('database', 'url')
        with CsvToDatabase(db_url) as csvImporter:
            for file_path in self.csvFilePaths:
                with open(file_path) as csv_file:
                    reader = csv.DictReader(csv_file)
            

    
    def getCsvFilesToProcess(self) -> list:
        return [path.join(root, name) for directory in self.cvsDirectories 
            for root, dirs, files in os.walk(directory)
                for name in files if name.endswith('.csv')]


class DatabaseNotSupportedError(NotImplementedError):                                                                                                                                                                                                                                           
    def __init__(self, message='Database not supported'):
        self.message = message


def load_config(config_path=None, config_dict: dict = None):
    config = ConfigParser()

    with open(BASE_CONFIG_PATH) as config_file:
        config.read_file(config_file)

    if config_dict is not None:
        config.read_dict(config_dict)

    if config_path is not None:
        if path.isdir(config_path):
            config_files = [path.join(config_path ,file_path) for file_path in os.listdir(config_path) if file_path.endswith('.ini') ]
            config.read(config_files)

        else:
            config.read(config_path)

    return config

def getTypeOf(value):

    try:
        int(value)
        return int
    except ValueError:
        pass
    
    try:
        float(value)
        return float
    except ValueError:
        pass
    
    return str

