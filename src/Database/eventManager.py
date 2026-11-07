from ctypes.wintypes import POINT
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.event import Event

TABLENAME = "EventData"
SEASONNO = "SeasonNo"
ROUNDNO = "RoundNo"
TITLE = "Title"
DATE = "Date"
WEATHER = "Weather"
QUALIDURATION = "QualiDuration"
RACELENGTH = "RaceLength"
POLEPOINT = "PolePoint"
POINTSMODEL = "PointsModel"

class EventManager:

    def __init__(self, databaseConnection):

        self.databaseConnection: sqlite3.Connection = databaseConnection
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLENAME} (
                {SEASONNO} TINYINT,
                {ROUNDNO} TINYINT,
                {TITLE} TINYTEXT,
                {DATE} DATE,
                {WEATHER} TEXT,
                {QUALIDURATION} INT,
                {RACELENGTH} SMALLINT,
                {POLEPOINT} TINYINT,
                {POINTSMODEL} TINYINT,
                PRIMARY KEY({SEASONNO}, {ROUNDNO}))
            """)
            
    def insertEvent(self, event: Event):
            
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""
                INSERT INTO {TABLENAME}
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            params = event.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def getEvent(self, seasonNo: int, roundNo: int) -> Event:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT 1 FROM {TABLENAME} WHERE {SEASONNO}  = ? AND {ROUNDNO} = ?"
            params = (seasonNo, roundNo)
            cursor.execute(query, params)
            return Event(cursor.fetchone())
    
    def getEventsFromSeason(self, seasonNo: int) -> list[Event]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {SEASONNO} = ?"
            params = (seasonNo, )
            return [Event(event) for event in cursor.fetchall()]
    
    def getEvents(self) -> list[Event]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Event(event) for event in cursor.fetchall()]
    
    def updateEvent(self, event: Event):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""UPDATE {TABLENAME}
                SET ({SEASONNO}, {ROUNDNO}, {TITLE}, {DATE}, {WEATHER}, {QUALIDURATION}, {RACELENGTH}, {POLEPOINT}, {POINTSMODEL})
                = (?, ?, ?, ?, ?, ?, ?, ?, ?)
                WHERE {SEASONNO} = ?
                AND {ROUNDNO} = ?"""
            params = event.toTuple() + (event.seasonNo, event.roundNo)
            self.databaseConnection.commit()

    def deleteEvent(self, roundNo, seasonNo):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {SEASONNO} = ? AND {ROUNDNO} = ?"
            params = (roundNo, seasonNo)
            cursor.execute(query, params)
            self.databaseConnection.commit()