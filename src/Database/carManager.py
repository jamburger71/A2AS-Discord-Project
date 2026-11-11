  
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

        self.databaseConnection: sqlite3.Connection = databaseConnection
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {ID} SMALLTEXT PRIMARY KEY,
                {NAME} SMALLTEXT,
                {DESCRIPTION} TEXT,
                {MANUFACTURER} SMALLTEXT,
                {YEAR} SMALLINT,
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
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = car.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def getCar(self, carID: str) -> Car:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE ID = ?"
            params = (carID, )
            cursor.execute(query, params)
            return Car.new(cursor.fetchone())
        
    def getCarsInClass(self, carClass: str) -> list[Car]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {CLASS} = ?"
            params = (carClass, )
            cursor.execute(query, params)
            return [Car.new(car) for car in cursor.fetchall()]
    
    def getCars(self) -> list[Car]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Car.new(car) for car in cursor.fetchall()]
    
    def updateCar(self, car: Car):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""
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
                {MAXWEIGHTUPGRADES},
                {BASEDRAG},
                {DRAGUPGRADESIZE},
                {MAXDRAGUPGRADES})
                = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                WHERE ID = ?
            """
            params = car.toTuple() + (car.ID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def deleteCar(self, carID: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {ID} = ?"
            params = (carID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()