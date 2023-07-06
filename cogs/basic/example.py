import discord
from discord import app_commands, ui
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext import tasks

class Example(commands.Cog): #name of your cog class, typically name it based off of your .py file
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="example", description="This is a command") #this is what names your command in the tree
    async def example(self, interaction: discord.Interaction): #function the command will perform
        await interaction.response.send_message("You used the example cog!")
        return

async def setup(client):
    #guild = client.get_guild(guildid) #uncomment this and the comment on line 18 to sync the cog to a specific guild
    await client.add_cog(About(client))#, guilds=[guild])