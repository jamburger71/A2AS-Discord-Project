import discord
from discord import app_commands
from discord.ext import commands
import logging

class HelpAdmin(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("Help cog loaded successfully.")

    @app_commands.command(name="helpadmin")
    @app_commands.describe()
    async def help(self, interaction: discord.Interaction):

        commandsEmbed = discord.Embed(
            title = "Admin Commands",
            description = """Below is a list of all available admin commands.
            Only those with the Moderator command can use them."""
        )
        commandsEmbed.add_field(
            name = "Database Commands",
            value = """
            /removeteam - Removes a team from the database (NOT IMPLEMENTED)
            /insertnewdriver - Inserts a new driver into the database
            /removedriver - Removes a driver from the database
            /changedrivername - Changes a driver's name (NOT IMPLEMENTED)
            /insertnewsponsor - Inserts a new sponsor (primary or secondary) into the database (NOT IMPLEMENTED)
            """,
            inline = False
        )
        commandsEmbed.add_field(
            name = "Progression Commands",
            value = """
            /agedrivers - Ages all drivers by 1 year, for use at the end of the season (NOT IMPLEMENTED)
            /createnewcalendar - Creates a new calendar for the next season (NOT IMPLEMENTED)
            /editcalendar - Edits the calendar for a season (NOT IMPLEMENTED)
            /insertresults - Inserts results for a race into the database (NOT IMPLEMENTED)
            /editresults - Edits results for a race in the database (NOT IMPLEMENTED)
            """
        )
        await interaction.response.send_message(embed = commandsEmbed)

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading HelpAdmin cog...")
    await bot.add_cog(HelpAdmin(bot))