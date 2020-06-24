from discord.ext import commands
import discord


class EventExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot online")


def setup(bot):
    bot.add_cog(EventExample(bot))
