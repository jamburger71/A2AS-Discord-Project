import discord
from discord import app_commands
from discord.ext import commands
import logging

from areyousure import areYouSure

class RemoveDriver(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("RemoveDriver cog loaded successfully.")

    @app_commands.command(name="removedriver")
    @app_commands.describe(driverid = "Driver ID or Three-Letter Code")
    @app_commands.checks.has_role("Moderator")
    async def removedriver(self, interaction: discord.Interaction, driverid: str):
        if driverid.isdigit():
            driverid = int(driverid) # type: ignore
        driver = self.bot.driverManager.getDriver(driverid)
        if driver is None:
            await interaction.response.send_message(f"No driver found with ID or code '{driverid}'.")
        else:
            view = areYouSure((driver,), removeDriverConfirmed, await interaction.response.send_message("Driver removal cancelled."))
            embed = discord.Embed(
                title="Are you sure?", 
                description=f"You will be removing {driver[1]} {driver[2]} from the database. You will need to manually re-insert him later if you want him back. This action cannot be undone.",
                )
            if not self.bot.driverManager.checkDriverAvailability(driver[0]):
                embed.add_field(
                    name="Warning", 
                    value=f"This driver is currently contracted to a team."
                )
            await interaction.response.send_message(embed = embed, view=view)
                

async def removeDriverConfirmed(self, args: tuple, interaction: discord.Interaction):
    driver = args[0]
    self.bot.driverManager.removeDriver(driver[0])
    await interaction.response.send_message(f"{driver[1]} {driver[2]} with ID {driver[0]} has been removed from the database.")

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading RemoveDriver cog...")
    await bot.add_cog(RemoveDriver(bot))