from commands.hash import hash_user_id
from structures.module1 import CommandHistory
from commands.file_utils import  save_data_to_json
from structures.module4 import hashmap
import configs
from meteo.weather_api import *
from citation.motivation_api import send_motivation_quote
from citation.motivation_api import scheduler



# Création d'un dictionnaire pour stocker les historiques des commandes pour chaque utilisateur
user_histories = hashmap(1000)

ignored_commands = ["lastcmd", "forward", "back", "history", "clear_history"]

# fichier json
user_histories_file = "user_histories.json"


def setup(bot):

    # Définition d'un événement pour quand le bot est prêt
    @bot.event
    async def on_ready():
        
        print(f"{bot.user.name} has connected to Discord!")
        await send_motivation_quote(bot) #teste de l'envoi de la citation
        # envoi de la citation  6h du matin
        scheduler.add_job(send_motivation_quote, 'cron', hour=6, minute=0, args=(bot,))


        # Envoi immédiat de la météo
        weather_data = await get_weather("Paris", configs.api_keymeteo)
        if weather_data:
            message = format_weather_message(weather_data)
            channel = bot.get_channel(configs.salon_meteo)
            await channel.send(message)

        # Planification de l'envoi de la météo tous les matins
        asyncio.create_task(send_weather_report(bot, configs.salon_meteo, "Paris", configs.api_keymeteo))

    @bot.event
    async def on_command(ctx):
        hashed_id = hash_user_id(ctx.author.id)
        if user_histories.get(hashed_id) is None:
            user_histories.append(hashed_id, CommandHistory())


    @bot.event
    async def on_command_completion(ctx):
        if ctx.command.name in ignored_commands:
            return

        hashed_id = hash_user_id(ctx.author.id)
        user_histories.get(hashed_id).add_command(ctx.message.content)

        user_histories_data = {}
        for sublist in user_histories.datas:
            for hashed_id, history in sublist:
                user_histories_data[hashed_id] = history.to_dict()

        save_data_to_json(user_histories_file, user_histories_data)
