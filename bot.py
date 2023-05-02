import discord
from discord.ext import commands, tasks
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
import config

from module1 import CommandHistory
from module2 import queue
from module3 import *

# Création des intents pour le bot
intents = discord.Intents.all()
intents.members = True

# Création de l'objet bot avec le préfixe de commande et les intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Création d'instances des modules personnalisés pour le bot
bot.command_queue = queue("première commande")

# Création d'un dictionnaire pour stocker les historiques des commandes pour chaque utilisateur
user_histories = {}

# liste des commandes à ignorer
ignored_commands = ["!lastcmd", "!forward", "!back", "!history", "!clear_history"]

################################################ Création de l'arbre binaire #################################################################

root = BinaryTreeNode("Quel langage de programmation souhaitez-vous apprendre (Python ou Java) ?")
left_child = BinaryTreeNode("Voulez-vous apprendre les bases de Python ou les concepts avancés ?")
right_child = BinaryTreeNode("Voulez-vous apprendre les bases de Java ou les concepts avancés ?")
python_basic = BinaryTreeNode("Vous pouvez commencer par le cours Python pour les débutants. Voulez-vous que je vous propose des liens ?")
python_advanced = BinaryTreeNode("Vous pouvez consulter le cours Python avancé. Voulez-vous que je vous propose des liens ?")
java_basic = BinaryTreeNode("Vous pouvez commencer par le cours Java pour les débutants. Voulez-vous que je vous propose des liens ?")
java_advanced = BinaryTreeNode("Vous pouvez consulter le cours Java avancé. Voulez-vous que je vous propose des liens ?")

root.left = left_child
root.right = right_child
left_child.left = python_basic
left_child.right = python_advanced
right_child.left = java_basic
right_child.right = java_advanced

question_tree = BinaryTree(root)


############################################################## Commandes de Bases ################################################################################

# Définition d'un événement pour quand le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    await send_motivation_quote() #teste de l'envoi de la citation

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
        user_id = ctx.author.id
        if user_id not in user_histories:
            user_histories[user_id] = CommandHistory()
        user_histories[user_id].add_command(ctx.message.content)
                
@bot.command(name="history")
async def history(ctx):
    user_id = ctx.author.id
    if user_id not in user_histories:
        await ctx.send("Aucune commande dans l'historique.")
    else:
        commands_str = str(user_histories[user_id])
        await ctx.send(f"Voici toutes les commandes que vous avez entrées :\n```{commands_str}```")

#
@bot.command(name="lastcmd")
async def last_command(ctx):
    user_id = ctx.author.id
    if user_id not in user_histories:
        await ctx.send("Aucune commande dans l'historique.")
    else:
        last_cmd = user_histories[user_id].get_last_command()
        await ctx.send(f"Dernière commande : {last_cmd}")

#
@bot.command(name="back")
async def back(ctx):
    user_id = ctx.author.id
    if user_id not in user_histories:
        await ctx.send("Début de l'historique atteint.")
    else:
        command = user_histories[user_id].move_backward()
        if command:
            await ctx.send(f"Dernière commande : {command}")
        else:
            await ctx.send("Début de l'historique atteint.")

#
@bot.command(name="forward")
async def forward(ctx):
    user_id = ctx.author.id
    if user_id not in user_histories:
        await ctx.send("Fin de l'historique atteint.")
    else:
        command = user_histories[user_id].move_forward()
        if command:
            await ctx.send(f"Dernière commande : {command}")
        else:
            await ctx.send("Fin de l'historique atteint.")

#
@bot.command(name="clear_history")
async def clear_history(ctx):
    user_id = ctx.author.id
    if user_id in user_histories:
        user_histories[user_id].clear()
    await ctx.send("L'historique a été supprimé.")

########################################################### datetime ############################################################################

# Affichage de la date et de l'heure actuelles
@bot.command(name="datetime")
async def current_datetime(ctx):
    now = datetime.datetime.now()
    await ctx.send(f"La date et l'heure actuelles sont : {now.strftime('%Y-%m-%d %H:%M:%S')}")



######################################################## API message motivation ##################################################################
 
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



####################################################### Commandes arbre ###########################################################################


@bot.command(name="helps")
async def helps(ctx):
    question = question_tree.get_current_question()
    await ctx.send(question)

@bot.command(name="python")
async def python(ctx):
    question_tree.traverse_left()
    question = question_tree.get_current_question()
    await ctx.send(question)

@bot.command(name="java")
async def java(ctx):
    question_tree.traverse_right()
    question = question_tree.get_current_question()
    await ctx.send(question)

@bot.command(name="bases")
async def bases(ctx):
    question_tree.traverse_left()
    answer = question_tree.get_current_question()
    await ctx.send(answer)

@bot.command(name="avancés")
async def advanced(ctx):
    question_tree.traverse_right()
    answer = question_tree.get_current_question()
    await ctx.send(answer)

@bot.command(name="reset")
async def reset(ctx):
    question_tree.reset()
    question = question_tree.get_current_question()
    await ctx.send("La conversation a été réinitialisée.")
    await ctx.send(question)


@bot.command(name="oui")
async def oui(ctx):
    if question_tree.current_node == python_basic:
        links = "Voici quelques liens pour apprendre les bases de Python :\nOpenclassrooms: https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python\nW3Schools: https://www.w3schools.com/python/"
    elif question_tree.current_node == python_advanced:
        links = "Voici quelques liens pour apprendre les concepts avancés de Python :\nOpenclassrooms: https://openclassrooms.com/fr/courses/4425111-apprenez-a-creer-votre-site-web-avec-html5-et-css3\nW3Schools: https://www.w3schools.com/python/"
    elif question_tree.current_node == java_basic:
        links = "Voici quelques liens pour apprendre les bases de Java :\nOpenclassrooms: https://openclassrooms.com/fr/courses/26832-apprenez-a-programmer-en-java\nW3Schools: https://www.w3schools.com/java/"
    elif question_tree.current_node == java_advanced:
        links = "Voici quelques liens pour apprendre les concepts avancés de Java :\nOpenclassrooms: https://openclassrooms.com/fr/courses/2654566-decouvrez-les-fonctionnalites-avancees-de-java\nW3Schools: https://www.w3schools.com/java/"
    else:
        links = "Je ne peux pas vous donner de liens pour le moment."
    await ctx.send(links)
    await ctx.send("Bonne chance dans votre apprentissage !")
    question_tree.reset()

@bot.command(name="non")
async def non(ctx):
    await ctx.send("N'hésitez pas à revenir vers moi si vous avez besoin d'aide.")
    question_tree.reset()

@bot.command(name="speak")
async def speak(ctx, subject: str):
    supported_languages = ["python", "java"]
    if subject.lower() in supported_languages:
        await ctx.send(f"Oui, je parle de {subject.capitalize()}.")
    else:
        await ctx.send(f"Désolé, je ne parle pas de {subject.capitalize()}.")


#################################################################################################################""

# Lancement du bot 
bot.run(config.api_key)



