from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.car import Car

class CarManager:

    def __init__(self, databaseConnection):

        self.DatabaseConnection = databaseConnection

    def insertCar(self, car: Car):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO CarData
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, car.toTuple())

    def getCar(self, carID: int) -> Car:

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                SELECT * FROM CarData
                WHERE ID = ?
            """, carID)
            return Car(cursor.fetchone())
    
    def editCar(self, car: Car):

        with closing(self.DatabaseConnection.cursor()) as cursor:
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