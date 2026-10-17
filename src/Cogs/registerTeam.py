import discord
from discord import app_commands
from discord.ext import commands
import logging

class RegisterTeamModal(discord.ui.Modal, title="Register Team"):

    def __init__(self, bot):

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

        self.bot.teamDatabase.registerTeam()
        await interaction.response.send_message("""Team Registered! Manage your team with /myteam. 
        Until you have assigned your team a car, drivers, and an engine supplier, your team will not compete.""")

class ChooseTeamCarDropdown(discord.ui.Select):

    def __init__(self):
        carOptions = [] #TODO get current car options
        options = []
        for carOption in carOptions:
            options.append(discord.SelectOption(
                label = carOption.carName
            ))

        super().__init__(
            placeholder = "Select your team car",
            min_values=1,
            max_values=1,
            options=options
        )

class RegisterTeam(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("RegisterTeam cog loaded successfully.")

    @app_commands.command(name="registerteam")
    @app_commands.describe()
    async def registerteam(
        self,
        interaction: discord.Interaction):
        team = self.bot.teamManager.getOwnerTeam(interaction.user.id)
        if team != None:
            await interaction.response.send_message("You already own a team! To manager your team, use /myteam")
            return
        interaction.response.send_modal(RegisterTeamModal(self.bot))

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading RegisterTeam cog...")
    await bot.add_cog(RegisterTeam(bot))