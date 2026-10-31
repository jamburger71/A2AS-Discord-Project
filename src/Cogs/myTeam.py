from discord.app_commands import describe

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
from Classes.result import Result
from Classes.season import Season

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
            
        def filterWins(result: Result):
            return result.racePosition == 1
            
        def filterPodiums(result: Result):
            return result.racePosition >= 3
            
        teamResults = self.bot.resultManager.getAllResultsForTeam(team.id)
        myTeamEmbed = discord.Embed(
            title = team.name,
            description = f"Entries: {len(teamResults)}\nWins: {len(teamResults.filter(filterWins))}\nPodiums: {len(teamResults.filter(filterPodiums))}"
        )

        carText = "No Car"
        if team.car != "":
            car: Car = self.bot.carManager.getCar(team.car)
            carText = f"{car.manufacturer} {car.name}"
            
        engineText = "No Engine"
        if team.engine != "":
            engine: Engine = self.bot.engineManager.getEngine(team.engine)
            engineText = f"{engine.manufacturer} {engine.model}"
            
        myTeamEmbed.add_field(
            name = "Car", 
            value = f"Chassis: {carText}\nEngine: {engineText}\nUpgrades: Drag({team.dragUpgrades}), Weight({team.weightUpgrades})"
        )

        teamDriver1Text = "No Driver Signed"
        if team.driverOne != "":
            teamDriver1 = self.bot.driverManager.getDriver(team.driverOne)
            teamDriver1Text = f"{teamDriver1.firstName} {teamDriver1.lastName} (Points: N/A)"

        teamDriver2Text = "No Driver Signed"
        if team.driverTwo != "":
            teamDriver2 = self.bot.driverManager.getDriver(team.driverTwo)
            teamDriver2Text = f"{teamDriver2.firstName} {teamDriver2.lastName} (Points: N/A)"

        myTeamEmbed.add_field(
            name = "Drivers",
            value = f"Driver 1: {teamDriver1Text}\nDriver 2: {teamDriver2Text}"
        )

        primarySponsorText = "No Primary Sponsor"
        if team.primarySponsor != "":
            primarySponsor: PrimarySponsor = self.bot.primarySponsorManager.getSponsor(team.primarySponsor)
            primarySponsorText = f"{primarySponsor.name}\n    Race Payout: £{primarySponsor.racePay}\n    Bonus Requirement: {primarySponsor.target}\n    Bonus Payout: £{primarySponsor.targetReward}"

        secondary1text = "No Secondary Sponsor 1"
        if team.secondarySponsor1 != "":
            secondarySponsor1: Sponsor = self.bot.secondarySponsorManager.getSponsor(team.secondarySponsor1)
            secondary1text = f"{secondarySponsor1.name}\n    Race Payout: £{secondarySponsor1.racePay}"

        secondary2text = "No Secondary Sponsor 2"
        if team.secondarySponsor2 != "":
            secondarySponsor2: Sponsor = self.bot.secondarySponsorManager.getSponsor(team.secondarySponsor2)
            secondary2text = f"{secondarySponsor2.name}\n    Race Payout: £{secondarySponsor2.racePay}"

        secondary3text = "No Secondary Sponsor 3"
        if team.secondarySponsor3 != "":
            secondarySponsor3: Sponsor = self.bot.secondarySponsorManager.getSponsor(team.secondarySponsor3)
            secondary3text = f"{secondarySponsor3.name}\n    Race Payout: £{secondarySponsor3.racePay}"
            
        myTeamEmbed.add_field(
            name = "Finances",
            value = f"Current Funds: {team.currentFunds}\nPrimary Sponsor: {primarySponsorText}\nSecondary Sponsor 1: {secondary1text}/n Secondary Sponsor 2: {secondary2text}\nSecondary Sponsor 3: {secondary3text}"
        )

        myTeamView = discord.ui.View(timeout=300)
        myTeamView.add_item(manageTeamButton(team))
        myTeamView.add_item(manageDriversButton(self.bot, team, teamDriver1, teamDriver2))
        myTeamView.add_item(manageCarButton(team))
        myTeamView.add_item(manageSponsorsButton(team))
        
        await interaction.response.send_message(embed = myTeamEmbed, view = myTeamView)
        
        logging.info(f"Team found for user {interaction.user.id}: {team.name} (ID: {team.id})")
        
    
class manageDriversButton(discord.ui.Button):

    def __init__(self, bot, team: Team, driver1: Driver | None, driver2: Driver | None):

        super().__init__(label = "Manage Drivers")
        self.bot = bot
        self.team = team
        self.driver1 = driver1
        self.driver2 = driver2

    async def callback(self, interaction: discord.Interaction):

        driversEmbed = discord.Embed(
            title = "Manage Drivers",
            description = "Hire, fire and check your driver stats here."
        )
        currentSeason: Season = self.bot.seasonManager.getCurrentSeason()
        seasonResults = self.bot.resultsManager.getResultsForSeason(currentSeason.seasonNo)
        seasonStandings = helpers.getCurrentStandings(seasonResults, currentSeason.pointsModel, currentSeason.pointForPole)
        if self.driver1 is not None:
            driver1position = helpers.ordinalConv(seasonStandings.index(self.driver1.ID)+1)
            driver1points = seasonStandings[self.driver1.ID]
            driversEmbed.add_field(
                name = f"{self.driver1.firstName} {self.driver1.lastName}",
                value = f"""
                Age: {self.driver1.age}
                Nationality: {self.driver1.nationality}
                Current Position: {driver1position} (Points: {driver1points})
                ### Stats:
                Qualifying Pace: {self.driver1.qualiPace}
                Race Pace: {self.driver1.racePace}
                Wet Weather Pace: {self.driver1.wetPace}
                Tyre Management: {self.driver1.tyreManagement}
                Aggressiveness: {self.driver1.aggressiveness}
                Defending: {self.driver1.defending}
                ### Contract:
                Cost: £{self.driver1.contractCost}/Season
                Expires: Who knows """
            )
        else:
            driversEmbed.add_field(
                name = "No Driver Signed",
                value = "You can hire one with the button below."
            )
        if self.driver2 is not None:
            driver2position = helpers.ordinalConv(seasonStandings.index(self.driver2.ID)+1)
            driver2points = seasonStandings[self.driver2.ID]
            driversEmbed.add_field(
                name = f"{self.driver2.firstName} {self.driver2.lastName}",
                value = f"""
                Age: {self.driver2.age}
                Nationality: {self.driver2.nationality}
                Current Position: {driver2position} (Points: {driver2points})
                ### Stats:
                Qualifying Pace: {self.driver2.qualiPace}
                Race Pace: {self.driver2.racePace}
                Wet Weather Pace: {self.driver2.wetPace}
                Tyre Management: {self.driver2.tyreManagement}
                Aggressiveness: {self.driver2.aggressiveness}
                Defending: {self.driver2.defending}
                ### Contract:
                Cost: £{self.driver2.contractCost}/Season
                Expires: Who knows """
            )
        else:
            driversEmbed.add_field(
                name = "No Driver Signed",
                value = "You can hire one with the button below."
            )

        driversView = discord.ui.View(300)
        

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

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    logging.info("Loading MyTeam cog...")
    await bot.add_cog(MyTeam(bot))