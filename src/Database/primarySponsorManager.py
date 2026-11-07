  
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.primarySponsor import PrimarySponsor
from Classes.sponsor import Sponsor

TABLENAME = "PrimarySponsorData"
ID = "ID"
NAME = "Name"
CONTRACTLENGTH = "ContractLength"
SIGNINGPAY = "SigningPay"
RACEPAY = "RacePay"
TARGET = "Target"
TARGETTYPE = "TargetType"
TARGETREWARD = "TargetReward"


class PrimarySponsorManager:

    def __init__(self, databaseConnection):

        self.databaseConnection: sqlite3.Connection = databaseConnection
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLENAME} (
            {ID} SMALLINT PRIMARY KEY,
            {NAME} SMALLTEXT,
            {CONTRACTLENGTH} TINYINT,
            {SIGNINGPAY} INT,
            {RACEPAY} INT
            {TARGET} SMALLINT,
            {TARGETTYPE} TINYINT,
            {TARGETREWARD} INT
            )""")

    def insertSponsor(self, sponsor: PrimarySponsor):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            params = sponsor.toTuple()
            cursor.execute(query, params)
            self.databaseConnection.commit()

    def getSponsor(self, sponsorID: int) -> Sponsor:

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {ID} = ?"
            params = (sponsorID, )
            cursor.execute(query, params)
            return PrimarySponsor(cursor.fetchone())

    def getSponsors(self) -> list[PrimarySponsor]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [PrimarySponsor(sponsor) for sponsor in cursor.fetchall()]

    def updateSponsor(self, sponsor: PrimarySponsor):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""
                UPDATE {TABLENAME}
                SET ({ID}, {NAME}, {CONTRACTLENGTH}, {SIGNINGPAY}, {RACEPAY}, {TARGET}, {TARGETTYPE}, {TARGETREWARD}) 
                = (?, ?, ?, ?, ?, ?, ?, ?)
                WHERE {ID} = ?
            """
            params = sponsor.toTuple() + (sponsor.id, )
            cursor.execute(query, params)
            self.databaseConnection.commit()
    
    def deleteSponsor(self, sponsorID: int):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"DELETE FROM {TABLENAME} WHERE {ID} = ?"
            params = (sponsorID, )
            cursor.execute(query, params)
            self.databaseConnection.commit()