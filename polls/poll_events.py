from .poll_data import save_data_to_json, polls

def setup(bot):
    @bot.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return

        if reaction.message.id in polls:
            author_id, max_votes, user_votes = polls[reaction.message.id]

            if user.id not in user_votes:
                user_votes[user.id] = [reaction.emoji]
            else:
                if len(user_votes[user.id]) >= max_votes:
                    await reaction.remove(user)
                else:
                    user_votes[user.id].append(reaction.emoji)

        save_data_to_json("polls.json", polls)

    @bot.event
    async def on_reaction_remove(reaction, user):
        if user.bot:
            return

        if reaction.message.id in polls:
            _, _, user_votes = polls[reaction.message.id]

            if user.id in user_votes and reaction.emoji in user_votes[user.id]:
                user_votes[user.id].remove(reaction.emoji)
