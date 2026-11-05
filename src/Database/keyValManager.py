
import logging
import sqlite3
import yaml
import os
from contextlib import closing
from pathlib import Path

TABLENAME = "KeyVal"
KEY = "Key"
VALUE = "Value"

class KeyValManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {KEY} TEXT PRIMARY KEY,
                {VALUE} BLOB
            )""")
        self.setDefaults()

    def setDefaults(self, overwrite: bool = False):

        path = Path(__file__).resolve().parent.parent.parent / "Resources" / "Defaults" / "DefaultKeyVals.yaml"
        with open(path) as stream:
            try:
                self.defaultKeyVals = yaml.safe_load(stream)
                with closing(self.databaseConnection.cursor()) as cursor:
                    for key, value in self.defaultKeyVals.items(): #Inserts any keys and default values if they dont already exist
                        params = (key, value)
                        if not overwrite:
                            query = f"INSERT OR IGNORE INTO {TABLENAME} VALUES (?, ?)"
                        else:
                            query = f"INSERT OR UPDATE INTO {TABLENAME} VALUES (?, ?)"
                        cursor.execute(query, params)
                    self.databaseConnection.commit()
            except yaml.YAMLError as exception:
                print(exception)

    def insertKeyVal(self, key: str, value):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?)"
            params = (key, value)
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def getKeyVal(self, key: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT {VALUE} FROM {TABLENAME} WHERE {KEY} = ?"
            params = (key,)
            cursor.execute(query, params)
            return cursor.fetchone()[0]

    def updateKeyVal(self, key: str, value):

        with closing(self.databaseConnection.cursor()) as cursor:
            
            query = f"UPDATE {TABLENAME} SET {VALUE} = ? WHERE {KEY} = ?"
            params = (value, key)
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def deleteKeyVal(self, key: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {KEY} = ?"
            params = (key, )
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def getAndIterateKeyVal(self, key: str):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT {VALUE} FROM {TABLENAME} WHERE {KEY} = ?"
            params = (key, )
            cursor.execute(query, params)
            value = cursor.fetchOne()[0]
            query = f"UPDATE {TABLENAME} SET {VALUE} = ? WHERE {KEY} = ?"
            params = (value+1, key)
            cursor.execute(query, params)
            self.databaseConnection.commit()
            return value

    def getAllKeyVals(self) -> list[tuple]:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME}"
            cursor.execute(query)
            return list(cursor.fetchall())