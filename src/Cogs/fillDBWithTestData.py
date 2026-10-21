import discord
from discord import app_commands
from discord.ext import commands
import logging
from faker import Faker

from discordLogger import DiscordLogger

class FillDBWithTestData(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("FillDBWithTestData cog loaded successfully.")

    @app_commands.command(name="filldbwithtestdata")
    @app_commands.checks.has_role("Moderator")
    async def filldbwithtestdata(self, interaction: discord.Interaction):
        faker = Faker()
        for _ in range(50):
            fakeName = faker.name().split(" ")
            self.bot.driverManager.insertDriver(
                fakeName[0], fakeName[1], faker.country(),
            )

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading FillDBWithTestData cog...")
    await bot.add_cog(FillDBWithTestData(bot))