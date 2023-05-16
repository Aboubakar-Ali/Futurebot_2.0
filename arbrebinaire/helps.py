from discord.ext import commands
from .construction import question_tree

def setup(bot):
    @bot.command(name="helps")
    async def helps(ctx):
        question = question_tree.get_current_question()
        await ctx.send(question)
