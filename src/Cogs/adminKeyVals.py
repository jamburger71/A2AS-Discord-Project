
import discord
from discord import app_commands, Interaction
from discord.ext import commands
import logging
from discordLogger import DiscordLogger

from Classes.driver import Driver
from areyousure import AreYouSure
from enums import keyVals

class AdminKeyVals(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("AdminManageDrivers cog loaded successfully.")

    @app_commands.command(name = "adminkeyvals")
    @app_commands.checks.has_role("Moderator")
    async def adminkeyvals(self, interaction: discord.Interaction):

        keyValEmbed = discord.Embed(
            title = "Key Val Manager",
            description = "Manage the key-val databade here."
        )

        allKeyVals = self.bot.keyValManager.getAllKeyVals()
        allKeyVals.sort()
        halfList = len(allKeyVals)//2
        leftSide = allKeyVals[halfList:]
        rightSide = allKeyVals[:halfList]
        leftText = ""
        rightText = ""
        for (key, value) in leftSide:
            leftText += f"{key}: {value}\n"
        for (key, value) in rightSide:
            rightText += f"{key}: {value}\n"

        keyValEmbed.add_field(
            name = "Key: Value",
            value = leftText
        )
        keyValEmbed.add_field(
            name = "",
            value = rightText
        )

        keyValView = discord.ui.View(timeout=300)
        keyValView.add_item(addKeyValButton(self.bot))
        keyValView.add_item(updateKeyValButton(self.bot))
        keyValView.add_item(deleteKeyValButton(self.bot))

        await interaction.response.send_message(embed = keyValEmbed)

class addKeyValButton(discord.ui.Button):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(label = "Add New KeyVal")

    async def callback(self, interaction: Interaction):

        await interaction.response.send_modal(addKeyValModal(self.bot))

class addKeyValModal(discord.ui.Modal):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(title = "Add New KeyVal")

    key = discord.ui.TextInput(
        label = "Key",
        placeholder = "No spaces please..."
    )
    value = discord.ui.TextInput(
        label = "Value",
        placeholder = "Anything you want"
    )

    async def on_submit(self, interaction: discord.Interaction):

        self.bot.keyValManager.insertVal(self.key.value, self.value.value)
        successEmbed = discord.Embed(
            title = f"{self.key.value} Added",
            description = f"Value: {self.value.value}"
        )
        await interaction.response.send_message(embed=successEmbed)

class updateKeyValButton(discord.ui.Button):

    def __init__(self, bot):

        self.bot = bot
        super().__init__(label = "Update KeyVal")

    async def callback(self, interaction: discord.Interaction):

        updateEmbed = discord.Embed(title = "Which keyVal would you like to update?")
        updateView = discord.ui.View(timeout=60)
        updateView.add_item(selectKeyValSelect(self.bot, True))

class deleteKeyValButton(discord.ui.Button):

    def __init__(self, bot):

        self.bot = bot
        super().__init__(label = "Delete KeyVal")
        

    async def callback(self, interaction: discord.Interaction):

        deleteKeyValView = discord.ui.View()
        deleteKeyValView.add_item(selectKeyValSelect(self.bot, False))
        deleteEmbed = discord.Embed(title = "Which keyVal would you like to delete?")
        await interaction.response.send_message(embed = deleteEmbed, view = deleteKeyValView)

class selectKeyValSelect(discord.ui.Select):

    def __init__(self, bot, update: bool):

        self.bot = bot
        self.keyVals = self.bot.keyValManager.getAllKeyVals()
        self.update = update
        options = []
        for (key, value) in self.keyVals:
            options.append(discord.SelectOption(label=key))
        super().__init__(
            placeholder = "Choose a KeyVal",
            options = options
        )

    async def callback(self, interaction: discord.Interaction):

        self.key = self.values[0]
        if self.update:
            value = self.bot.keyValManager.getKeyVal(self.key)
            await interaction.response.send_modal(updateKeyValModal(self.bot, self.key, value))
        else:
            deleteEmbed = discord.Embed(
                title = f"Are you sure you want to delete {self.key}?",
                description = f"Deleting this KeyVal may have unintended results."
            )
            await interaction.response.send_message(embed = deleteEmbed, view = AreYouSure(self.confirmDelete, self.cancelDelete))

    async def confirmDelete(self, interaction: discord.Interaction):

        successEmbed = discord.Embed(title = f"{self.key} deleted.")
        self.bot.keyValManager.deleteKeyVal(self.key)

    async def cancelDelete(self, interaction: discord.Interaction):

        cancelEmbed = discord.Embed(title = "Operation Cancelled")
        await interaction.response.send_message(embed = cancelEmbed)

class updateKeyValModal(discord.ui.Modal):

    oldValue = 0
    
    def __init__(self, bot, key, value):

        self.bot = bot
        self.key = key
        oldValue = value
        self.oldValue = value
        super().__init__(title = f"Updating value for {key}")

    value = discord.ui.TextInput(
        label = "New Value",
        placeholder = f"Previous value: {oldValue}"
    )

    async def on_submit(self, interaction: discord.Interaction):

        newValue = self.value.value
        self.bot.keyValManager.updateKeyVal(self.key, newValue)
        successEmbed = discord.Embed(
            title = f"{self.key} Changed",
            description = f"New value: {newValue} (old: {self.oldValue})"
        )
        await interaction.response.send_message(embed=successEmbed)

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print(f"Loading {AdminKeyVals.__name__} cog...")
    await bot.add_cog(AdminKeyVals(bot))