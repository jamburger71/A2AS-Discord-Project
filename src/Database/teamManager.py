import logging
import sqlite3
import yaml
import os
from contextlib import closing

class TeamManager:

    def __init__(self, databaseConnection):

        self.DatabaseConnection = databaseConnection

    def getOwnerTeam(self, ownerID) -> tuple | None:

        logging.info(f"Getting team for ownerID: {ownerID}")
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM TeamData
                WHERE OwnerDiscordID = {ownerID}
                AND IsActive = True
                LIMIT 1
            """)
            return cursor.fetchone()

    def getAvailableTeamSlots(self, maxSlots):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM TeamData
                WHERE IsActive
            """)
            return maxSlots - cursor.fetchone()[0]

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
                """, (newTeamName, teamID,))
                self.DatabaseConnection.commit()

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
            tyremanufacturer: str,
            teamID: int) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO TeamData (TeamID, OwnerDiscordID, TeamName, TeamNationality, Driver1, Driver2, PrimarySponsor, SecondarySponsor1, SecondarySponsor2, SecondarySponsor3, EngineSupplier, TyreManufacturer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (teamID, ownerID, teamName, nationality, driver1, driver2, primarySponsor, secondarySponsor1, secondarySponsor2, secondarySponsor3, engineSupplier, tyremanufacturer,))
            self.DatabaseConnection.commit()

    def changeTeamOwnership(self, teamID: int, newOwnerID: int) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                UPDATE TeamData
                SET OwnerDiscordID = ?
                WHERE TeamID = ?
            """, (newOwnerID, teamID,))
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