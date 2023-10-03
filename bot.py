# Basic bot dependencies
import discord
from discord.ext.commands import Bot
import platform

# Import configurations
import configs

# Modules import - this imports all modules under the modules directory
# IDEs will complain about unresolved references, but it runs as intended
from modules import archive_module

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Bot(description=configs.BOT_DESCRIPTION, command_prefix=configs.BOT_PREFIX, intents=intents)

@client.event
async def on_ready():
    print('--------')
    print('Takodachi Bot')
    print('--------')
    print('Logged in as ' + client.user.name + ' (ID:' + str(client.user.id) + ') | Connected to '
        + str(len(client.guilds)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Github Link: --')
    print('--------')
    print('Reference: https://github.com/CedArctic/Chimera')
    print('--------')
    return await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Ina's back"))

@client.command()
async def savel(ctx, command):
    await archive_module.archive_live_stream(ctx, command)

@client.command()
async def savev(ctx, command):
    await archive_module.archive_video(ctx, command)