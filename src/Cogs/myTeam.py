
import discord
from discord import app_commands
from discord.ext import commands
import logging

from areyousure import AreYouSure
import enums
import helpers
from Classes.myBot import MyBot
from Classes.team import Team
from Classes.driver import Driver
from Classes.car import Car
from Classes.engine import Engine
from Classes.sponsor import Sponsor
from Classes.primarySponsor import PrimarySponsor
from Classes.result import Result
from Classes.season import Season

class MyTeam(commands.Cog):

    def __init__(self, bot: MyBot):  
        self.bot = bot

    async def cog_load(self):
        logging.info("MyTeam cog loaded successfully.")

    @app_commands.command(name="myteam")
    async def myteam(self, interaction: discord.Interaction):

        team: Team | None = self.bot.teamManager.getTeamByOwner(interaction.user.id)
        if team is None:
            logging.info(f"No team found for user {interaction.user.id}")
            noTeamEmbed = discord.Embed(
                title = "You don't own a team!",
                description = "If there are available team slots, you cannl use /registerteam to set up your team."
            )
            await interaction.response.send_message(embed = noTeamEmbed)
            return
            
        def filterWins(result: Result):
            return result.racePosition == 1
            
        def filterPodiums(result: Result):
            return result.racePosition >= 3
            
        teamResults = self.bot.resultManager.getAllResultsForTeam(team.ID)
        myTeamEmbed = discord.Embed(
            title = team.name,
            description = f"Entries: {len(teamResults)}\nWins: {len([res for res in teamResults if res.racePosition == 1])}\nPodiums: {len([res for res in teamResults if res.racePosition <= 3])}\nPoles: {len([res for res in teamResults if res.qualiPosition == 1])}"
        )

        carText = "No Car"
        if team.car != None:
            car: Car = self.bot.carManager.getCar(team.car)
            carText = f"{car.manufacturer} {car.name}"
            
        engineText = "No Engine"
        if team.engine != None:
            engine: Engine = self.bot.engineManager.getEngine(team.engine)
            engineText = f"{engine.manufacturer} {engine.model}"
            
        myTeamEmbed.add_field(
            name = "Car", 
            value = f"Chassis: {carText}\nEngine: {engineText}\nUpgrades: Drag({team.dragUpgrades}), Weight({team.weightUpgrades})"
        )

        teamDriver1Text = "No Driver Signed"
        teamDriverOne = self.bot.driverManager.getDriver(team.driverOne)
        if teamDriverOne is not None:
            teamDriver1Text = f"{teamDriverOne.firstName} {teamDriverOne.lastName} (Points: N/A)"

        teamDriver2Text = "No Driver Signed"
        teamDriverTwo = self.bot.driverManager.getDriver(team.driverTwo)
        if teamDriverTwo is not None:
            teamDriver2Text = f"{teamDriverTwo.firstName} {teamDriverTwo.lastName} (Points: N/A)"

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
        
        logging.info(f"Team found for user {interaction.user.id}: {team.name} (ID: {team.ID})")
        
    
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
        driversView = discord.ui.View(timeout = 300)
        
        currentSeason: Season = self.bot.seasonManager.getCurrentSeason()
        seasonResults = self.bot.resultsManager.getResultsForSeason(currentSeason.seasonNo)
        seasonStandings: list[tuple] = helpers.getCurrentStandings(seasonResults, currentSeason.pointsModel, currentSeason.pointForPole)
        
        if self.team.driverOne is not None:
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
            driversView.add_item(fireDriverButton(1, self.team, driver1, self.bot))
        else:
            driversEmbed.add_field(
                name = "No Driver Signed",
                value = "You can hire one with the button below."
            )
            driversView.add_item(hireDriverButton(1, self.team, self.bot))
        if self.team.driverTwo is not None:
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
            driversView.add_item(fireDriverButton(2, self.team, driver2, self.bot))
        else:
            driversEmbed.add_field(
                name = "No Driver Signed",
                value = "You can hire one with the button below."
            )
            driversView.add_item(hireDriverButton(2, self.team, self.bot))

        await interaction.response.send_message(embed = driversEmbed, view = driversView)

