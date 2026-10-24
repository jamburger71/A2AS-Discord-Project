from discordLogger import DiscordLogger
import logging
import sqlite3
import yaml
import os
from contextlib import closing

from Classes.primarySponsor import PrimarySponsor

class PrimarySponsorManager:

    def __init__(self, databaseConnection):

        self.databaseConnection = databaseConnection

    def insertSponsor(self, sponsor: PrimarySponsor):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO PrimarySponsorData
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, sponsor.toTuple())

    def getSponsor(self, sponsorID: int):

        with closing(self.databaseConnection.cursor) as cursor:
            cursor.execute("""
                SELECT * FROM PrimarySponsorData
                WHERE ID = ?
            """, (sponsorID))
        return PrimarySponsor(cursor.fetchone())

    def getSponsors(self) -> list[PrimarySponsor]:

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute("""SELECT * FROM PrimarySponsorData""")
            return list(map(PrimarySponsor, cursor.fetchall()))

    def updateSponsor(self, sponsor: PrimarySponsor):

        with closing(self.databaseConnection.cursor()) as cursor:
            cursor.execute(f"""
                UPDATE PrimarySponsorData
                SET ()
                WHERE ID = {sponsor.id}
            """)