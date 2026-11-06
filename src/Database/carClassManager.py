from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.carClass import CarClass

TABLENAME = "CarClassData"
ID = "ID"
NAME = "Name"
DESCRIPTION = "Description"

class CarClassManager:
    
    def __init__(self, databaseConnection):
        
        self.databaseConnection = databaseConnection
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {ID} SMALLTEXT PRIMARY KEY,
                {NAME} SMALLTEXT,
                {DESCRIPTION} TEXT
            )""")
        
    def insertCarClass(self, carClass: CarClass):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?)"
            params = carClass.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def getCarClass(self, classID: str) -> CarClass | None:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {ID} = ?"
            params = (classID, )
            cursor.execute(query, params)
            return CarClass.new(cursor.fetchone())

    def updateCarClass(self, carClass: CarClass):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"UPDATE {TABLENAME} SET ({ID}, {NAME}, {DESCRIPTION}) = (?, ?, ?) WHERE {ID} = ?"
            params = carClass.toTuple() + (carClass.id, )
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def getCarClasses(self) -> list[CarClass | None]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [CarClass.new(carClass) for carClass in cursor.fetchall()]

    def deleteCarClass(self, classID: str):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {ID} = ?"
            params = (classID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()