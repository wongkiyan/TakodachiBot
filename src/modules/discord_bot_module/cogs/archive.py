from discord.ext.commands import Cog, hybrid_command
from src.modules.archive_module import archive

class Archive(Cog):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_command(name='savel')
    async def archive_live_stream(self, ctx, url):
        """ 保存直播: url """
        await archive.archive_live_stream(ctx, url)

    @hybrid_command(name='savev')
    async def archive_video(self, ctx, url):
        """ 保存影片: """
        await archive.archive_video(ctx, url)

async def setup(bot):
    await bot.add_cog(Archive(bot))