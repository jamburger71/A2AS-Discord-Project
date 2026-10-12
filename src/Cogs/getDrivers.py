import discord
from discord import app_commands
from discord.ext import commands
import logging

from helpers import convertToPounds, groupReturnsByN
from pageController import PageController

class GetDrivers(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("GetDriver cog loaded successfully.")

    @app_commands.command(name="alldrivers")
    @app_commands.describe(availableonly="Whether to only show available drivers")
    async def alldrivers(self,interaction: discord.Interaction, availableonly: bool = False):
        drivers = self.bot.driverManager.getAllDrivers(availableOnly=availableonly)
        if len(drivers) == 0:
            await interaction.response.send_message("No drivers found.")
        else:
            pages = groupReturnsByN(10, drivers)
            currentPage = 1
            embed = discord.Embed(title="All Drivers", description=f"Page {currentPage} of {len(pages)}")
            view = PageController(pages=pages, currentPage=currentPage, interaction=interaction, nextPageFunc=self.nextPage)
            for driver in pages[currentPage - 1]:
                if driver is not None:
                    embed.add_field(name=f"{driver[1]} {driver[2]}", value=f"ID: {driver[0]}, Code: {driver[3]}, Nationality: {driver[4]}, Age: {driver[5]}", inline=False)
            await interaction.response.send_message(embed=embed, view=view)

    async def nextPage(self, interaction: discord.Interaction, lastMessage: discord.Message, pages: list, currentPage: int):
        totalPages = len(pages)
        embed = discord.Embed(title="All Drivers", description=f"Page {currentPage + 1} of {totalPages}")
        driverList = pages[currentPage]
        for driver in driverList:
            if driver is not None:
                embed.add_field(name=f"{driver[1]} {driver[2]}", value=f"ID: {driver[0]}, Code: {driver[3]}, Nationality: {driver[4]}, Age: {driver[5]}", inline=False)
        await lastMessage.delete()
        await interaction.response.send_message(embed=embed)



async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading GetDrivers cog...")
    await bot.add_cog(GetDrivers(bot))