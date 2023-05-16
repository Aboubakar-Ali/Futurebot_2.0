from .constants import GUILD_ID, TITANIC_CHANNEL_ID, MAX_AGE
import aiohttp

def setup(bot):
    @bot.event
    async def on_member_join(member):
        if member.guild.id == GUILD_ID:
            channel = bot.get_channel(TITANIC_CHANNEL_ID)
            welcome_message = f"""
            
            Salut {member.mention}!
            Bienvenue dans le salon Titanic Survivor!

            Pour jouer, vous allez utiliser la commande suivante : 
            !titanic_survival age sex pclass embarked

            Les paramètres à entrer sont :
            - age : votre âge
            - sex : votre sexe (0 pour femme et 1 pour homme)
            - pclass : votre classe sur le bateau (1 pour première classe, 2 pour deuxième classe, 3 pour troisième classe)
            - embarked : votre point d'embarquement (0 pour Cherbourg, 1 pour Queenstown, 2 pour Southampton)

            Voici un exemple de commande :
            !titanic_survival 20 1 1 0
            Cela signifie que vous êtes un homme de 20 ans en première classe qui a embarqué à Cherbourg.

            Amusez-vous à essayer de survivre au Titanic!
            """
            await channel.send(welcome_message)

    @bot.command(name="titanic_survival")
    async def titanic_survival(ctx, age: int, sex: int, pclass: int, embarked: int):
        # Vérifier si la commande a été envoyée à partir du bon canal
        if ctx.channel.id != TITANIC_CHANNEL_ID:
            return

        # Normaliser l'âge
        age = age / MAX_AGE

        # Préparation des données à envoyer à l'API
        data = {
            "age": age,
            "sex": sex,
            "pclass": pclass,
            "embarked": embarked
        }

        # Envoi de la requête à l'API
        async with aiohttp.ClientSession() as session:
            async with session.post("http://127.0.0.1:5000/predict", json=data) as resp:
                # Vérification que la requête a réussi
                if resp.status != 200:
                    await ctx.send("Une erreur est survenue lors de la prédiction.")
                    return

                # Récupération et envoi de la prédiction
                prediction = await resp.json()
                survived = prediction["survived"]

                if survived:
                    await ctx.send("Selon le modèle, vous auriez survécu au Titanic.")
                else:
                    await ctx.send("Selon le modèle, vous n'auriez pas survécu au Titanic.")
