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

        self.databaseConnection = databaseConnection

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
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {OWNERID} = {ownerID}")
            return Team(cursor.fetchone())

    def getTeamByID(self, teamID: int) -> Team:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {OWNERID} = {teamID}")
            return Team(cursor.fetchone())
    
    def getTeams(self):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Team(team) for team in cursor.fetchall()]
    
    def updateTeam(self, team: Team) -> None:
    
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
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
                ) = {str(team.toTuple())}
                WHERE {ID} = {team.ID}
            """)
            self.databaseConnection.commit()

    def insertTeam(self, team: Team):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {str(team.toTuple())}")
            self.databaseConnection.commit()

    def deleteTeam(self, teamID: int):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"DELETE FROM {TABLENAME} WHERE {ID} = {teamID}")
            self.databaseConnection.commit()