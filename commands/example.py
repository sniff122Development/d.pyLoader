from discord.commands import slash_command
import discord
from discord.ext import commands


class CommandExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="example")  # NOTE: may take up to an hour to register globally
    async def _example_command(self, ctx):
        await ctx.respond("Got it!")


def setup(bot):
    bot.add_cog(CommandExample(bot))
