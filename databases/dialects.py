
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager


class BaseSqlDialect(AbstractContextManager):
    """
        Abstract base class that defines behavior for SQL databases dialects
    """
    @abstractmethod
    def __init__(self):
        pass


    @abstractmethod
    def createTable(self):
        pass


    @abstractmethod
    def insertIntoTable(self, table: str, values):
        pass


class SqliteDialect(BaseSqlDialect):

    DIALECT = "sqlite"

    DATA_TYPES = {int: 'INTEGER', float: 'REAL', str: 'TEXT', None: 'NULL' }
    
    def __init__(self, dbUri):
        import sqlite3
        self.connection = sqlite3.connect(dbUri)
        self.cursor = self.connection.cursor()


    def createTable(self, table: str, fields):
        statement = "CREATE TABLE IF NOT EXIST {} (".format(table)
        for field in fields:
            field[0] + field[1]
        pass


    def insertInto(self, table: str, values: list, field_count):
        statement = "INSERT INTO {} VALUES ".format(table)

        wildcards = ','.join(['?'] * field_count)
        insert_statement = statement + "("+ wildcards +")"

        if field_count > 1:
            self.cursor.executemany(insert_statement, values)
        else:
            self.cursor.execute(insert_statement, values)

        self.connection.commit()


    def __exit__(self, exc_type, exc, exc_tb):

        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
        
        return True
    
