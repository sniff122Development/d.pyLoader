import logging
import discord
from discord.ext import commands
import discord.commands
import json
import os
import traceback


# Setup logging, logging level INFO and set format
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')


# Load config file as a dict
with open("config.json", "r") as f:
    config = json.load(f)


# Create bot instance with prefix from config.json
logger.info("Creating bot instance")
bot = discord.Bot()
bot.config = config # Set config on bot so it can be used within cogs, etc


# Load all commands in the 'commands' directory
for command_extension in [f.replace('.py', '') for f in os.listdir("commands") if os.path.isfile(os.path.join("commands", f))]:
    try:
        bot.load_extension("commands." + command_extension)
        logger.info(f"CogManager: Loaded command: '{command_extension}")
    except (discord.ClientException, ModuleNotFoundError):
        logging.warning(f"CogManager: Failed to load command: '{command_extension}'")
        traceback.print_exc()


# Load all events in the 'events' directory
for event_extension in [f.replace('.py', '') for f in os.listdir("events") if os.path.isfile(os.path.join("events", f))]:
    try:
        bot.load_extension("events." + event_extension)
        logger.info(f"CogManager: Loaded event: '{event_extension}")
    except (discord.ClientException, ModuleNotFoundError):
        logging.warning(f"CogManager: Failed to load event: '{event_extension}'")
        traceback.print_exc()


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, e):
    if isinstance(e, discord.ext.commands.errors.NotOwner):
        await ctx.send_response("You need to be the bot owner to use this command!")


# Reloads all cogs
@bot.slash_command(name="reloadall", guild_ids=[838494915314712607])
@commands.is_owner()
async def _reload_all_command(ctx: discord.ApplicationContext):
    await ctx.send_response("Reloading...")

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
        except discord.ExtensionNotFound:
            logging.info(f"CogManager: Command '{command_extension}' was not previously loaded! New cog? If so this can be safely ignored")
            pass
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
        except discord.ExtensionNotFound:
            logging.info(f"CogManager: Event '{command_extension}' was not previously loaded! New cog? If so this can be safely ignored")
        except (discord.ClientException, ModuleNotFoundError) as e:
            await ctx.send(f"Failed to load extension {event_extension}\n{e}")
            logging.warning(f'CogManager: Failed to load extension {event_extension}.')
            traceback.print_exc()
            return

    msgcontent = f"Reload Complete!\nLoaded Commands: \n```\n{LoadedCommands}```\nLoaded Events: \n```\n{LoadedEvents}```"
    await ctx.send_followup(msgcontent)


# Log into discord using the token from config.json
logger.info("Attempting to login to Discord")
try:
    bot.run(bot.config["token"])
except Exception as e:
    logging.fatal("Failed to login to Discord")
    raise
