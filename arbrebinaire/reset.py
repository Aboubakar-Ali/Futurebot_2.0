from discord.ext import commands
from .construction import question_tree

def setup(bot):
    @bot.command(name="reset")
    async def reset(ctx):
        question_tree.reset()
        question = question_tree.get_current_question()
        await ctx.send("La conversation a été réinitialisée.")
        await ctx.send(question)

