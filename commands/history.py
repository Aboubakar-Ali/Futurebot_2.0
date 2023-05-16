import hashlib

def hash_user_id(user_id):
    hasher = hashlib.sha256()
    hasher.update(str(user_id).encode())
    hashed_id = hasher.hexdigest()
    return hashed_id

def setup(bot, user_histories):
    @bot.command(name="history")
    async def history(ctx):
        hashed_id = hash_user_id(ctx.author.id)
        user_history = user_histories.get(hashed_id)
        if user_history is None:
            await ctx.send("Aucun historique trouvé.")
            return

        history = user_history.get_all_commands()
        if not history:
            await ctx.send("Aucun historique trouvé.")
            return

        history_string = "\n".join(history)
        await ctx.send(f"Voici votre historique de commandes:\n```\n{history_string}\n```")
