from discord.ext import commands
from .construction import question_tree, python_basic, python_advanced, java_basic, java_advanced

def setup(bot):
    @bot.command(name="speak")
    async def speak(ctx, subject: str):
        supported_languages = ["python", "java"]
        if subject.lower() in supported_languages:
            await ctx.send(f"Oui, je parle de {subject.capitalize()}.")
        else:
            await ctx.send(f"Désolé, je ne parle pas de {subject.capitalize()}.")

