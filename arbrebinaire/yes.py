from discord.ext import commands
from .construction import question_tree, python_basic, python_advanced, java_basic, java_advanced

def setup(bot):
    @bot.command(name="oui")
    async def oui(ctx):
        if question_tree.current_node == python_basic:
            links = "Voici quelques liens pour apprendre les bases de Python :\nOpenclassrooms: https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python\nW3Schools: https://www.w3schools.com/python/"
        elif question_tree.current_node == python_advanced:
            links = "Voici quelques liens pour apprendre les concepts avancés de Python :\nOpenclassrooms: https://openclassrooms.com/fr/courses/4425111-apprenez-a-creer-votre-site-web-avec-html5-et-css3\nW3Schools: https://www.w3schools.com/python/"
        elif question_tree.current_node == java_basic:
            links = "Voici quelques liens pour apprendre les bases de Java :\nOpenclassrooms: https://openclassrooms.com/fr/courses/26832-apprenez-a-programmer-en-java\nW3Schools: https://www.w3schools.com/java/"
        elif question_tree.current_node == java_advanced:
            links = "Voici quelques liens pour apprendre les concepts avancés de Java :\nOpenclassrooms: https://openclassrooms.com/fr/courses/2654566-decouvrez-les-fonctionnalites-avancees-de-java\nW3Schools: https://www.w3schools.com/java/"
        else:
            links = "Je ne peux pas vous donner de liens pour le moment."
        await ctx.send(links)
        await ctx.send("Bonne chance dans votre apprentissage !")
        question_tree.reset()

