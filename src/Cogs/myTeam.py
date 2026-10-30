import dis
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
from Classes.sponsor import Sponsor
from Classes.primarySponsor import PrimarySponsor

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
        
        myTeamEmbed = discord.Embed(
            title = team.name,
            description = f"Races entered: {}"
        )
        await interaction.response.send_message(embed = MyTeamEmbed(team, self.bot), view = MyTeamView(team, self.bot))
        
        logging.info(f"Team found for user {interaction.user.id}: {team.name} (ID: {team.id})")

class MyTeamEmbed(discord.Embed):

    def __init__(self, team: Team, bot):

        super().__init__(title = team.name)

        carText = "No Car"
        if team.car != "":
            car: Car = bot.carManager.getCar(team.car)
            carText = f"Car: {car.manufacturer} {car.name}"
        
        engineText = "No Engine"
        if team.engine != "":
            engine: Engine = bot.engineManager.getEngine(team.engine)
            engineText = f"Engine: {engine.manufacturer} {engine.model}\nPower: {engine.power}hp\nReliability: {engine.reliability}/100"
            
        carSection = discord.ui.Section(
            discord.ui.TextDisplay("## Car"),
            discord.ui.TextDisplay(carText),
            discord.ui.TextDisplay(engineText),
            accessory = manageCarButton(team)
        )

        teamDriver1Text = "No Driver Signed"
        if team.driverOne != "":
            teamDriver1 = bot.driverManager.getDriver(team.driverOne)
            teamDriver1Text = f"{teamDriver1.firstName} {teamDriver1.lastName} (Points: N/A)"

        teamDriver2Text = "No Driver Signed"
        if team.driverTwo != "":
            teamDriver2 = bot.driverManager.getDriver(team.driverTwo)
            teamDriver2Text = f"{teamDriver2.firstName} {teamDriver2.lastName} (Points: N/A)"
            
        driverSection = discord.ui.Section(
            discord.ui.TextDisplay("# Drivers"),
            discord.ui.TextDisplay(teamDriver1Text),
            discord.ui.TextDisplay(teamDriver2Text),
            accessory = manageDriversButton(team)
        )

        primarySponsorText = "### No Primary Sponsor"
        if team.primarySponsor != "":
            primarySponsor: PrimarySponsor = bot.primarySponsorManager.getSponsor(team.primarySponsor)
            primarySponsorText = f"### {primarySponsor.name}\nRace Payout: £{primarySponsor.racePay}\nBonus Requirement: {primarySponsor.target}\nBonus Payout: £{primarySponsor.targetReward}"

        secondary1text = "### No Secondary Sponsor 1"
        if team.secondarySponsor1 != "":
            secondarySponsor1: Sponsor = bot.secondarySponsorManager.getSponsor(team.secondarySponsor1)
            secondary1text = f"### {secondarySponsor1.name}\nRace Payout: £{secondarySponsor1.racePay}"

        secondary2text = "### No Secondary Sponsor 2"
        if team.secondarySponsor2 != "":
            secondarySponsor2: Sponsor = bot.secondarySponsorManager.getSponsor(team.secondarySponsor2)
            secondary2text = f"### {secondarySponsor2.name}\nRace Payout: £{secondarySponsor2.racePay}"

        secondary3text = "### No Secondary Sponsor 3"
        if team.secondarySponsor3 != "":
            secondarySponsor3: Sponsor = bot.secondarySponsorManager.getSponsor(team.secondarySponsor3)
            secondary3text = f"### {secondarySponsor3.name}\nRace Payout: £{secondarySponsor3.racePay}"
            
        sponsorText = f"{primarySponsorText}\n{secondary1text}\n{secondary2text}\n{secondary3text}"
        financeSection = discord.ui.Section(
            discord.ui.TextDisplay("## Finances"),
            discord.ui.TextDisplay(f"Current Funds: £{team.currentFunds}"),
            discord.ui.TextDisplay(sponsorText),
            accessory = manageSponsorsButton(team)
        )

        teamSection = discord.ui.Section(
            discord.ui.TextDisplay("## Team Details"),
            discord.ui.TextDisplay(f"Owned by {bot.get_user(team.ownerID).name}"),
            accessory = manageTeamButton(team)
        )

class MyTeamView(discord.ui.View):

    def __init__(self, team: Team, bot):

        super().__init__()

        self.add_item(manageTeamButton(team))
        self.add_item(manageDriversButton(team))
        self.add_item(manageCarButton(team))
        self.add_item(manageSponsorsButton(team))
        
    
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

class manageTeamButton(discord.ui.Button):

    def __init__(self, team: Team):

        super().__init__(label = "Manage Team")

    async def callback(self, interaction: discord.Interaction):

        return

class manageTeamView()

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    logging.info("Loading MyTeam cog...")
    await bot.add_cog(MyTeam(bot))