class hireDriverButton(discord.ui.Button):

    def __init__(self, driverSlot: int, team: Team, bot):

        super().__init__(label = f"Hire Driver for Slot {driverSlot}")
        self.driverSlot = driverSlot
        self.team = team
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):

        allDrivers = self.bot.driverManager.getDrivers()
        allTeams = self.bot.teamManager.getTeams()
        takenDrivers = []
        for team in allTeams:
            if team.driverOne is not -1:
                takenDrivers.append(team.driverOne)
            if team.driverTwo is not -1:
                takenDrivers.append(team.driverTwo)
        self.availableDrivers = [driver for driver in allDrivers if driver.ID not in takenDrivers]
        self.pages = (len(self.availableDrivers) // 10) + 1
        self.pageEmbeds = []
        for page in range(self.pages):
            embed = discord.Embed(
                title = "Available Drivers",
                description = f"Page {page+1} of {self.pages}"
            )
            for i in range(10):
                if (page*10)+i == len(self.availableDrivers): break
                driver: Driver = self.availableDrivers[(page*10)+i]
                driverAvg = (driver.qualiPace + driver.racePace + driver.wetPace + driver.tyreManagement + driver.aggressiveness + driver.defending)/6
                embed.add_field(
                    name = f"{driver.firstName} {driver.lastName} - ID: {driver.ID}",
                    value = f"""QPACE: {driver.qualiPace} RPACE: {driver.racePace} WPACE: {driver.wetPace}
                    TYRE: {driver.tyreManagement} AGG: {driver.aggressiveness} DEF: {driver.defending}
                    AVG: {driverAvg} COST: {driver.contractCost}"""
                )
            self.pageEmbeds.append(embed)
        self.pageView = discord.ui.View()
        self.currentPage = 1
        await interaction.response.send_message(embed = self.pageEmbeds[self.currentPage], view = self.pageView)
        
        @discord.ui.button(label="Previous Page", style=discord.ButtonStyle.green, disabled=self.currentPage==1)
        async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            
            self.currentPage -= 1
            if self.currentPage == 0:
                self.previous_button.disabled = True
            self.nextButton.disabled = False
            self.updateEmbed(interaction)

        @discord.ui.button(label="Next Page", style=discord.ButtonStyle.green)
        async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            
            self.currentPage += 1
            if self.currentPage == len(self.pages):
                self.next_button.disabled = True
            self.previous_button.disabled = False
            self.updateEmbed(interaction)
            
        async def updateEmbed(self, interaction: discord.Interaction):

            await interaction.response.edit_message(embed = self.pageEmbeds[self.currentPage-1], view = self.pageView)
            
        self.pageView.add_item(previous_button)
        self.pageView.add_item(next_button)
        self.message = interaction.response.send_message(embed=self.pageEmbeds[0], view=self.pageView)
        

class fireDriverButton(discord.ui.Button):

    def __init__(self, driverSlot: int, team: Team, driver: Driver, bot):

        super().__init__(label = f"Fire {driver.firstName} {driver.lastName}")
        self.driverSlot = driverSlot
        self.driver = driver
        self.team = team
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):

        firingEmbed = discord.Embed(
            title = "Are you sure you want to fire your driver?",
            description = "You may not be able to re-hire them later!"
        )
        await interaction.response.send_message(embed = firingEmbed, view = AreYouSure(self.fireDriver, self.dontFireDriver))

    async def fireDriver(self, interaction: discord.Interaction):

        firedEmbed = discord.Embed(
            title = f"{self.driver.firstName} {self.driver.lastName} has been fired from {self.team.name}."
        )
        await interaction.response.send_message(embed = firedEmbed)
        if self.driverSlot == 1:
            self.team.driverOne = None
        else:
            self.team.driverTwo = None
        self.bot.teamManager.updateTeam(self.team)

    async def dontFireDriver(self, interaction: discord.Interaction):

        firingCancelledEmbed = discord.Embed(
            title = "Firing Cancelled.",
            description = "Your driver is still signed!"
        )
        await interaction.response.send_message(embed = firingCancelledEmbed)
  

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


async def setup(bot: MyBot):  
    logging.info("Loading MyTeam cog...")
    await bot.add_cog(MyTeam(bot))