def setup(bot):
    @bot.command(name="del")
    async def delete(ctx):
        await ctx.channel.purge(limit=10)
