import sqlite3
import yaml
from contextlib import closing

class DatabaseManager:

    def __init__(self, databaseName: str):

        self.DatabaseConnection = sqlite3.connect(databaseName)
        self.createTables()

    def createTables(self):

        with open("FixedData\Defaults\DefaultKeyVals") as stream:
            try:
                defaultKeyVals = yaml.safe_load(stream)
            except yaml.YAMLerror as exception:
                print(exception)

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
                ShortName TINYTEXT,
                IsActive BOOLEAN,
                EngineSupplier INT,
                TyreSupplier TINYINT,
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
                Wins SMALLINT,
                Podiums SMALLINT,
                Starts SMALLINT,
                Finishes SMALLINT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS DriverData (
                DriverID INT PRIMARY KEY,
                FirstName SMALLTEXT,
                LastName SMALLTEXT,
                Age TINYINT,
                QualiPace TINYINT,
                RacePace TINYINT,
                WetPace TINYINT,
                TyreManagement TINYINT,
                Aggressiveness TINYINT,
                Defending TINYINT,
                ContractCost SMALLINT,
                EventCost SMALLINT,
                Races SMALLINT,
                Wins SMALLINT,
                Podiums SMALLINT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS KeyVal (
                Key TEXT PRIMARY KEY,
                Value BLOB
                )
            """)
            for key, value in defaultKeyVals: #Inserts any keys and default values if they dont already exist
                cursor.execute(f"""
                    INSERT IGNORE INTO KeyVal VALUES 
                    ({key}, {value})
                """)

    def dropAllTables(self):
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute(#TODO)

    def getOwnerTeam(self, ownerID):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                SELECT * FROM TeamData
                WHERE OwnerDiscordID = {ownerID}
                AND IsActive = True
            """)
            return cursor.fetchone()

    def getAvailableTeamSlots(self):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM TeamData
                WHERE IsActive
            """)

    def getDrivers(self):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Drivers")