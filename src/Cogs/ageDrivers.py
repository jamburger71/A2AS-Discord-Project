import discord
from discord import app_commands
from discord.ext import commands
import logging
from discordLogger import DiscordLogger

from areyousure import AreYouSure

class AgeDrivers(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("AgeDrivers cog loaded successfully.")

    @app_commands.command(name="agedrivers")
    async def agedrivers(self, interaction: discord.Interaction):

        self.discLogger = DiscordLogger(interaction.user, "Age All Drivers", self.bot)
        view = AreYouSure(None, self.ageDriversConfirmed, self.ageDriversDenied)
        self.discLogger.info("Asking if the user is sure")
        await interaction.response.send_message(embed = discord.Embed(
            title="Are you sure?", 
            description=f"You will be aging all drivers by 1 year. This action will have to be manually reverted."
            ), view=view)

    async def ageDriversConfirmed(self, args: None, interaction: discord.Interaction):
        self.discLogger.info("User confirms request to age all drivers")
        self.bot.driverManager.ageAllDrivers(self.discLogger)
        await interaction.response.send_message("All drivers have been aged by 1 year.")
        await self.discLogger.submit()

    async def ageDriversDenied(self, args: None, interaction: discord.Interaction):
        self.discLogger.warn("User manually cancelled the action.")
        await self.discLogger.submit()
        await interaction.response.send_message("Driver aging cancelled.")

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading AgeDrivers cog...")
    await bot.add_cog(AgeDrivers(bot))