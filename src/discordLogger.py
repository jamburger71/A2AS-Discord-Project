import discord
from discord.ext import commands
import os

class DiscordLogger:

    def __init__(self, author, action: str, bot: "MyBot"): # type: ignore # noqa: F821

        self.GOOD = 0
        self.WARNING = 1
        self.ERROR = 2
        self.fullLog: list = []
        self.warnings: list = []
        self.errors: list = []
        self.author = author
        self.action = action
        self.bot = bot
        self.logState: int = self.GOOD

    def info(self, log: str):

        self.fullLog.append("INFO: "+log)

    def warn(self, log: str):

        self.fullLog.append("WARN: "+log)
        self.warnings.append("WARN: "+log)
        self.logState = max(self.logState, self.WARNING)

    def error(self, log: str):

        self.fullLog.append("ERROR: "+log)
        self.errors.append("ERROR: "+log)
        self.logState = self.ERROR

    async def submit(self):

        logChannel = self.bot.get_channel(os.getenv("DISCORD_LOG_CHANNEL"))
        logEmbed = discord.Embed()
        if self.logState == self.GOOD:
            logEmbed.title = f"{self.author.name} completed action: {self.action}"
            logEmbed.description = "The action was completed with no issues."
            logEmbed.color = discord.Color.green()
        elif self.logState == self.WARNING:
            logEmbed.title = f"{self.author.name} completed action with warnings: {self.action}"
            logEmbed.description = f"The action completed with {len(self.warnings)} warning(s)."
            logEmbed.color = discord.Color.yellow()
        else:
            logEmbed.title = f"{self.author.name} failed to complete action: {self.action}"
            logEmbed.description = f"The action failed with {len(self.errors)} error(s) and {len(self.warnings)} warning(s)."
            logEmbed.color = discord.Color.red()
            
        if self.logState >= self.WARNING:
            warningsDesc = "None"
            if len(self.warnings) > 0:
                warningsDesc = ""
                for warning in self.warnings:
                    warningsDesc += (warning + "\n")
            logEmbed.add_field(
                name = "Warnings:",
                value = warningsDesc
            )
        if self.logState == self.ERROR:
            errorDesc = ""
            for error in self.errors:
                errorDesc += (error + "\n")
            logEmbed.add_field(
                name = "Errors:",
                value = errorDesc
            )
        logDesc = ""
        for log in self.fullLog:
            logDesc += (log + "\n")
        logEmbed.add_field(
            name = "Full Log:",
            value = logDesc
        )
        await logChannel.send_message(embed = logEmbed)