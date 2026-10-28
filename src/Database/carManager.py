from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.car import Car

TABLENAME = "CarData"
ID = "ID"
NAME = "Name"
DESCRIPTION = "Description"
MANUFACTURER = "Manufacturer"
YEAR = "Year"
CLASS = "Class"
MAXTEAMS = "MaxTeams"
DEFAULTWEIGHT = "DefaultWeight"
BASEWEIGHT = "BaseWeight"
WEIGHTUPGRADESIZE = "WeightUpgradeSize"
MAXWEIGHTUPGRADES = "MaxWeightUpgrades"
BASEDRAG = "BaseDrag"
DRAGUPGRADESIZE = "DragUpgradeSize"
MAXDRAGUPGRADES = "MaxDragUpgrades"

class CarManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {ID} SMALLTEXT PRIMARY KEY,
                {NAME} SMALLTEXT,
                {DESCRIPTION} TEXT,
                {MANUFACTURER} SMALLTEXT,
                {YEAR} TINYTEXT,
                {CLASS} TEXT,
                {MAXTEAMS} TINYINT,
                {DEFAULTWEIGHT} INT,
                {BASEWEIGHT} INT,
                {WEIGHTUPGRADESIZE} REAL,
                {MAXWEIGHTUPGRADES} TINYINT,
                {BASEDRAG} REAL,
                {DRAGUPGRADESIZE} REAL,
                {MAXDRAGUPGRADES} TINYINT
            )""")


    def insertCar(self, car: Car):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {str(car.toTuple())}")

    def getCar(self, carID: int) -> Car:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE ID = {carID}")
            return Car(cursor.fetchone())
        
    def getCarsInClass(self, carClass: str) -> list[Car]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {CLASS} = {carClass}")
            return list(map(Car, cursor.fetchall()))
    
    def getCars(self) -> list[Car]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return list(map(Car, cursor.fetchall()))
    
    def updateCar(self, car: Car):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                UPDATE CarData
                SET
                ({ID},
                {NAME},
                {DESCRIPTION},
                {MANUFACTURER},
                {YEAR},
                {CLASS},
                {MAXTEAMS},
                {DEFAULTWEIGHT},
                {BASEWEIGHT},
                {WEIGHTUPGRADESIZE},
                {MAXWEIGHTUPGRADES}
                {BASEDRAG},
                {DRAGUPGRADESIZE},
                {MAXDRAGUPGRADES})
                = {str(car.toTuple())}
                WHERE ID = {car.id}
            """)
            cursor.commit()

    def deleteCar(self, carID: int):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"DELETE FROM {TABLENAME} WHERE {ID} = {carID}")
            cursor.commit()