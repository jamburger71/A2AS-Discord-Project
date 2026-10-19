import logging
import sqlite3
import yaml
import os
from contextlib import closing

class TeamManager:

    def __init__(self, databaseConnection):

        self.DatabaseConnection = databaseConnection

    def getOwnerTeam(self, ownerID: int) -> tuple | None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM TeamData
                WHERE OwnerDiscordID = ?
                LIMIT 1
            """, (ownerID,))
            return cursor.fetchone()
    
    def getTeams(self):
        
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""SELECT * FROM TeamData""")
            return cursor.fetchall()

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
            teamDescription: str,
            nationality: str, 
            teamID: int) -> None:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO TeamData (TeamID, OwnerDiscordID, TeamName, TeamDescription, Nationality)
                VALUES (?, ?, ?, ?, ?)
            """, (teamID, ownerID, teamName, teamDescription, nationality,))
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