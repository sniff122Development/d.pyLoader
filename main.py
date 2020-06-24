import logging
import discord
from discord.ext import commands
import json
import os
import traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)s: %(message)s')


with open("config.json", "r") as f:
    config = json.load(f)

logger.info("Creating bot instance")
bot = commands.Bot(command_prefix=config["prefix"])
bot.config = config

for command_extension in [f.replace('.py', '') for f in os.listdir("commands") if os.path.isfile(os.path.join("commands", f))]:
    try:
        bot.load_extension("commands." + command_extension)
        logger.info(f"CogManager: Loaded command: '{command_extension}")
    except (discord.ClientException, ModuleNotFoundError):
        logging.warning(f"CogManager: Failed to load command: '{command_extension}'")
        traceback.print_exc()

for event_extension in [f.replace('.py', '') for f in os.listdir("events") if os.path.isfile(os.path.join("events", f))]:
    try:
        bot.load_extension("events." + event_extension)
        logger.info(f"CogManager: Loaded event: '{event_extension}")
    except (discord.ClientException, ModuleNotFoundError):
        logging.warning(f"CogManager: Failed to load event: '{event_extension}'")
        traceback.print_exc()


@commands.command(name="reloadall")
@commands.is_owner()
async def _reload_all_command(ctx):
    msg = await ctx.send("Reloading...")

    LoadedCommands = ""
    for command_extension in [f.replace('.py', '') for f in os.listdir("commands") if
                              os.path.isfile(os.path.join("commands", f))]:
        try:
            try:
                bot.unload_extension("commands." + command_extension)
            except:
                pass
            bot.load_extension("commands." + command_extension)
            logger.info(f"CogManager: Loaded command: '{command_extension}.py'")
            LoadedCommands = LoadedCommands + f"\n{command_extension}.py"
        except (discord.ClientException, ModuleNotFoundError) as e:
            await ctx.send(f"Failed to load command {command_extension}.py\n{e}")
            logging.warning(f'CogManager: Failed to load command {command_extension}.')
            traceback.print_exc()
            return

    LoadedEvents = ""
    for event_extension in [f.replace('.py', '') for f in os.listdir("events") if
                            os.path.isfile(os.path.join("events", f))]:
        try:
            try:
                bot.unload_extension("events." + event_extension)
            except:
                pass
            bot.load_extension("events." + event_extension)
            logger.info(f"CogManager: Loaded Event: '{event_extension}.py'")
            LoadedEvents = LoadedEvents + f"\n{event_extension}.py"
        except (discord.ClientException, ModuleNotFoundError) as e:
            await ctx.send(f"Failed to load extension {event_extension}\n{e}")
            logging.warning(f'CogManager: Failed to load extension {event_extension}.')
            traceback.print_exc()
            return

    msgcontent = f"Reload Complete!\nLoaded Commands: \n```\n{LoadedCommands}```\nLoaded Events: \n```\n{LoadedEvents}```"
    await msg.edit(content=msgcontent)


logger.info("Attempting to login to Discord")
try:
    bot.run(bot.config["token"])
except Exception as e:
    logging.critical("Failed to login to Discord")
    print(e)
