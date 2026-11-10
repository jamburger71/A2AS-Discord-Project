from discord.app_commands import describe
import enums
import dis
import discord
from discord import app_commands
from discord.ext import commands
import logging
  

from Classes.driver import Driver
from Classes.team import Team
from Classes.myBot import MyBot
from Classes.season import Season
from Classes.event import Event
from areyousure import AreYouSure
from enums import keyVals
from helpers import ordinalConv

class CurrentStandings(commands.Cog):

    def __init__(self, bot: MyBot):  
        self.bot = bot

    async def cog_load(self):
        logging.info("CurrentStandings cog loaded successfully.")

    @app_commands.command(name="currentstandings")
    async def currentstandings(self, interaction: discord.Interaction):

        seasonNo = self.bot.keyValManager.getKeyVal("CurrentSeason")
        roundNo = self.bot.keyValManager.getKeyVal("CurrentRound")
        currentSeason: Season = self.bot.seasonManager.getSeason(seasonNo)
        lastEvent: Event = self.bot.eventManager.getEvent(seasonNo, roundNo-1)
        allDrivers = self.bot.driverManager.getDrivers()
        allTeams: list[Team] = self.bot.teamManager.getTeams()
        seasonResults = self.bot.resultManager.getResultsForSeason(seasonNo)
        
        driverPosField = ""
        driverNamesField = ""
        driverPointsField = ""
        teamPosField = ""
        teamNamesField = ""
        teamPointsField = ""
        driverPointsList: list[list] = [[]]
        teamPointsList: list[list] = [[]]
        for driver in allDrivers:
            driverResults = self.bot.resultManager.getSeasonResultsForDriver(driver.ID, seasonNo)
            driverTeam = self.bot.teamManager.getTeamByDriver(driver.ID)
            if driverTeam is not None or driverResults is not []:
                driverPoints = sum([result.getPoints(currentSeason) for result in driverResults])
                driverPointsList.append([driver, driverPoints])
                driverNamesField += f"{driver.firstName} {driver.lastName}\n"
                driverPointsField += f"{driverPoints}\n"
        for team in allTeams:
            if team.isActive:
                teamResults = self.bot.resultManager.getSeasonResultsForTeam(team.ID, seasonNo)
                teamPoints = sum([result.getPoints(seasonNo) for result in teamResults])
                teamPointsList.append([team, teamPoints])
                teamNamesField += f"{team.name}\n"
                teamPointsField += f"{teamPoints}\n"
        for pos in range(len(driverPointsList)):
            driverPosField += f"{ordinalConv(pos+1)}\n"
        for pos in range(len(teamPointsList)):
            teamPosField += f"{ordinalConv(pos+1)}\n"
        driverPointsList.sort(key = lambda x: x[1], reverse=True)
        teamPointsList.sort(key = lambda x: x[1], reverse=True)
        driverStandingsEmbed = discord.Embed(
            title = "Drivers' Standings",
            description = "Rounds completed: {len(events)}"
        )
        driverStandingsEmbed.add_field(
            name = "Pos",
            value = driverPosField
        )
        driverStandingsEmbed.add_field(
            name = "Driver",
            value = driverNamesField
        )
        driverStandingsEmbed.add_field(
            name = "Points",
            value = driverPointsField
        )

        teamStandingsEmbed = discord.Embed(
            title = "Constructors' Standings",
            description = f"After the {lastEvent.title})"
        )
        teamStandingsEmbed.add_field(
            name = "Pos",
            value = teamPosField
        )
        teamStandingsEmbed.add_field(
            name = "Team",
            value = teamNamesField
        )
        teamStandingsEmbed.add_field(
            name = "Points",
            value = teamPointsField
        )
        
        await interaction.response.send_message(embeds = [driverStandingsEmbed, teamStandingsEmbed])
            
async def setup(bot: MyBot):  
    print(f"Loading {CurrentStandings.__name__} cog...")
    await bot.add_cog(CurrentStandings(bot))