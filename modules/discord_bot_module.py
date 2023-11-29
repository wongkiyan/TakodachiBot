# Basic bot dependencies
import discord
from discord.ext.commands import Bot
import platform
import asyncio

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import configs as Configs

# Modules import
from modules import archive_module

from library.services.module_service import ModuleService

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Bot(description=Configs.BOT_DESCRIPTION,command_prefix=Configs.BOT_PREFIX, intents=intents)

discord_loop = asyncio.new_event_loop()
asyncio.set_event_loop(discord_loop)

@client.event
async def on_ready():
    print('--------')
    print('Good morning, after noon, evening! It is tako time. Wah! How are you today?')
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

class DiscordBotService(ModuleService):
    def start_service(self):
        asyncio.run_coroutine_threadsafe(client.start(Configs.BOT_TOKEN), discord_loop)
        discord_loop.run_forever()

    def stop_service(self):
        if not client.is_closed():
            asyncio.run_coroutine_threadsafe(client.close(), discord_loop)
        client.clear()
        print()
        print("Discord Bot closed")
        discord_loop.stop()

    def is_running(self):
        return client.is_ready()

if __name__ == "__main__":
    discord_bot_service = DiscordBotService()
    discord_bot_service.start_service()
