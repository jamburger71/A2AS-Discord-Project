import logging
import sqlite3
import yaml
import os
from contextlib import closing

class KeyValManager:

    def __init__(self, databaseConnection):

        self.DatabaseConnection = databaseConnection
        self.setDefaults()

    def setDefaults(self, overwrite: bool = False):

        with open("FixedData\\Defaults\\DefaultKeyVals.yaml") as stream:
            try:
                self.defaultKeyVals = yaml.safe_load(stream)
                with closing(self.DatabaseConnection.cursor()) as cursor:
                    for key, value in self.defaultKeyVals.items(): #Inserts any keys and default values if they dont already exist
                        if not overwrite:
                            cursor.execute("INSERT OR IGNORE INTO KeyVal (Key, Value) VALUES (?, ?)", (key, value))
                        else:
                            cursor.execute("INSERT OR REPLACE INTO KeyVal (Key, Value) VALUES (?, ?)", (key, value))
            except yaml.YAMLError as exception:
                print(exception)

    def getKeyVal(self, key: str):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("SELECT Value FROM KeyVal WHERE Key = ?", (key,))
            return cursor.fetchone()[0]

    def updateKeyVal(self, key: str, value):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("UPDATE KeyVal SET Value = ? WHERE Key = ?", (value, key))
            self.DatabaseConnection.commit()

    def getNextDriverID(self, keyValManager, increment: bool = False) -> int:

        driverID = keyValManager.getKeyVal("NextDriverID")
        if increment:
            keyValManager.updateKeyVal("NextDriverID", driverID + 1)
        print(f"Next driver ID: {driverID}")
        return driverID