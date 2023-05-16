import discord
from discord.ext import commands
import configs

# import historique
from structures.module1 import CommandHistory
from structures.module2 import queue
from bot.events import   user_histories_file, user_histories, ignored_commands
from commands.file_utils import load_data_from_json, save_data_to_json
from commands.focus import setup as focus_setup
from commands.back import setup as back_setup
from commands.delete import setup as delete_setup
from commands.forward import setup as forward_setup
from commands.history import setup as history_setup
from commands.last import setup as last_setup
from commands.clear_history import setup as clear_history_setup
from bot.events import setup as events_setup

# import arbre
from arbrebinaire.helps import setup as helps_setup
from arbrebinaire.python import setup as python_setup
from arbrebinaire.bases import setup as bases_setup
from arbrebinaire.java import setup as java_setup
from arbrebinaire.no import setup as no_setup
from arbrebinaire.reset import setup as reset_setup
from arbrebinaire.speack import setup as speack_setup
from arbrebinaire.ultim import setup as ultim_setup
from arbrebinaire.yes import setup as yes_setup

# import sondages
from polls.poll_commands import setup as commands_setup
from polls.poll_events import setup as cevents_setup

# import Titanic survivor
from titanic.commands import setup as survivor

# import devinette 
from devinette.commands import setup as commands_devinette

# Création des intents pour le bot
intents = discord.Intents.all()
intents.members = True

# Création de l'objet bot avec le préfixe de commande et les intents
bot = commands.Bot(command_prefix='!', intents=intents)

#charge le fichier json
user_histories_data = load_data_from_json(user_histories_file)

for hashed_id, history_data in user_histories_data.items():
    user_histories.append(hashed_id, CommandHistory.from_dict(history_data))

# Création d'instances des modules personnalisés pour le bot
bot.command_queue = queue("première commande")

# ajout à la liste d'attentes avant l'exécution
@bot.before_invoke
async def before_any_command(ctx):
    if not ctx.command.name in ignored_commands:
        bot.command_queue.append(ctx)
        await ctx.send("Votre commande est dans la liste d'attente.")


# Setup des commandes history
focus_setup(bot)
back_setup(bot, user_histories)
delete_setup(bot)
forward_setup(bot, user_histories)
history_setup(bot, user_histories)
last_setup(bot, user_histories)
clear_history_setup(bot, user_histories, save_data_to_json, user_histories_file)

# Setup des commandes de l'arbre
helps_setup(bot)
python_setup(bot)
bases_setup(bot)
java_setup(bot)
no_setup(bot)
reset_setup(bot)
speack_setup(bot)
ultim_setup(bot)
yes_setup(bot)


# Setup des commandes et des evenement du sondages
commands_setup(bot)
cevents_setup(bot)

# Setup des commandes de devinette
commands_devinette(bot)

# Setup des commandes de Titanic
survivor(bot)

# Setup des événements bot
events_setup(bot)



# Lancement du bot 
bot.run(configs.api_key)

