import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import configs


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
async def send_motivation_quote(bot):
    quote = await get_random_motivation_quote()
    channel = bot.get_channel(configs.salon_citation)
    await channel.send(quote)




# Planifier de l'envoi de citations 
scheduler = AsyncIOScheduler()
scheduler.start()
