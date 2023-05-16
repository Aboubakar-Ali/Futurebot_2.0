from discord.ext import commands
from .construction import question_tree

def setup(bot):
    @bot.command(name="bases")
    async def bases(ctx):
        question_tree.traverse_left()
        answer = question_tree.get_current_question()
        await ctx.send(answer)

