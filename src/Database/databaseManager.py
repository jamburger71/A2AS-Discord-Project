import logging
import sqlite3
import yaml
import os
from contextlib import closing

class DatabaseManager:

    def __init__(self, databaseName: str):
        
        self.DatabaseConnection = sqlite3.connect(databaseName, timeout=10)
        self.createTables()
        self.databaseName = databaseName

        self.DatabaseConnection.execute("PRAGMA journal_mode=WAL;")

    def createTables(self):

        self.dropAllTables()

        with closing(self.DatabaseConnection.cursor()) as cursor:
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS TeamData (
                TeamID INT PRIMARY KEY,
                TeamName SMALLTEXT,
                TeamDescription TEXT,
                Nationality TINYTEXT,
                OwnerDiscordID SMALLINT,
                IsActive BOOLEAN DEFAULT FALSE,
                EngineSupplier INT,
                Car SMALLTEXT,
                FirstDriver INT,
                SecondDriver INT,
                CurrentFunds INT DEFAULT 0,
                DragUpgrades INT DEFAULT 0,
                WeightUpgrades INT DEFAULT 0,
                PrimarySponsor INT,
                SecondarySponsor1 INT,
                SecondarySponsor2 INT,
                SecondarySponsor3 INT)
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS SeasonData (
                SeasonNo TINYINT PRIMARY KEY,
                SeasonName TEXT,
                SeasonClass SMALLTEXT,
                SeasonYear TINYTEXT,
                seasonStatus TINYINT
                )
            """)

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