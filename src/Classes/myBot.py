from dotenv import load_dotenv
import logging
import os
import discord
from discord import app_commands
from discord.ext import commands
from pathlib import Path

from Database.databaseManager import DatabaseManager
from Database.carClassManager import CarClassManager
from Database.carManager import CarManager
from Database.driverManager import DriverManager
from Database.engineManager import EngineManager
from Database.eventManager import EventManager
from Database.keyValManager import KeyValManager
from Database.teamManager import TeamManager
from Database.primarySponsorManager import PrimarySponsorManager
from Database.resultManager import ResultManager
from Database.seasonManager import SeasonManager
from Database.secondarySponsorManager import SecondarySponsorManager
from Database.trackLayoutManager import TrackLayoutManager
from Database.trackManager import TrackManager

logHandler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode='w')

class MyBot(commands.Bot):

    def __init__(self):

        load_dotenv()

        intents = discord.Intents.all()
        super().__init__(command_prefix="/", description="A2AS Personal Assistant", intents=intents)

        self.databaseManager = DatabaseManager(databaseName=os.getenv("DB_NAME"+".db") or "GenericDB.db")
        self.databaseConnection = self.databaseManager.databaseConnection
        self.carClassManager = CarClassManager(self.databaseConnection)
        self.carManager = CarManager(self.databaseConnection)
        self.driverManager = DriverManager(self.databaseConnection)
        self.engineManager = EngineManager(self.databaseConnection)
        self.eventManager = EventManager(self.databaseConnection)
        self.keyValManager = KeyValManager(self.databaseConnection)
        self.primarySponsorManager = PrimarySponsorManager(self.databaseConnection)
        self.resultManager = ResultManager(self.databaseConnection)
        self.seasonManager = SeasonManager(self.databaseConnection)
        self.secondarySponsorManager = SecondarySponsorManager(self.databaseConnection)
        self.teamManager = TeamManager(self.databaseConnection)
        self.trackLayoutManager = TrackLayoutManager(self.databaseConnection)
        self.trackManager = TrackManager(self.databaseConnection)

    async def setup_hook(self):

        cogsDirectory = Path(__file__).resolve().parent / "Cogs"
        logging.info(f"Loading cogs from {cogsDirectory.resolve()}")
        print(f"Loading cogs from {cogsDirectory.resolve()}")
        for root, _, files in os.walk(cogsDirectory):
            for filename in files:
                print(f"Checking file: {filename}")
                if filename.endswith(".py") and not filename.startswith("__"):
                    
                    filePath = Path(os.path.join(root, filename))
                    relativePath = filePath.relative_to(cogsDirectory.parent)
                    extensionPath = ".".join(relativePath.with_suffix("").parts)
                    try:
                        await self.load_extension(extensionPath)
                        print(f"Loaded cog: {filename}")
                        logging.info(f"Loaded cog: {filename}")
                    except Exception as e:
                        logging.error(f"Failed to load cog {filename}: {e}")
                else:
                    print(f"Skipping file: {filename}.")
                    logging.info(f"Skipping file: {filename}.")

        synced = await self.tree.sync()
        logging.info(f"Synced {len(synced)} command(s).")
        print(f"Synced {len(synced)} command(s).")
