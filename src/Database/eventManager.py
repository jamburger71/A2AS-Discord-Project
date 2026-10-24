import logging
import sqlite3
import yaml
import os
from contextlib import closing

from classes.event import Event

class EventManager:

    def __init__(self, databaseConnection):

        self.DatabaseConnection = databaseConnection
    
    def getEventsForTeamOrDriver(self, ID: int):
        
        IDString = str(ID)
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                SELECT * FROM EventRounds
                WHERE QualiResults LIKE *{IDString}*""")
            return cursor.fetchall()
    
    def checkIfEventExists(self, seasonNo, roundNo) -> bool:
        
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute(f"""SELECT 1 FROM EventRounds
                WHERE SeasonNo = {seasonNo}
                AND EventNo = {roundNo}""")
            return cursor.fetchOne != None
    
    def insertEvent(self, event: Event):
        
        try:
            with closing(self.DatabaseConnection.cursor()) as cursor:
                cursor.execute("""
                    INSERT INTO EventRounds
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, event.toTuple())
                cursor.fetchall()
        except Exception as e:
            return e
    
    def updateEvent(
        self,
        seasonNo: int,
        roundNo: int,
        eventTitle: int | None,
        eventDate: int | None,
        weather: str | None,
        qualiDuration: int | None,
        qualiResults: str | None,
        raceLength: int | None,
        raceResults: str | None
    ):
        
        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                UPDATE EventData
                SET 
                EventTitle = COALESCE(?, EventTitle),
                EventDate = COALESCE(?, EventDate),
                Weather = COALESCE(?, Weather),
                QualiDuration = COALESCE(?, QualiDuration),
                QualiResults = COALESCE(?, QualiResults),
                RaceLength = COALESCE(?, RaceLength),
                RaceResults = COALESCE(?, RaceResults)
                WHERE SeasonNo = ? AND RoundNo = ?""",
                (eventTitle, eventDate, weather, qualiDuration, qualiResults, raceLength, raceResults, seasonNo, roundNo))
            cursor.commit()

    def deleteEvent(self, roundNo, seasonNo):

        with closing(self.DatabaseConnection.cursor()) as cursor:
            cursor.execute("""
                DELETE FROM EventData
                WHERE RoundNo = ? 
                AND SeasonNo = ?""", 
                (roundNo, seasonNo))
            cursor.commit()