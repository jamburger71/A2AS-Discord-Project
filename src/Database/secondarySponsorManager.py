  
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.sponsor import Sponsor

TABLENAME = "SecondarySponsorData"
ID = "ID"
NAME = "Name"
CONTRACTLENGTH = "ContractLength"
SIGNINGPAY = "SigningPay"
RACEPAY = "RacePay"


class SecondarySponsorManager:

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
            )""")

    def insertSponsor(self, sponsor: Sponsor):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"INSERT INTO {TABLENAME} VALUES (?, ?, ?, ?, ?)"
            params = sponsor.toTuple()
            cursor.execute(query, params)

    def getSponsor(self, sponsorID: int):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"SELECT * FROM {TABLENAME} WHERE {ID} = ?"
            params = (sponsorID, )
            cursor.execute(query, params)
        return Sponsor(cursor.fetchone())

    def getSponsors(self) -> list[Sponsor]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return [Sponsor(sponsor) for sponsor in cursor.fetchall()]

    def updateSponsor(self, sponsor: Sponsor):

        with closing(self.databaseConnection.cursor()) as cursor:
            query = f"""UPDATE {TABLENAME}
                SET ({ID}, {NAME}, {CONTRACTLENGTH}, {SIGNINGPAY}, {RACEPAY})
                = (?, ?, ?, ?, ?)
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