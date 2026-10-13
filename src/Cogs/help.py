import discord
from discord import app_commands
from discord.ext import commands
import logging

class Help(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("Help cog loaded successfully.")

    @app_commands.command(name="help")
    @app_commands.describe()
    async def help(self, interaction: discord.Interaction):

        commandsEmbed = discord.Embed(
            title = "All Commands",
            description = "Below is a list of all available commands and a short description."
        )
        commandsEmbed.add_field(
            name = "General Commands",
            value = """
            /help - Displays this help message
            /calendar - Displays the current season's calendar (NOT IMPLEMENTED)
            /standings - Displays the current season's standings (NOT IMPLEMENTED)
            /teamstandings - Displays the current season's team standings (NOT IMPLEMENTED)
            /alldrivers - Displays all drivers and their stats (NOT IMPLEMENTED)
            /viewprimarysponsors - Displays all primary sponsors and their stats (NOT IMPLEMENTED)
            /viewsecondarysponsors - Displays all secondary sponsors and their stats (NOT IMPLEMENTED)
            """,
            inline = False
        )
        commandsEmbed.add_field(
            name = "Team Management Commands",
            value = """
            /myteam - Displays your team information
            /changeteamname - Changes your team name
            /registerteam - Registers a new team.
            /transferownership - Transfers ownership of your team to another user. Tag the person you want to transfer ownership to. (NOT IMPLEMENTED)
            /buyupgrade - Buys an upgrade for your team (NOT IMPLEMENTED)
            """,
            inline = False
        )
        await interaction.response.send_message(embed = commandsEmbed)

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading Help cog...")
    await bot.add_cog(Help(bot))