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
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {str(carClass.toTuple())}")
    
    def getCarClass(self, classID: int):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {ID} = {classID} LIMIT 1")
            return CarClass(cursor.fetchone())