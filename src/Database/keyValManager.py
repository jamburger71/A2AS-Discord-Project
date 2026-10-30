import logging
import sqlite3
import yaml
import os
from contextlib import closing

TABLENAME = "KeyVal"
KEY = "Key"
VALUE = "Value"

class KeyValManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS KeyVal (
                Key TEXT PRIMARY KEY,
                Value BLOB)
            """)
        self.setDefaults()

    def setDefaults(self, overwrite: bool = False):

        with open("Resources\\Defaults\\DefaultKeyVals.yaml") as stream:
            try:
                self.defaultKeyVals = yaml.safe_load(stream)
                with closing(self.databaseConnection.cursor()) as cursor:
                    for key, value in self.defaultKeyVals.items(): #Inserts any keys and default values if they dont already exist
                        if not overwrite:
                            cursor.execute(f"INSERT OR IGNORE INTO {TABLENAME} VALUES ({key}, {value})")
                        else:
                            cursor.execute(f"INSERT OR REPLACE INTO {TABLENAME} VALUES ({key}, {value})")
            except yaml.YAMLError as exception:
                print(exception)

    def getKeyVal(self, key: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT {VALUE} FROM {TABLENAME} WHERE {KEY} = {key} LIMIT 1")
            return cursor.fetchone()[0]

    def updateKeyVal(self, key: str, value):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"UPDATE {TABLENAME} SET {VALUE} = {value} WHERE {KEY} = {key}")
            self.databaseConnection.commit()
    
    def getAndIterateKeyVal(self, key: str):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT {VALUE} FROM {TABLENAME} WHERE {KEY} = {key} LIMIT 1")
            value = cursor.fetchOne()[0]
            cursor.execute(f"UPDATE {TABLENAME} SET {VALUE} = {value + 1} WHERE {KEY} = {key}")
            return value