import hashlib

def hash_user_id(user_id):
    hasher = hashlib.sha256()
    hasher.update(str(user_id).encode())
    hashed_id = hasher.hexdigest()
    return hashed_id

def setup(bot, user_histories):
    @bot.command(name="lastcmd")
    async def last_command(ctx):
        hashed_id = hash_user_id(ctx.author.id)
        history = user_histories.get(hashed_id)
        if not history:
            await ctx.send("Aucune commande dans l'historique.")
        else:
            last_cmd = history.get_last_command()
            await ctx.send(f"Dernière commande : {last_cmd}")
