import aiohttp
import datetime
import asyncio


async def get_weather(city: str, api_key: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric") as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

def format_weather_message(weather_data):
    city = weather_data["name"]
    temp = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    message = f"La météo de {city} aujourd'hui:\n\nTempérature: {temp}°C\nDescription: {description}"
    return message

async def send_weather_report(bot, channel_id: int, city: str, api_key: str):
    while True:
        now = datetime.datetime.now()
        if now.hour == 8 and now.minute == 0:  # l'heure d'envoi du rapport météo
            weather_data = await get_weather(city, api_key)
            if weather_data:
                message = format_weather_message(weather_data)
                channel = bot.get_channel(channel_id)
                await channel.send(message)

        await asyncio.sleep(60)  # Attendre 60 secondes avant de vérifier à nouveau l'heure
