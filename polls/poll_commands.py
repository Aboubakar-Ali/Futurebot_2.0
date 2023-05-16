from .poll_data import save_data_to_json, polls, poll_names
import collections

POLL_CHANNEL_ID = 1105439720063905803 

def setup(bot):
    # Commande pour créer un sondage
    @bot.command(name="create_poll")
    async def create_poll(ctx, name: str, max_votes: int, question: str, *choices: str):
        # Vérification du salon
        if ctx.channel.id != POLL_CHANNEL_ID:
            await ctx.send("Vous ne pouvez pas créer un sondage dans ce salon.")
            return

        if len(choices) < 2:
            await ctx.send("Veuillez fournir au moins deux choix pour le sondage.")
            return
        if len(choices) > 10:
            await ctx.send("Veuillez fournir au maximum dix choix pour le sondage.")
            return
        if max_votes < 1 or max_votes > len(choices):
            await ctx.send(f"Veuillez fournir un nombre valide de votes maximum entre 1 et {len(choices)}.")
            return

        # Liste des émojis de numéros pour les réactions
        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        # Création et envoi du message de sondage
        poll_message = f"**Sondage créé par {ctx.author.display_name}**\n\n{question}\n\n"
        for i, choice in enumerate(choices, 1):
            poll_message += f"{number_emojis[i-1]} {choice}\n"
        poll_message += f"\nVous pouvez voter pour un maximum de {max_votes} choix."
        sent_message = await ctx.send(poll_message)

        # Ajout des réactions au message de sondage
        for i in range(len(choices)):
            await sent_message.add_reaction(number_emojis[i])

        # Enregistrement du sondage
        polls[sent_message.id] = (ctx.author.id, max_votes, {})
        poll_names[name.lower()] = sent_message.id
        save_data_to_json("polls.json", polls)


        save_data_to_json("polls.json", polls)
        save_data_to_json("poll_names.json", poll_names)

    @bot.command(name="result")
    async def result(ctx, poll_name: str):
        poll_name = poll_name.lower()
        if poll_name not in poll_names:
            await ctx.send("Aucun sondage avec ce nom n'a été trouvé.")
            return

        message_id = poll_names[poll_name]
        if message_id not in polls:
            await ctx.        send("Le sondage demandé n'a pas été trouvé.")
            return

        _, _, user_votes = polls[message_id]
        results = collections.Counter()
        for votes in user_votes.values():
            for vote in votes:
                results[vote] += 1

        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        result_message = f"Résultats du sondage '{poll_name}':\n\n"
        for emoji, count in results.items():
            result_message += f"{emoji} : {count} vote(s)\n"

        await ctx.send(result_message)
