def setup(bot):
    @bot.command(name="focus")
    async def focus(ctx):
        await ctx.send("Restez concentré")
