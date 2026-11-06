import discord
from discord import app_commands
from discord.ext import commands
import logging
  

from Classes.driver import Driver
from Classes.team import Team
from Classes.myBot import MyBot
from areyousure import AreYouSure
from enums import keyVals

class CurrentStandings(commands.Cog):

    def __init__(self, bot: MyBot):  
        self.bot = bot

    async def cog_load(self):
        logging.info("CurrentStandings cog loaded successfully.")

    @app_commands.command(name="currentstandings")
    async def currentstandings(self, interaction: discord.Interaction):

        currentSeason = self.bot.keyValManager.getKeyVal("CurrentSeason")
        allTeams = self.bot.teamManager.getTeams()
        allDrivers: list[Driver] = []
        for team in allTeams:
            driverOne = self.bot.driverManager.getDriver(team.driverOne)
            driverTwo = self.bot.driverManager.getDriver(team.driverTwo)
            if driverOne is not None: allDrivers.append(driverOne)
            if driverTwo is not None: allDrivers.append(driverTwo)
            
        driverStandingsEmbed = discord.Embed(
            title = "Drivers' Standings",
            description = "Rounds completed: {len(events)}"
        )

async def setup(bot: MyBot):  
    print(f"Loading {CurrentStandings.__name__} cog...")
    await bot.add_cog(CurrentStandings(bot))