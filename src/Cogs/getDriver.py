import discord
from discord import app_commands
from discord.ext import commands
import logging

from helpers import convertToPounds

class GetDriver(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("GetDriver cog loaded successfully.")

    @app_commands.command(name="getdriver")
    @app_commands.describe(driverid = "Driver ID or Three-Letter Code")
    async def getdriver(self, interaction: discord.Interaction, driverid: str):
        if driverid.isdigit():
            driverid = int(driverid) # type: ignore
        driver = self.bot.driverManager.getDriver(driverid)
        if driver is None:
            await interaction.response.send_message(f"No driver found with ID or code '{driverid}'.")
        else:
            driverEmbed = discord.Embed(title=f"{driver[1]} {driver[2]}")
            driverEmbed.description = f"ID: {driver[0]}\nNationality: {driver[4]}\nAge: {driver[5]}"
            driverEmbed.add_field(name="Stats", 
                                value=f"Qualifying Pace: {driver[6]}\nRace Pace: {driver[7]}\nWet Weather Pace: {driver[8]}\nTyre Management: {driver[9]}\nAggressiveness: {driver[10]}\nDefending: {driver[11]}", inline=False)
            driverEmbed.add_field(name="Contract Cost", value=convertToPounds(driver[12]))
            driverEmbed.add_field(name="Statistics",
                                value=f"Races: {driver[13]}\nWins: {driver[14]}\nPodiums: {driver[15]}", inline=False)
            await interaction.response.send_message(embed = driverEmbed)

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading GetDriver cog...")
    await bot.add_cog(GetDriver(bot))