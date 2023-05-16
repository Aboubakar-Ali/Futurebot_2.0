from discord.ext import commands
from .construction import question_tree

def setup(bot):
    @bot.command(name="avancés")
    async def advanced(ctx):
        question_tree.traverse_right()
        answer = question_tree.get_current_question()
        await ctx.send(answer)

