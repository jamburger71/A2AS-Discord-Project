from termios import TAB0
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
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {car.toTuple()}")

    def getCar(self, carID: int) -> Car:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE ID = ?", carID)
            return Car(cursor.fetchone())
    
    def editCar(self, car: Car):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute("""
                UPDATE CarData
                SET (ID, Name, Description, Manufacturer, Year, MaxTeams, CarClass)
                = (?, ?, ?, ?, ?, ?)
                WHERE ID = ?
            """, car.toTuple() + (car.id, ))
            cursor.commit()

    def deleteCar(self, carID: int):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                DELETE FROM CarData
                WHERE ID = ?
            """, (carID))
            cursor.commit()