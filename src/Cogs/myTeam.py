from types import NoneType
import json
import discord
from discord import app_commands
from discord.ext import commands
import logging

import helpers
from Classes.team import Team
from Classes.driver import Driver
from Classes.car import Car
from Classes.engine import Engine

class MyTeam(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("MyTeam cog loaded successfully.")

    @app_commands.command(name="myteam")
    async def myteam(self, interaction: discord.Interaction):

        team: Team | None = self.bot.teamManager.getOwnerTeam(interaction.user.id)
        if team is None:
            logging.info(f"No team found for user {interaction.user.id}")
            await interaction.response.send_message("You don't own a team!")
            return

        await interaction.response.send_message(view = MyTeamView(team, self.bot))
        
        logging.info(f"Team found for user {interaction.user.id}: {team.name} (ID: {team.id})")

class MyTeamView(discord.ui.View):

    def __init__(self, team: Team, bot):

        super().__init__(timeout=300)

        car: Car | None = bot.carManager.getCar(team.car)
        carText = car.name if car is not None else "No car"
        engine: Engine | None = bot.engineManager.getEngine(team.engine)
        engineText = engine.model if engine is not None else "No engine"
        carSection = discord.ui.Section(
            discord.ui.TextDisplay("## Car"),
            discord.ui.TextDisplay(f"Current Car: {carText}"),
            discord.ui.TextDisplay(f"Current Engine: {engineText}"),
            accessory = manageCarButton(team)
        )
        
        driverText = []
        teamDriver1 = bot.driverManager.getDriver(team.driverOne)
        teamDriver2 = bot.driverManager.getDriver(team.driverTwo)
        for drNo, driver in enumerate([teamDriver1, teamDriver2]):
            if driver is not None:
                driverText[drNo] = f"## {teamDriver1.firstName} {teamDriver1.lastName}"
            else:
                driverText[drNo] = f"You have no {helpers.ordinalConv(drNo+1)} driver."
                
            
        driverSection = discord.ui.Section(
            discord.ui.TextDisplay("# Drivers"),
            discord.ui.TextDisplay(driverText[0]),
            discord.ui.TextDisplay(driverText[1]),
            accessory = manageDriversButton(team)
        )

        self.add_item(carSection)
        self.add_item(discord.ui.Separator())
        self.add_item(driverSection)
        self.add_item(discord.ui.Separator())

class manageDriversButton(discord.ui.Button):

    def __init__(self, team: Team):

        super().__init__(label = "Manage Drivers")
        self.team = team

    async def callback(self, interaction: discord.Interaction):

        return

class manageCarButton(discord.ui.Button):

    def __init__(self, team: Team):

        super().__init__(label = "Manage car")
        self.team = team

    async def callback(self, interaction: discord.Interaction):

        return

class manageSponsorsButton(discord.ui.Button):

    def __init__(self, team: Team):

        super().__init__(label = "Manage Sponsors")

    async def callback(self, interaction: discord.Interaction):

        return

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    logging.info("Loading MyTeam cog...")
    await bot.add_cog(MyTeam(bot))