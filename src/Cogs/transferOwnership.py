import discord
from discord import app_commands
from discord.ext import commands
import logging

from areyousure import areYouSure

class TransferOwnership(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("TransferOwnership cog loaded successfully.")

    @app_commands.command(name="transferownership")
    @app_commands.describe(newowner = "New Owner (by Discord ID)")
    async def transferownership(self, interaction: discord.Interaction, newowner: str):
        team = self.bot.teamManager.getOwnerTeam(interaction.user.id)
        if team == None:
            await interaction.response.send_message("You don't own a team!")
        else:
            areYouSureView = areYouSure((team[0], newowner), self.transferOwnershipConfirmed, await interaction.response.send_message("Team ownership transfer cancelled."), self.bot.databaseManager)
            await interaction.response.send_message(embed = discord.Embed(
                title="Confirm Team Ownership Transfer",
                description=f"Are you sure you want to transfer ownership of team {team[1]} to {newowner}?"
            ), view=areYouSureView)

    async def transferOwnershipConfirmed(self, args: tuple, interaction: discord.Interaction):
        teamID, newOwnerID = args
        if not self.bot.teamManager.checkIfUserOwnsTeam(newOwnerID):
            self.bot.teamManager.changeTeamOwnership(teamID, newOwnerID)
        else:
            await interaction.response.send_message("That user already owns a team, and cannot own another.")


async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading TransferOwnership cog...")
    await bot.add_cog(TransferOwnership(bot))