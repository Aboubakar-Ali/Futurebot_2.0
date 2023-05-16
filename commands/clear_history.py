import hashlib

def hash_user_id(user_id):
    hasher = hashlib.sha256()
    hasher.update(str(user_id).encode())
    hashed_id = hasher.hexdigest()
    return hashed_id

def setup(bot, user_histories, save_data_to_json, user_histories_file):
    @bot.command(name="clear_history")
    async def clear_history(ctx):
        hashed_id = hash_user_id(ctx.author.id)
        history = user_histories.get(hashed_id)
        if history:
            # Clear the history in the bot
            history.clear()
            # Also remove the history from the user_histories hashmap
            user_histories.remove(hashed_id)

            # Update the user_histories_data dictionary
            user_histories_data = {}
            for sublist in user_histories.datas:
                for hashed_id, history in sublist:
                    user_histories_data[hashed_id] = history.to_dict()

            # Save the updated data to the JSON file
            save_data_to_json(user_histories_file, user_histories_data)
            
            await ctx.send("L'historique a été supprimé.")
        else:
            await ctx.send("Aucun historique à supprimer.")

