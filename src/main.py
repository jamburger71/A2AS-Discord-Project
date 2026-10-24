import discord
from discord import app_commands
from discord.ext import commands
import logging
from pathlib import Path
import os
from dotenv import load_dotenv

from Database.databaseManager import DatabaseManager
from Database.driverManager import DriverManager
from Database.keyValManager import KeyValManager
from Database.teamManager import TeamManager
from Database.eventManager import EventManager
from Database.carManager import CarManager
from Database.primarySponsorManager import PrimarySponsorManager
from Database.secondarySponsorManager import SecondarySponsorManager

load_dotenv()

logHandler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode='w')

class MyBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.all()
        super().__init__(command_prefix="/", description="A2AS Personal Assistant", intents=intents)

        self.databaseManager = DatabaseManager(databaseName=os.getenv("DB_NAME"+".db") or "GenericDB.db")
        self.DatabaseConnection = self.databaseManager.DatabaseConnection
        self.driverManager = DriverManager(self.DatabaseConnection)
        self.teamManager = TeamManager(self.DatabaseConnection)
        self.eventManager = EventManager(self.DatabaseConnection)
        self.keyValManager = KeyValManager(self.DatabaseConnection)

    async def setup_hook(self):

        cogsDirectory = Path(__file__).resolve().parent / "Cogs"
        logging.info(f"Loading cogs from {cogsDirectory.resolve()}")
        print(f"Loading cogs from {cogsDirectory.resolve()}")
        for root, dirs, files in os.walk(cogsDirectory):
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

bot = MyBot()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    logging.error(f"An error occurred: {error}")
    if isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message("Command not found.")
    elif isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("You do not have permission to use this command.")
    else:
        await interaction.response.send_message(f"An unknown error occurred: {error}")

bot.run(os.getenv("DISCORD_BOT_TOKEN") or "No Token")