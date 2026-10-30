import discord
from discord import app_commands
from discord.ext import commands
import logging
from discordLogger import DiscordLogger

from Classes.driver import Driver
from areyousure import AreYouSure
from enums import keyVals

class AdminManageDrivers(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("AdminManageDrivers cog loaded successfully.")

    @app_commands.command(name="adminmanagedrivers")
    @app_commands.checks.has_role("Moderator")
    async def adminmanagedrivers(self, interaction: discord.Interaction):
        
        DriverManageEmbed = discord.Embed(
            title = "Manage Drivers",
            description="For Admins Only - manage the whole driver database here."
        )

        await interaction.response.send_message(embed = DriverManageEmbed, view = DriverManageView(self.bot))

class DriverManageView(discord.ui.View):

    def __init__(self, bot):

        super().__init__(timeout=60)
        self.bot = bot

        @discord.ui.button(label="Add Driver")
        async def callback_addDriver(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(AddDriverModal(self.bot))
        
        @discord.ui.button(label="Add Random Drivers")
        async def callback_addRandomDrivers(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(addRandomDriversModal(self.bot))
        
        @discord.ui.button(label="Edit Driver")
        async def callback_editDriver(self, interaction:discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message()
        
        @discord.ui.button(label="Age All Drivers By 1")
        async def callback_ageAllDrivers(self, interaction:discord.Interaction, button: discord.ui.Button):
            
            async def confirm(args, interaction: discord.Interaction):
                self.bot.DriverManager.ageAllDrivers()
                await interaction.response.send_message("All drivers aged by 1 year.")
            
            async def deny(args, interaction: discord.Interaction):
                await interaction.response.send_message("Command Cancelled.")
                
            await interaction.response.send_message(view=AreYouSure(None, confirm, deny))


class AddDriverModal(discord.ui.Modal, title="Add New Driver"):

    def __init__(self, bot):

        super().__init__()
        self.bot = bot

    name = discord.ui.TextInput(label="Firstname/Surname/Age/Nationality", placeholder="Use / to separate values")
    paceStats = discord.ui.TextInput(label="Quali pace/Race pace/Wet pace", placeholder="Between 0 & 100")
    racecraftStats = discord.ui.TextInput(label="Tyre Management/Aggressiveness/Defending", placeholder="Between 0 & 100")
    cost = discord.ui.TextInput(label="Season cost", placeholder="Can be negative - pay driver!")

    async def on_submit(self, interaction: discord.Interaction):

        driverDetails = tuple(self.name.value.split('/'))
        driverPace = tuple(self.paceStats.value.split('/'))
        driverRacecraft = tuple(self.racecraftStats.value.split('/'))
        driverCost = tuple(self.cost.value,)
        if len(driverDetails) == 4 and len(driverPace) == 3 and len(driverRacecraft) == 3:
            driverID = self.bot.KeyValManager.getAndIterateKeyVal(keyVals.NEXTDRIVERID)
            self.bot.driverManager.insertDriver(Driver((driverID, ) + driverDetails  + driverPace + driverRacecraft + driverCost))

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
            driverID = self.bot.KeyValManager.getAndIterateKeyVal(keyVals.NEXTDRIVERID)
            newDriver = Driver.randomDriver(driverID=driverID)
            self.bot.driverManager.insertDriver(newDriver)

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print(f"Loading {AdminManageDrivers.__name__} cog...")
    await bot.add_cog(AdminManageDrivers(bot))