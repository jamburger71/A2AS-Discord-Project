import discord

class pagecontroller(discord.ui.View):
    def __init__(self, pages: list, currentPage: int, interaction: discord.Interaction, nextPageFunc=None):
        super().__init__(timeout=300)
        self.pages = pages
        self.currentPage = currentPage
        self.lastInteraction = interaction
        self.nextPageFunc = nextPageFunc

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentPage > 0:
            self.currentPage -= 1
            if self.nextPageFunc is not None:
                self.nextPageFunc(interaction=interaction, lastMessage=self.lastInteraction.message, pages=self.pages, currentPage=self.currentPage-1)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.currentPage < len(self.pages) - 1:
            self.currentPage += 1
            if self.nextPageFunc is not None:
                self.nextPageFunc(interaction=interaction, lastMessage=self.lastInteraction.message, pages=self.pages, currentPage=self.currentPage+1)