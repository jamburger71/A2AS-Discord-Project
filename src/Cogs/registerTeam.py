import discord
from discord import app_commands
from discord.ext import commands
import logging

class RegisterTeamModal(discord.ui.Modal, title="Register Team"):

    def __init__(self, bot):

        super().__init__()
        self.bot = bot
        
    name = discord.ui.TextInput(
        label="Team Name",
        placeholder="Team name...",
        required=True
    )
    description = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Team Description",
        placeholder = "Team description...",
        required=False,
        max_length=500
    )
    nationality = discord.ui.TextInput(
        label="Team Nationality",
        placeholder="Nationality...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        
        teamID = self.bot.keyValManager.getKeyVal("NextTeamID")

        self.bot.teamManager.registerTeam(interaction.user.id, self.name.value, self.description.value, self.nationality.value, teamID)
        await interaction.response.send_message("""Team Registered! Manage your team with /myteam.
        Until you have assigned your team a car, drivers, and an engine supplier, your team will not compete.
        You can assign these values using the commands in /myteam.""")
        self.bot.keyValManager.updateKeyVal("NextTeamID", teamID+1)

class RegisterTeam(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("RegisterTeam cog loaded successfully.")

    @app_commands.command(name="registerteam")
    @app_commands.describe()
    async def registerteam(self, interaction: discord.Interaction):
        team = self.bot.teamManager.getOwnerTeam(interaction.user.id)
        if team != None:
            await interaction.response.send_message("You already own a team! To manager your team, use /myteam")
            return
        await interaction.response.send_modal(RegisterTeamModal(bot=self.bot))

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading RegisterTeam cog...")
    await bot.add_cog(RegisterTeam(bot))