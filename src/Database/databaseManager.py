import logging
import sqlite3
import yaml
import os
from contextlib import closing

class DatabaseManager:

    def __init__(self, databaseName: str):
        print(f"Creating database: {databaseName}")
        self.DatabaseConnection = sqlite3.connect(databaseName)
        self.createTables()
        self.databaseName = databaseName

    def createTables(self):

        #self.dropAllTables()

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS EventRounds (
                SeasonNo TINYINT,
                RoundNo TINYINT,
                EventTitle TINYTEXT,
                EventDate DATE,
                Weather TEXT,
                QualiDuration INT,
                QualiResults TEXT,
                RaceLength SMALLINT,
                RaceResults TEXT,
                PRIMARY KEY(SeasonNo, RoundNo))
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS TeamData (
                TeamID INT PRIMARY KEY,
                TeamName SMALLTEXT,
                IsActive BOOLEAN,
                EngineSupplier INT,
                TyreManufacturer TINYINT,
                Nationality TINYTEXT,
                OwnerName SMALLTEXT,
                OwnerDiscordID SMALLINT,
                FirstDriver INT,
                SecondDriver INT,
                CurrentFinances INT,
                DragUpgrades INT DEFAULT 0,
                WeightUpgrades INT DEFAULT 0,
                PrimarySponsor INT,
                SecondarySponsor1 INT,
                SecondarySponsor2 INT,
                SecondarySponsor3 INT,
                Wins SMALLINT DEFAULT 0,
                Podiums SMALLINT DEFAULT 0,
                Starts SMALLINT DEFAULT 0,
                Finishes SMALLINT DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS DriverData (
                DriverID INT PRIMARY KEY NOT NULL,
                FirstName SMALLTEXT,
                LastName SMALLTEXT,
                ThreeLetterCode TINYTEXT,
                Nationality TINYTEXT,
                Age TINYINT,
                QualiPace TINYINT,
                RacePace TINYINT,
                WetPace TINYINT,
                TyreManagement TINYINT,
                Aggressiveness TINYINT,
                Defending TINYINT,
                ContractCost SMALLINT,
                Races SMALLINT DEFAULT 0,
                Wins SMALLINT DEFAULT 0,
                Podiums SMALLINT DEFAULT 0,
                IsAvailable BOOLEAN DEFAULT 1
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS KeyVal (
                Key TEXT PRIMARY KEY,
                Value BLOB
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
            cursor.execute("DROP TABLE IF EXISTS EventRounds")
            cursor.execute("DROP TABLE IF EXISTS TeamData")
            cursor.execute("DROP TABLE IF EXISTS DriverData")
            cursor.execute("DROP TABLE IF EXISTS KeyVal")

    def deleteDatabase(self):
        self.DatabaseConnection.close()
        try:
            os.remove(f"{self.databaseName}")
        except Exception as e:
            print(e)