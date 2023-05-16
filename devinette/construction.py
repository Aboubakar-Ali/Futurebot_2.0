import asyncio

questions_answers = {
    "Quelle est la capitale de la France ?": "paris",
    "Combien de pattes a un chat ?": "4",
    "Quel est le plus grand océan du monde ?": "pacifique",
    "Quel est le plus petit pays du monde ?": "vatican",
    "Quel est le plus long fleuve du monde ?": "nil",
    "Quel pays est surnommé le pays du soleil levant ?": "japon",
    "Qui a peint La Joconde ?": "léonard de vinci",
    "Quel est l'élément chimique représenté par le symbole O ?": "oxygène",
    "Quelle est la distance moyenne entre la Terre et la Lune ?": "384400",
    "Quel est le nom du dieu grec de la foudre ?": "zeus",
    "Quel est l'os le plus long du corps humain ?": "fémur",
    "Combien y a-t-il de continents sur Terre ?": "7",
    "Quel est le nom de la plus grande île du monde ?": "groenland",
    "Quel est l'animal le plus rapide du monde ?": "guépard",
    "Qui a écrit Le Petit Prince ?": "antoine de saint-exupéry",
    "Quelle est la planète la plus proche du Soleil ?": "mercure",
    "Quel est le nom du pharaon égyptien dont le tombeau a été découvert en 1922 ?": "toutânkhamon",
    "Quelle est la devise de la France ?": "liberté, égalité, fraternité",
    "Quel est le plus haut sommet du monde ?": "mont everest",
    "Qui est le dieu romain de la guerre ?": "mars",
    "Quel est l'élément chimique représenté par le symbole Au ?": "or",
    "Quel est le nom du célèbre mathématicien grec auteur de l'élément ?": "euclide",
    "Quel est le plus grand désert du monde ?": "antarctique",
    "Quel est le nom du processus par lequel les plantes produisent de la nourriture à partir de la lumière solaire ?": "photosynthèse",
    "Quel est le nom du célèbre savant qui a développé la théorie de la relativité ?": "albert einstein",
    "Quel est le nom de l'océan situé entre l'Afrique et l'Australie ?": "océan indien",
    "Quelle est la capitale du Brésil ?": "brasília",
    "Quel est le nom de la célèbre théorie de l'évolution de Charles Darwin ?": "sélection naturelle",
    "Quel est le plus grand pays d'Amérique du Sud ?": "brésil",
    "Quel est le nom du célèbre peintre néerlandais auteur de La Nuit étoilée ?": "vincent van gogh"
}


current_question = None
question_asker = None
wrong_attempts = 0
user_wrong_attempts = {}
authorized_channel_id = 1103302296571494420

async def ask_for_another_question(bot, ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "oui" or m.content.lower() == "non")

    try:
        response = await bot.wait_for("message", check=check, timeout=30)
        return response.content.lower() == "oui"
    except asyncio.TimeoutError:
        return False

