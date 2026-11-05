import logging
import sqlite3
import yaml
import os
from contextlib import closing

class DatabaseManager:

    def __init__(self, databaseName: str):
        
        self.DatabaseConnection = sqlite3.connect(databaseName + ".db", timeout=10)
        self.databaseName = databaseName + ".db"

        self.DatabaseConnection.execute("PRAGMA journal_mode=WAL;")

    def checkTableExists(self, tableName: str) -> bool:
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                SELECT 1 FROM sqlite_master 
                WHERE type = 'table'
                AND name = ?""", (tableName,))
            return cursor.fetchone() is not None

    def dropAllTables(self):
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute(f'DROP TABLE IF EXISTS "{table_name[0]}"')

            self.DatabaseConnection.commit()

    def deleteDatabase(self):
        self.DatabaseConnection.close()
        try:
            os.remove(f"{self.databaseName}")
        except Exception as e:
            print(e)