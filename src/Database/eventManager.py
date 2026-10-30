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

class EventManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection
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
                PRIMARY KEY({SEASONNO}, {ROUNDNO}))
            """)
            
    def insertEvent(self, event: Event):
            
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                INSERT INTO {TABLENAME}
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, event.toTuple())
            cursor.commit()
    
    def getEvent(self, seasonNo: int, roundNo: int) -> Event:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT 1 FROM {TABLENAME}
                WHERE {SEASONNO}  = {seasonNo}
                AND {ROUNDNO} = {roundNo}""")
            return Event(cursor.fetchone())
    
    def getEventsFromSeason(self, seasonNo: int) -> list[Event]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM {TABLENAME}
                WHERE {SEASONNO} = {seasonNo}
            """)
            return list(map(Event, cursor.fetchall()))
    
    def getEvents(self) -> list[Event]:
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return list(map(Event, cursor.fetchall()))
    
    def updateEvent(self, event: Event):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                UPDATE {TABLENAME}
                SET 
                {SEASONNO} = {event.seasonNo},
                {ROUNDNO} = {event.roundNo},
                {TITLE} = {event.title},
                {DATE} = {event.date},
                {WEATHER} = {event.weather},
                {QUALIDURATION} = {event.qualiDuration},
                {RACELENGTH} = {event.raceLength},
                WHERE {SEASONNO} = {event.seasonNo} 
                AND {ROUNDNO} = {event.roundNo}""")
            cursor.commit()

    def deleteEvent(self, roundNo, seasonNo):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                DELETE FROM {TABLENAME}
                WHERE {SEASONNO} = {seasonNo}
                AND {ROUNDNO} = {roundNo}""", 
                (roundNo, seasonNo))
            cursor.commit()