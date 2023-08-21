#imports
import discord
from discord import app_commands, ui
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext import tasks
import datetime
import os
import aiosqlite #can change based off of db used for project
import nacl #to join voice channels
import random
import requests

#configuration
class ViewPersistence(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        description = "Bot Description here"
        prefix = "."
        super().__init__(description=description, command_prefix=prefix, intents=intents)
        
    async def setup_hook(self) -> None: #for persistent views, add the view here
        self.add_view()
client = ViewPersistence()


#globals
global guild
global embedColor
global guildid

guild = discord.Object(id="guildid")
embedColor = discord.Color.from_str("#ffffff")

#functions
async def loadCogsAndExtensions():
    successfulCogs = []
    failedCogs = []
    successfulPremiumCogs = []
    failedPremiumCogs = []
    successfulExtensions = []
    failedExtensions = []
    for extension in os.listdir('./extensions'):
        if extension.endswith('.py'):
            try: #try to load all extensions for all servers, if it fails then add it to fail list
                await client.load_extension(f'extensions.{cog[:-3]}')
                successfulExtensions.append(extension[:-3])
            except Exception as e:
                print(f"Failed to load {extension[:-3]}. Error: {e}")
                failedExtensions.append(extension[:-3])
    for cog in os.listdir('./cogs/basic'):
        if cog.endswith('.py'):
            try: #try to load all basic cogs for all servers, if it fails then add it to fail list
                await client.load_extension(f'cogs.basic.{cog[:-3]}')
                successfulCogs.append(cog[:-3])
            except Exception as e:
                print(f"Failed to load {cog[:-3]}. Error: {e}")
                failedCogs.append(cog[:-3])
    for cog in os.listdir('./cogs/premium'):
        if cog.endswith('.py'):
            try: #try to load all premium cogs for all servers, if it fails then add it to fail list
                await client.load_extension(f'cogs.premium.{cog[:-3]}')
                successfulPremiumCogs.append(cog[:-3])
            except Exception as e:
                print(f"Failed to load {cog[:-3]}. Error: {e}")
                failedPremiumCogs.append(cog[:-3])
    return successfulCogs, failedCogs, successfulPremiumCogs, failedPremiumCogs, successfulExtensions, failedExtensions

@client.tree.command(name="sync", description="Sync command tree", guild=guild) #useful for catching the bot up to servers that haven't received updates.
async def sync(interaction: discord.Interaction):
    if interaction.user.id == interaction.guild.owner:
        await client.tree.sync()
        await interaction.response.send_message("Synced client command tree.", ephemeral=True)
    else:
        embed = await embeds.Error.build("You do not have permission to use this command.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="reload", description="Reloads a specific cog", guild=guild) #useful for hot-reloading commands that have been changed or edited since the bot has come online.
@app_commands.choices(type=[app_commands.Choice(name="Basic", value="basic"), app_commands.Choice(name="Premium", value="premium")])
async def reload(interaction: discord.Interaction, type: str, cog: str):
    try:
        await client.reload_extension(f"cogs.{type}.{cog}") #cogs.basic.{cog} basically becomes ./cogs/basic/cogname.py
        await interaction.response.send_message(f"Reloaded {cog}", ephemeral=True)
    except Exception as e:
        print(e)
        await client.load_extension(f"cogs.{type}.{cog}")
        await interaction.response.send_message(f"Loaded {cog}", ephemeral=True)
            

@client.event
async def on_ready():
    #guild = client.get_guild(guildid)
    #members = len([x for x in guild.members if not x.bot])
    prep = await loadCogsAndExtensions() #load out our bot files so we may count success and fails
    guild = client.get_guild(guildid) #find host guild for any administrative bot tasks (such as reloading cogs)
    await client.tree.sync(guild=guild) #sync command tree to host guild so host guild is always up to date with commands.
    print(f"Login successful.\nBot User: {client.user}\nSuccessful Basic Cogs: {len(prep[0])}\nFailed Basic Cogs: {len(prep[1])}\nSuccessful Premium Cogs: {len(prep[2])}\nFailed Premium Cogs: {len(prep[3])}\nSuccessful Extensions: {len(prep[4])}\nFailed Extensions: {len(prep[5])}")
client.run(os.getenv("token"))