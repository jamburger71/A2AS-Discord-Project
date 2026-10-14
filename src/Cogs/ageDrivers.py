import discord
from discord import app_commands
from discord.ext import commands
import logging

from areyousure import areYouSure

class AgeDrivers(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("AgeDrivers cog loaded successfully.")

    @app_commands.command(name="agedrivers")
    async def agedrivers(self, interaction: discord.Interaction):

        view = areYouSure(None, self.ageDriversConfirmed, await interaction.response.send_message("Driver aging cancelled."))
        await interaction.response.send_message(embed = discord.Embed(
            title="Are you sure?", 
            description=f"You will be aging all drivers by 1 year. This action will have to be manually reverted."
            ), view=view)

    async def ageDriversConfirmed(self, args: None, interaction: discord.Interaction):
        self.bot.driverManager.ageAllDrivers()
        await interaction.response.send_message("All drivers have been aged by 1 year.")

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading AgeDrivers cog...")
    await bot.add_cog(AgeDrivers(bot))