import logging
import sqlite3
import yaml
import os
from contextlib import closing

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
    
    def insertEvent(
        self,
        seasonNo, 
        roundNo, 
        eventTitle, 
        eventDate,
        Weather,
        QualiDuration,
        QualiResults,
        RaceLength,
        RaceResults):
        
        try:
            with closing(self.DatabaseConnection.cursor()) as cursor:
                cursor.execute("""
                    INSERT INTO EventRounds
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, seasonNo, roundNo, eventTitle, eventDate, Weather, QualiDuration, QualiResults, RaceLength, RaceResults)
                cursor.fetchall()
        except Exception as e:
            return e
    
    def updateEvent(
        self,
        seasonNo: int,
        roundNo: int,
        eventTitle: int | None,
        eventDate: int | None,
        
    )