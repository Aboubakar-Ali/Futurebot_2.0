from discord.ext import commands
from .construction import question_tree

def setup(bot):
    @bot.command(name="java")
    async def java(ctx):
        question_tree.traverse_right()
        question = question_tree.get_current_question()
        await ctx.send(question)

