from discordLogger import DiscordLogger
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

        self.databaseConnection = databaseConnection

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
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {str(sponsor.toTuple())}")

    def getSponsor(self, sponsorID: int):

        with closing(self.databaseConnection.cursor) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {ID} = {sponsorID}")
        return Sponsor(cursor.fetchone())

    def getSponsors(self) -> list[Sponsor]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return list(map(Sponsor, cursor.fetchall()))

    def updateSponsor(self, sponsor: Sponsor):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                UPDATE {TABLENAME}
                SET ({ID}, {NAME}, {CONTRACTLENGTH}, {SIGNINGPAY}, {RACEPAY}) = {str(sponsor.toTuple())}
                WHERE {ID} = {sponsor.id}
            """)
    
    def deleteSponsor(self, sponsorID: int):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"DELETE FROM {TABLENAME} WHERE {ID} = {sponsorID}")