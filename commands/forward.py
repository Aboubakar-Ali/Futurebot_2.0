import hashlib

def hash_user_id(user_id):
    hasher = hashlib.sha256()
    hasher.update(str(user_id).encode())
    hashed_id = hasher.hexdigest()
    return hashed_id

def setup(bot, user_histories):
    @bot.command(name="forward")
    async def forward(ctx):
        hashed_id = hash_user_id(ctx.author.id)
        history = user_histories.get(hashed_id)
        if not history:
            await ctx.send("Fin de l'historique atteint.")
        else:
            command = history.move_forward()
            if command:
                await ctx.send(f"Dernière commande : {command}")
            else:
                await ctx.send("Fin de l'historique atteint.")
