import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.team import Team
from Classes.driver import Driver

TABLENAME = "TeamData"
ID = "ID"
NAME = "Name"
DESCRIPTION = "Description"
OWNERID = "OwnerID"
ENGINE = "Engine"
CAR = "Car"
DRIVERONE = "DriverOne"
DRIVERTWO = "DriverTwo"
CURRENTFUNDS = "CurrentFunds"
DRAGUPGRADES = "DragUpgrades"
WEIGHTUPGRADES = "WeightUpgrades"
PRIMARYSPONSOR = "PrimarySponsor"
SECONDARYSPONSOR1 = "SecondarySponsor1"
SECONDARYSPONSOR2 = "SecondarySponsor2"
SECONDARYSPONSOR3 = "SecondarySponsor3"

class TeamManager:

    def __init__(self, databaseConnection):

        self.databaseConnection: sqlite3.Connection = databaseConnection

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {ID} INT PRIMARY KEY,
                {NAME} SMALLTEXT,
                {DESCRIPTION} TEXT,
                {OWNERID} TEXT,
                {ENGINE} SMALLTEXT,
                {CAR} SMALLTEXT,
                {DRIVERONE} SMALLINT,
                {DRIVERTWO} SMALLINT,
                {CURRENTFUNDS} INT,
                {DRAGUPGRADES} TINYINT,
                {WEIGHTUPGRADES} TINYINT,
                {PRIMARYSPONSOR} SMALLINT,
                {SECONDARYSPONSOR1} SMALLINT,
                {SECONDARYSPONSOR2} SMALLINT,
                {SECONDARYSPONSOR3} SMALLINT
            )""")

    def getTeamByOwner(self, ownerID: int) -> Team:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {OWNERID} = ?"
            params = (ownerID, )
            cursor.execute(query, params)
            return Team.new(cursor.fetchone())

    def getTeamByID(self, teamID: int) -> Team:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {ID} = ?"
            params = (teamID, )
            cursor.execute(query, params)
            return Team.new(cursor.fetchone())
    
    def getTeams(self):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Team.new(team) for team in cursor.fetchall()]
    
    def updateTeam(self, team: Team) -> None:
    
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""
                UPDATE {TABLENAME}
                SET (
                {ID},
                {NAME},
                {DESCRIPTION},
                {OWNERID},
                {ENGINE},
                {CAR},
                {DRIVERONE},
                {DRIVERTWO},
                {CURRENTFUNDS},
                {DRAGUPGRADES},
                {WEIGHTUPGRADES},
                {PRIMARYSPONSOR},
                {SECONDARYSPONSOR1},
                {SECONDARYSPONSOR2},
                {SECONDARYSPONSOR3}
                ) = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                WHERE {ID} = ?
            """
            params = team.toTuple() + (team.ID, )
            self.databaseConnection.commit()

    def insertTeam(self, team: Team):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = team.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def deleteTeam(self, teamID: int):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {ID} = ?"
            params = (teamID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()