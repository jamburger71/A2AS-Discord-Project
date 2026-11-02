import discord
from discord import app_commands
from discord.ext import commands
import logging

from areyousure import AreYouSure
import enums
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
        myTeamView.add_item(manageTeamButton(self.bot, team))
        myTeamView.add_item(manageDriversButton(self.bot, team))
        myTeamView.add_item(manageCarButton(self.bot, team))
        myTeamView.add_item(manageSponsorsButton(self.bot, team))
        
        await interaction.response.send_message(embed = myTeamEmbed, view = myTeamView)
        
        logging.info(f"Team found for user {interaction.user.id}: {team.name} (ID: {team.id})")
        
    
class manageDriversButton(discord.ui.Button):

    def __init__(self, bot, team: Team):

        super().__init__(label = "Manage Drivers")
        self.bot = bot
        self.team = team

    async def callback(self, interaction: discord.Interaction):

        driversEmbed = discord.Embed(
            title = "Manage Drivers",
            description = "Hire, fire and check your driver stats here."
        )
        currentSeason: Season = self.bot.seasonManager.getCurrentSeason()
        seasonResults = self.bot.resultsManager.getResultsForSeason(currentSeason.seasonNo)
        seasonStandings: list[tuple] = helpers.getCurrentStandings(seasonResults, currentSeason.pointsModel, currentSeason.pointForPole)
        
        if self.team.driverOne is not -1:
            driver1 = self.bot.driverManager.getDriver(self.team.driverOne)
            for index, driver in enumerate(seasonStandings):
                if driver[0] == driver1.ID:
                    driver1position = helpers.ordinalConv(index+1)
                    driver1points = driver[1]
                    break
            driversEmbed.add_field(
                name = f"{driver1.firstName} {driver1.lastName}",
                value = f"""
                Age: {driver1.age}
                Nationality: {driver1.nationality}
                Current Position: {driver1position} (Points: {driver1points})
                ### Stats:
                Qualifying Pace: {driver1.qualiPace}
                Race Pace: {driver1.racePace}
                Wet Weather Pace: {driver1.wetPace}
                Tyre Management: {driver1.tyreManagement}
                Aggressiveness: {driver1.aggressiveness}
                Defending: {driver1.defending}
                ### Contract:
                Cost: £{driver1.contractCost}/Season
                Expires: End Of Season"""
            )
        else:
            driversEmbed.add_field(
                name = "No Driver Signed",
                value = "You can hire one with the button below."
            )
        if self.team.driverTwo is not -1:
            driver2 = self.bot.driverManager.getDriver(self.team.driverTwo)
            for index, driver in enumerate(seasonStandings):
                if driver[0] == driver2.ID:
                    driver2position = helpers.ordinalConv(index+1)
                    driver2points = driver[1]
                    break
            driversEmbed.add_field(
                name = f"{driver2.firstName} {driver2.lastName}",
                value = f"""
                Age: {driver2.age}
                Nationality: {driver2.nationality}
                Current Position: {driver2position} (Points: {driver2points})
                ### Stats:
                Qualifying Pace: {driver2.qualiPace}
                Race Pace: {driver2.racePace}
                Wet Weather Pace: {driver2.wetPace}
                Tyre Management: {driver2.tyreManagement}
                Aggressiveness: {driver2.aggressiveness}
                Defending: {driver2.defending}
                ### Contract:
                Cost: £{driver2.contractCost}/Season
                Expires: End Of Season"""
            )
        else:
            driversEmbed.add_field(
                name = "No Driver Signed",
                value = "You can hire one with the button below."
            )

        driversView = discord.ui.View(timeout = 300)

class manageCarButton(discord.ui.Button):

    def __init__(self, bot, team: Team):

        super().__init__(label = "Manage car")
        self.bot = bot
        self.team = team

    async def callback(self, interaction: discord.Interaction):

        return

class manageSponsorsButton(discord.ui.Button):

    def __init__(self, bot, team: Team):

        super().__init__(label = "Manage Sponsors")
        self.bot = bot
        self.team = team

    async def callback(self, interaction: discord.Interaction):

        return

class manageTeamButton(discord.ui.Button):

    def __init__(self, bot, team: Team):

        super().__init__(label = "Manage Team")
        self.bot = bot
        self.team = team

    async def callback(self, interaction: discord.Interaction):

        return

class hireDriverButton(discord.ui.Button):

    def __init__(self, driverSlot: int, team: Team, bot):

        super().__init__(label = f"Hire Driver for Slot {driverSlot}")
        self.driverSlot = driverSlot
        self.team = team
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):

        return

class fireDriverButton(discord.ui.Button):

    def __init__(self, driverSlot: int, team: Team, driver: Driver, bot):

        super().__init__(label = f"Fire {driver.firstName} {driver.lastName}")
        self.driverSlot = driverSlot
        self.team = team
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(view = AreYouSure(fireDriver, dontFireDriver))

    def fireDriver(self):

        if self.driverSlot == 1:
            self.team.driverOne = -1
        else:
            self.team.driverTwo = -1
        self.bot.teamManager.updateTeam(self.team)

    def dontFireDriver(self):

        return

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    logging.info("Loading MyTeam cog...")
    await bot.add_cog(MyTeam(bot))