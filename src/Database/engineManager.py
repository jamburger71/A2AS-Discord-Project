from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.engine import Engine

DATABASE_NAME = "EngineData"
MODEL = "Model"
MANUFACTURER = "Manufacturer"
YEAR = "Year"
POWER = "Power"
RELIABILITY = "Reliability"
PRICE = "Price"

class EngineManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {DATABASE_NAME} (
                {MODEL} SMALLTEXT PRIMARY KEY,
                {MANUFACTURER} SMALLTEXT,
                {YEAR} TINYTEXT,
                {POWER} TINYINT,
                {RELIABILITY} TINYINT,
                {PRICE} INT)
            """)

    def insertEngine(self, engine: Engine):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""INSERT INTO {DATABASE_NAME} VALUES ({engine.toTuple()})
            """)
    
    def updateEngine(self, engine: Engine):
        
        with closing(self.databaseConnection.cursor) as cursor:
            cursor.execute(f"""
                UPDATE {DATABASE_NAME}
                SET 
                {MODEL} = {engine.model},
                {MANUFACTURER} = {engine.manufacturer},
                {YEAR} = {engine.year},
                {POWER} = {engine.power},
                {RELIABILITY} = {engine.reliability},
                {PRICE} = {engine.price}
                WHERE {MODEL} = {engine.model}
            """)
            self.databaseConnection.commit()
    
    def getEngine(self, engineModel: str) -> Engine:
        
        with closing(self.databaseConnection.cursor) as cursor:
            cursor.execute(f"SELECT 1 FROM {DATABASE_NAME} WHERE {MODEL} = {engineModel}")
            return Engine(cursor.fetchone())
    
    def getEnginesForYear(self, year: str) -> list[Engine]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {DATABASE_NAME} WHERE {YEAR} = {year}")
            return list(map(Engine, cursor.fetchall()))
    
    def getEngines(self) -> list[Engine]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {DATABASE_NAME}")
            return list(map(Engine, cursor.fetchall()))
    
    def deleteEngine(self, engineModel: str):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"REMOVE FROM {DATABASE_NAME} WHERE {MODEL} = {engineModel}")
            cursor.commit()