from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.driver import Driver

class DriverManager:

    def __init__(self, databaseConnection):

        self.DatabaseConnection = databaseConnection

    def insertDriver(self, driverID: int, firstName: str, lastName: str, threeLetterCode: str, nationality: str, age: int, qualiPace: int, racePace: int, wetPace: int, tyreManagement: int, aggressiveness: int, defending: int, contractCost: int, isAvailable: bool = True):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            try:
                cursor.execute("""
                    INSERT INTO DriverData (FirstName, LastName, ThreeLetterCode, Nationality, Age, QualiPace, RacePace, WetPace, TyreManagement, Aggressiveness, Defending, ContractCost, IsAvailable)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (firstName, lastName, threeLetterCode, nationality, age, qualiPace, racePace, wetPace, tyreManagement, aggressiveness, defending, contractCost, isAvailable))
                self.DatabaseConnection.commit()
            except sqlite3.IntegrityError as e:
                self.DatabaseConnection.rollback()
                print(f"Failed to insert driver {firstName} {lastName} with ID {threeLetterCode}: {e}")
                logging.error(f"Failed to insert driver {firstName} {lastName} with ID {driverID}: {e}")
                raise e

    def insertDriverFromClass(self, driver: Driver):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO DriverData (DriverID, FirstName, LastName, ThreeLetterCode, Nationality, Age, QualiPace, RacePace, WetPace, TyreManagement, Aggressiveness, Defending, ContractCost, IsAvailable)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (driver.id, driver.firstName, driver.lastName, driver.threecode, driver.nationality, driver.age, driver.qualiPace, driver.racePace, driver.wetPace, driver.tyreManagement, driver.aggressiveness, driver.defending, driver.contractCost, driver.isAvailable))
            self.DatabaseConnection.commit()

    def updateDriverStats(self, driverID: int, won: bool = False, podium: bool = False) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if won:
                cursor.execute("UPDATE DriverData SET Wins = Wins + 1 WHERE DriverID = ?", (driverID,))
            if podium:
                cursor.execute("UPDATE DriverData SET Podiums = Podiums + 1 WHERE DriverID = ?", (driverID,))
            cursor.execute("UPDATE DriverData SET Races = Races + 1 WHERE DriverID = ?", (driverID,))
            self.DatabaseConnection.commit()

    def updateDriverRatings(self, driverID: int, qualiPace: int | None = None, racePace: int | None = None, wetPace: int | None = None, tyreManagement: int | None = None, aggressiveness: int | None = None, defending: int | None = None) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if qualiPace is not None:
                cursor.execute("UPDATE DriverData SET QualiPace = ? WHERE DriverID = ?", (qualiPace, driverID))
            if racePace is not None:
                cursor.execute("UPDATE DriverData SET RacePace = ? WHERE DriverID = ?", (racePace, driverID))
            if wetPace is not None:
                cursor.execute("UPDATE DriverData SET WetPace = ? WHERE DriverID = ?", (wetPace, driverID))
            if tyreManagement is not None:
                cursor.execute("UPDATE DriverData SET TyreManagement = ? WHERE DriverID = ?", (tyreManagement, driverID))
            if aggressiveness is not None:
                cursor.execute("UPDATE DriverData SET Aggressiveness = ? WHERE DriverID = ?", (aggressiveness, driverID))
            if defending is not None:
                cursor.execute("UPDATE DriverData SET Defending = ? WHERE DriverID = ?", (defending, driverID))
            self.DatabaseConnection.commit()

    def updateDriverName(self, driverID: int, firstName: str | None = None, lastName: str | None = None) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if firstName is not None:
                cursor.execute("UPDATE DriverData SET FirstName = ? WHERE DriverID = ?", (firstName, driverID))
            if lastName is not None:
                cursor.execute("UPDATE DriverData SET LastName = ? WHERE DriverID = ?", (lastName, driverID))
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

    def getAllDrivers(self, availableOnly: bool = False) -> list[Driver]:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            if availableOnly:
                cursor.execute("SELECT * FROM DriverData WHERE IsAvailable = True")
            else:
                cursor.execute("SELECT * FROM DriverData")
            drivers = cursor.fetchall()
            return [Driver(driverData) for driverData in drivers]

    def getDriver(self, driverID: int) -> Driver | None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("SELECT * FROM DriverData WHERE DriverID = ?", (driverID,))
            driverData = cursor.fetchone()
            return Driver(driverData)

    def getAllThreecodes(self) -> list[str]:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT Threecode FROM DriverData")
            return [row[0] for row in cursor.fetchall()]
    
    def checkDriverAvailability(self, driverID: int | str) -> bool:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("SELECT IsAvailable FROM DriverData WHERE ThreeLetterCode = ?", (driverID,))
            result = cursor.fetchone()
            return result is not None

    def setDriverAvailability(self, driverID: int, isAvailable: bool) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("UPDATE DriverData SET IsAvailable = ? WHERE DriverID = ?", (isAvailable, driverID))
            self.DatabaseConnection.commit()

    def ageAllDrivers(self, discLogger: DiscordLogger) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            try:
                discLogger.info("Increasing all driver ages by 1")
                cursor.execute("UPDATE DriverData SET Age = Age + 1")
                discLogger.info("Committing changes to database")
                self.DatabaseConnection.commit()
            except Exception as e:
                template = "An exception of type {0} occurred. Arguments: {1!r}"
                message = template.format(type(e).__name__, e.args)
                discLogger.error(message)