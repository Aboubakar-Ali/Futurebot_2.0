import discord
from discord.ext import commands, tasks
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
import config

from module1 import CommandHistory
from module2 import queue

# Création des intents pour le bot
intents = discord.Intents.all()
intents.members = True

# Création de l'objet bot avec le préfixe de commande et les intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Création d'instances des modules personnalisés pour le bot
bot.history = CommandHistory()
bot.command_queue = queue("première commande")

ignored_commands = ["!lastcmd", "!forward", "!back", "!history", "!clear_history"]


# Définition d'un événement pour quand le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    # await send_motivation_quote() #teste de l'envoi de la citation

# Définition d'une commande pour supprimer les messages en masse(limitation à 10)
@bot.command(name="del")
async def delete(ctx):
    await ctx.channel.purge(limit=10)

# Commande servant de test
@bot.command(name="focus")
async def focus(ctx):
    await ctx.send("Restez concentré")

# ajout à la liste d'attentes avant l'exécution
@bot.before_invoke
async def before_any_command(ctx):
    if not ctx.command.name in ignored_commands:
        bot.command_queue.append(ctx)
        await ctx.send("Votre commande est dans la liste d'attente.")

@bot.event
async def on_command_completion(ctx):
    if ctx.message.content not in ignored_commands:
        bot.history.add_command(ctx.message.content)

# Commande pour afficher l'historique des commandes
@bot.command(name="history")
async def history(ctx):
    commands = bot.history.get_all_commands()
    if commands == "Pas d'historique":
        await ctx.send("Aucune commande dans l'historique.")
    else:
        commands_str = "\n".join(commands)
        await ctx.send(f"Voici toutes les commandes que vous avez entrées :\n```{commands_str}```")

# Commande pour afficher la dernière commande
@bot.command(name="lastcmd")
async def last_command(ctx):
    last_cmd = bot.history.get_last_command()
    if last_cmd == "Pas d'historique":
        await ctx.send("Aucune commande dans l'historique.")
    else:
        await ctx.send(f"Dernière commande : {last_cmd}")

# Commande pour revenir en arrière dans l'historique des commandes
@bot.command(name="back")
async def back(ctx):
    command = bot.history.move_backward()
    if command:
        await ctx.send(f"Dernière commande : {command}")
    else:
        await ctx.send("Début de l'historique atteint.")

# Commande pour avancer dans l'historique des commandes
@bot.command(name="forward")
async def forward(ctx):
    command = bot.history.move_forward()
    if command:
        await ctx.send(f"Dernière commande : {command}")
    else:
        await ctx.send("Fin de l'historique atteint.")

# Commande pour effacer l'historique des commandes
@bot.command(name="clear_history")
async def clear_history(ctx):
    bot.history.clear()
    await ctx.send("L'historique a été supprimé.")

# Affichage de la date et de l'heure actuelles
@bot.command(name="datetime")
async def current_datetime(ctx):
    now = datetime.datetime.now()
    await ctx.send(f"La date et l'heure actuelles sont : {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Récupération d'une citation motivante aléatoire
async def get_random_motivation_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://zenquotes.io/api/random") as response:
            if response.status == 200:
                quote_data = await response.json()
                quote = quote_data[0]["q"]
                author = quote_data[0]["a"]
                return f"{quote} - {author}"
            else:
                return "Erreur lors de la récupération de la citation."


# Envoi de la citation motivante
async def send_motivation_quote():
    quote = await get_random_motivation_quote()
    channel = bot.get_channel(1091337472782377002)
    await channel.send(quote)


# Planifier de l'envoi de citations 
scheduler = AsyncIOScheduler()
scheduler.add_job(send_motivation_quote, 'cron', hour=6, minute=0)
scheduler.start()


# Lancement du bot 
bot.run(config.api_key)



