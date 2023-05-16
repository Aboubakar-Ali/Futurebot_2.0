from .construction import questions_answers, current_question, question_asker, wrong_attempts, user_wrong_attempts, authorized_channel_id, ask_for_another_question
import random

def setup(bot):
    @bot.command(name="devinette")
    async def devinette(ctx):
        global current_question, question_asker, wrong_attempts

        if ctx.channel.id != authorized_channel_id:
            await ctx.send("Cette commande ne peut être utilisée que dans le salon autorisé.")
            return

        if current_question:
            await ctx.send("Un jeu de devinette est déjà en cours.")
            return

        question_asker = ctx.author
        current_question = random.choice(list(questions_answers.keys()))
        wrong_attempts = 0
        await ctx.send(f"Voici la question: {current_question}")

    @bot.command(name="reponse")
    async def reponse(ctx, *, user_answer: str):
        global current_question, question_asker

        if not current_question:
            await ctx.send("Aucun jeu de devinette en cours. Utilisez la commande `!devinette` pour commencer un jeu.")
            return

        correct_answer = questions_answers[current_question].lower()

        if ctx.author not in user_wrong_attempts:
            user_wrong_attempts[ctx.author] = 0

        if user_answer.lower() == correct_answer or user_wrong_attempts[ctx.author] >= 1:
            if user_answer.lower() != correct_answer:
                await ctx.send(f"Malheureusement, vous avez épuisé vos deux essais. La bonne réponse était : {correct_answer}")
            else:
                await ctx.send(f"{ctx.author.mention} a donné la bonne réponse ! Félicitations !")
            
            await ctx.send("Voulez-vous une autre question ? Répondez par 'oui' ou 'non'.")
            
            current_question = None
            question_asker = None
            user_wrong_attempts[ctx.author] = 0
            
            if await ask_for_another_question(bot, ctx):
                await devinette(ctx)

            else:
                await ctx.send("Merci d'avoir joué !")
        else:
            user_wrong_attempts[ctx.author] += 1
            await ctx.send("Ce n'est pas la bonne réponse. Essayez encore !")
