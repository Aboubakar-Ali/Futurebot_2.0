from discord.ext import commands
from .construction import question_tree

def setup(bot):
    @bot.command(name="python")
    async def python(ctx):
        question_tree.traverse_left()
        question = question_tree.get_current_question()
        await ctx.send(question)