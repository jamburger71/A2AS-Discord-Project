from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.primarySponsor import PrimarySponsor

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

        self.databaseConnection = databaseConnection
        
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
            cursor.execute(f"INSERT INTO {TABLENAME} VALUES {str(sponsor.toTuple())}")

    def getSponsor(self, sponsorID: int):

        with closing(self.databaseConnection.cursor) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME} WHERE {ID} = {sponsorID}")
        return PrimarySponsor(cursor.fetchone())

    def getSponsors(self) -> list[PrimarySponsor]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM {TABLENAME}")
            return list(map(PrimarySponsor, cursor.fetchall()))

    def updateSponsor(self, sponsor: PrimarySponsor):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                UPDATE {TABLENAME}
                SET ({ID}, {NAME}, {CONTRACTLENGTH}, {SIGNINGPAY}, {RACEPAY}, {TARGET}, {TARGETTYPE}, {TARGETREWARD}) = {str(sponsor.toTuple())}
                WHERE {ID} = {sponsor.id}
            """)
    
    def deleteSponsor(self, sponsorID: int):
        
        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"DELETE FROM {TABLENAME} WHERE {ID} = {sponsorID}")