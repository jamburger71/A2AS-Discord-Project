import logging
import sqlite3
import yaml
import os
from contextlib import closing

from pathlib import Path

class DatabaseManager:

    def __init__(self, databaseName: str | None):

        if databaseName is None:
            raise ValueError("Database name cannot be None")

        self.DatabaseConnection = sqlite3.connect(databaseName)
        self.createTables()
        self.databaseName = databaseName
        self.setDefaults(False)

    def createTables(self):

        # self.dropAllTables()

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
                IsAvailable BOOLEAN DEFAULT True
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
    
    def setDefaults(self, overwrite: bool = False):

        yamlPath = Path(__file__).resolve().parent.parent / "FixedData" / "Defaults" / "DefaultKeyVals.yaml"

        with open(yamlPath) as stream:
            try:
                self.defaultKeyVals = yaml.safe_load(stream)
                with closing(self.DatabaseConnection.cursor()) as cursor:
                    for key, value in self.defaultKeyVals.items(): #Inserts any keys and default values if they dont already exist
                        if not overwrite:
                            cursor.execute("INSERT OR IGNORE INTO KeyVal (Key, Value) VALUES (?, ?)", (key, value))
                        else:
                            cursor.execute("INSERT OR REPLACE INTO KeyVal (Key, Value) VALUES (?, ?)", (key, value))
            except yaml.YAMLError as exception:
                logging.error(exception)

    def getKeyVal(self, key: str):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("SELECT Value FROM KeyVal WHERE Key = ?", (key,))
            return cursor.fetchone()[0]

    def updateKeyVal(self, key: str, value):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("UPDATE KeyVal SET Value = ? WHERE Key = ?", (value, key))
            self.DatabaseConnection.commit()

    def dropAllTables(self):
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("DROP TABLE IF EXISTS EventRounds")
            cursor.execute("DROP TABLE IF EXISTS TeamData")
            cursor.execute("DROP TABLE IF EXISTS DriverData")
            self.setDefaults(True)

    def deleteDatabase(self):
        self.DatabaseConnection.close()
        os.remove(f"{self.databaseName}")
    
    def getOwnerTeam(self, ownerID) -> tuple | None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM TeamData
                WHERE OwnerDiscordID = {ownerID}
                AND IsActive = True
                LIMIT 1
            """)
            return cursor.fetchone()

    def getAvailableTeamSlots(self):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM TeamData
                WHERE IsActive
            """)
            maxTeamSlots = self.getKeyVal("MaxTeamSlots")
            return maxTeamSlots - cursor.fetchone()[0]

    def tyreIsAvailable(self, tyremanufacturer: str) -> bool:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM TeamData
                WHERE TyreManufacturer = ?
            """, (tyremanufacturer,))
            count = cursor.fetchone()[0]
            return count < 5

    def updateTeamName(self, teamID: int, newTeamName: str) -> None:
    
            with closing(self.DatabaseConnection.cursor()) as cursor:
                cursor.execute("""
                    UPDATE TeamData
                    SET TeamName = ?
                    WHERE TeamID = ?
                """, (newTeamName, teamID))
                self.DatabaseConnection.commit()
    
    def getNextTeamID(self, increment: bool = False) -> int:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("SELECT Value FROM KeyVal WHERE Key = 'NextTeamID'")
            if increment:
                cursor.execute("UPDATE KeyVal SET Value = Value + 1 WHERE Key = 'NextTeamID'")
                self.DatabaseConnection.commit()
            return cursor.fetchone()

    def registerTeam(
            self, 
            ownerID: int, 
            teamName: str, 
            nationality: str, 
            driver1: str, 
            driver2: str, 
            primarySponsor: str, 
            secondarySponsor1: str, 
            secondarySponsor2: str, 
            secondarySponsor3: str, 
            engineSupplier: str, 
            tyremanufacturer: str):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            teamID = self.getNextTeamID(increment=True)
            cursor.execute("""
                INSERT INTO TeamData (TeamID, OwnerDiscordID, TeamName, TeamNationality, Driver1, Driver2, PrimarySponsor, SecondarySponsor1, SecondarySponsor2, SecondarySponsor3, EngineSupplier, TyreManufacturer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (teamID, ownerID, teamName, nationality, driver1, driver2, primarySponsor, secondarySponsor1, secondarySponsor2, secondarySponsor3, engineSupplier, tyremanufacturer))
            self.DatabaseConnection.commit()

    def changeTeamOwnership(self, teamID: int, newOwnerID: int) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                UPDATE TeamData
                SET OwnerDiscordID = ?
                WHERE TeamID = ?
            """, (newOwnerID, teamID))
            self.DatabaseConnection.commit()

    def checkIfUserOwnsTeam(self, ownerID: int) -> bool:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM TeamData
                WHERE OwnerDiscordID = ?
                AND IsActive = True
            """, (ownerID,))
            count = cursor.fetchone()[0]
            return count > 0

    def insertDriver(self, firstName: str, lastName: str, threeLetterCode: str, nationality: str, age: int, qualiPace: int, racePace: int, wetPace: int, tyreManagement: int, aggressiveness: int, defending: int, contractCost: int):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            driverID = self.getNextDriverID(increment=True)
            cursor.execute("""
                INSERT INTO DriverData (DriverID, FirstName, LastName, ThreeLetterCode, Nationality, Age, QualiPace, RacePace, WetPace, TyreManagement, Aggressiveness, Defending, ContractCost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (driverID, firstName, lastName, threeLetterCode, nationality, age, qualiPace, racePace, wetPace, tyreManagement, aggressiveness, defending, contractCost))
            self.DatabaseConnection.commit()

    def removeDriver(self, driverID: int | str):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if isinstance(driverID, str):
                cursor.execute("""
                    DELETE FROM DriverData
                    WHERE ThreeLetterCode = ?
                """, (driverID,))
            else:
                cursor.execute("""
                    DELETE FROM DriverData
                    WHERE DriverID = ?
                """, (driverID,))
            self.DatabaseConnection.commit()

    def updateDriverStats(self, driverID: int, won: bool, podium: bool) -> None: # Assumed driver raced or wouldnt bother updating stats

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                UPDATE DriverData
                SET Races = Races + ?,
                    Wins = Wins + ?,
                    Podiums = Podiums + ?
                WHERE DriverID = ?
            """, (1, 1 if won else 0, 1 if won | podium else 0, driverID))

    def updateDriverRatings(self, 
                            driverID: int, 
                            qualiPaceChange: int, 
                            racePaceChange: int, 
                            wetPaceChange: int, 
                            tyreManagementChange: int, 
                            aggressivenessChange: int, 
                            defendingChange: int) -> None:
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                UPDATE DriverData
                SET QualiPace = QualiPace + ?,
                    RacePace = RacePace + ?,
                    WetPace = WetPace + ?,
                    TyreManagement = TyreManagement + ?,
                    Aggressiveness = Aggressiveness + ?,
                    Defending = Defending + ?
                WHERE DriverID = ?
            """, (max(0, min(100, qualiPaceChange)), 
                  max(0, min(100, racePaceChange)), 
                  max(0, min(100, wetPaceChange)), 
                  max(0, min(100, tyreManagementChange)), 
                  max(0, min(100, aggressivenessChange)), 
                  max(0, min(100, defendingChange)), 
                  driverID))
            self.DatabaseConnection.commit()

    def getAllDrivers(self, availableOnly: bool = False) -> list:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if availableOnly:
                cursor.execute("SELECT * FROM DriverData WHERE IsAvailable = True")
            else:
                cursor.execute("SELECT * FROM DriverData")
            return cursor.fetchall()

    def getDriver(self, driverID: int | str) -> tuple | None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if isinstance(driverID, str):
                cursor.execute("SELECT * FROM DriverData WHERE ThreeLetterCode = ?", (driverID,))
            else:
                cursor.execute("SELECT * FROM DriverData WHERE DriverID = ?", (driverID,))
            return cursor.fetchone()

    def getNextDriverID(self, increment: bool = False) -> int:

        driverID = self.getKeyVal("NextDriverID")
        if increment:
            self.updateKeyVal("NextDriverID", driverID + 1)
        return driverID

    def checkDriverAvailability(self, driverID: int | str) -> bool:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if isinstance(driverID, str):
                cursor.execute("SELECT IsAvailable FROM DriverData WHERE ThreeLetterCode = ?", (driverID,))
            else:
                cursor.execute("SELECT IsAvailable FROM DriverData WHERE DriverID = ?", (driverID,))
            result = cursor.fetchone()
            return result is not None

    def setDriverAvailability(self, driverID: int, isAvailable: bool) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("UPDATE Drivers SET IsAvailable = ? WHERE DriverID = ?", (isAvailable, driverID))
            self.DatabaseConnection.commit()

    def ageAllDrivers(self) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("UPDATE Drivers SET Age = Age + 1")
            self.DatabaseConnection.commit()

