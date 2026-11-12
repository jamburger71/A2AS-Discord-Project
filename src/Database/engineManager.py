  
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

        self.databaseConnection: sqlite3.Connection = databaseConnection
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {DATABASE_NAME} (
                {MODEL} SMALLTEXT PRIMARY KEY,
                {MANUFACTURER} SMALLTEXT,
                {YEAR} SMALLINT,
                {POWER} TINYINT,
                {RELIABILITY} TINYINT,
                {PRICE} INT)
            """)

    def insertEngine(self, engine: Engine):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"INSERT INTO {DATABASE_NAME} VALUES (?, ?, ?, ?, ?, ?)"
            params = engine.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def updateEngine(self, engine: Engine):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""
                UPDATE {DATABASE_NAME}
                SET ({MODEL}, {MANUFACTURER}, {YEAR}, {POWER}, {RELIABILITY}, {PRICE})
                = (?, ?, ?, ?, ?, ?)
                WHERE {MODEL} = ?
            """
            params = engine.toTuple() + (engine.model, )
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def getEngine(self, engineModel: str) -> Engine:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {DATABASE_NAME} WHERE {MODEL} = ?"
            params = (engineModel, )
            cursor.execute(query, params)
            return Engine.new(cursor.fetchone())
    
    def getEnginesByYear(self, year: str) -> list[Engine]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {DATABASE_NAME} WHERE {YEAR} = ?"
            params = (year, )
            cursor.execute(query, params)
            return [Engine.new(engine) for engine in cursor.fetchall()]
    
    def getEngines(self) -> list[Engine]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {DATABASE_NAME}")
            return [Engine.new(engine) for engine in cursor.fetchall()]
    
    def deleteEngine(self, engineModel: str):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {DATABASE_NAME} WHERE {MODEL} = ?"
            params = (engineModel, )
            cursor.execute(query, params)
            self.databaseConnection.commit()