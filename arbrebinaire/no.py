from discord.ext import commands
from .construction import question_tree, python_basic, python_advanced, java_basic, java_advanced

def setup(bot):
    @bot.command(name="non")
    async def non(ctx):
        await ctx.send("N'hésitez pas à revenir vers moi si vous avez besoin d'aide.")
        question_tree.reset()
