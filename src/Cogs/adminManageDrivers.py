import discord
from discord import app_commands
from discord.ext import commands
import logging
from discordLogger import DiscordLogger
from faker import Faker
from faker.config import AVAILABLE_LOCALES
import random

import helpers
from Classes.driver import Driver

class AdminManageDrivers(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("AdminManageDrivers cog loaded successfully.")

    @app_commands.command(name="adminmanagedrivers")
    @app_commands.checks.has_role("Moderator")
    async def adminmanagedrivers(self, interaction: discord.Interaction):

        await interaction.response.send_message(view = DriverManageView(self.bot))

class DriverManageView(discord.ui.View):

    def __init__(self, bot):

        super().__init__(timeout=60)
        self.bot = bot

        @discord.ui.button(label="Add Driver")
        async def callback_addDriver(self, interaction: discord.Interaction, button: discord.ui.Button):

            await interaction.response.send_modal(AddDriverModal(self.bot))

class AddDriverModal(discord.ui.Modal, title="Add New Driver"):

    def __init__(self, bot):

        super().__init__()
        self.bot = bot

    name = discord.ui.TextInput(
        label="Firstname/Surname/Age/Nationality",
        placeholder="Use / to separate values"
        )
    paceStats = discord.ui.TextInput(
        label="Quali pace/Race pace/Wet pace",
        placeholder="Between 0 & 100"
    )
    racecraftStats = discord.ui.TextInput(
        label="Tyre Management/Aggressiveness/Defending",
        placeholder="Between 0 & 100"
    )
    cost = discord.ui.TextInput(
        label="Season cost",
        placeholder="Can be negative - pay driver!"
    )

    async def on_submit(self, interaction: discord.Interaction):

        driverDetails = tuple(self.name.value.split('/'))
        driverPace = tuple(self.paceStats.value.split('/'))
        driverRacecraft = tuple(self.racecraftStats.value.split('/'))
        driverCost = tuple(self.cost.value,)
        if len(driverDetails) == 4 and len(driverPace) == 3 and len(driverRacecraft) == 3:
            allThreecodes = self.bot.driverManager.getThreeCodes()
            driverID = helpers.getBestLetterCode(driverDetails[0], driverDetails[1], allThreecodes)
            self.bot.driverManager.insertDriver(Driver(driverDetails + driverPace + driverRacecraft + driverCost, ))

class addRandomDriversModal(discord.ui.Modal):

    def __init__(self, bot):

        super().__init__(timeout=60)
        self.bot = bot

    howMany = discord.ui.TextInput(
        label="How many drivers?",
        placeholder="1 to 100"
    )

    async def on_submit(self, interaction: discord.Interaction):

        driverCount = self.howMany.value
        for i in range(int(driverCount)):
            faker = Faker(random.choice(AVAILABLE_LOCALES))
            firstname, lastname = faker.name().split(' ')
            allThreecodes = self.bot.driverManager.getThreeCodes()
            threecode = helpers.getBestLetterCode(firstname, lastname, allThreecodes)
            if threecode is not None:
                age = random.randint(18, 45)
                nationality = faker.country()
                baseVal = random.randint(0, 100)
                deviation = random.randint(0, 25)
                qualiPace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
                racePace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
                wetPace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
                tyreManagement = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
                aggressiveness = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
                defending = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
                newDriver = Driver((threecode, firstname, lastname, qualiPace, racePace))

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading AgeDrivers cog...")
    await bot.add_cog(AdminManageDrivers(bot))