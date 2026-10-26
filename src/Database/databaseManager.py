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
                CREATE TABLE IF NOT EXISTS DriverData (
                ThreeLetterCode TINYTEXT PRIMARY KEY,
                FirstName SMALLTEXT,
                LastName SMALLTEXT,
                Gender SMALLTEXT,
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
                IsAvailable BOOLEAN DEFAULT 1)
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS CarData (
                ID SMALLTEXT PRIMARY KEY,
                Name SMALLTEXT,
                Description TEXT,
                Manufacturer SMALLTEXT,
                Year TINYTEXT,
                MaxTeams TINYINT,
                CarClass TEXT)
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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS SecondarySponsorData (
                ID SMALLINT PRIMARY KEY,
                Name SMALLTEXT,
                ContractLength TINYINT,
                IsAvailable BOOLEAN,
                SigningPay INT,
                RacePay INT
                )
            """)

            cursor.execute("""
            Select Top 0 * into PrimarySponsorData from SecondarySponsorData
            """)
            cursor.execute("""
            ALTER TABLE PrimarySponsorData
            ADD
                Target SMALLINT,
                TargetType TINYINT,
                TargetReward INT
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