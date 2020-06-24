from discord.ext import commands
import discord


class CommandExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="example")
    async def _example_command(self, ctx):
        await ctx.send("Got that!")


def setup(bot):
    bot.add_cog(CommandExample(bot))
