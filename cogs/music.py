from discord import FFmpegPCMAudio, Embed, Colour
from discord.ext import commands, tasks
from modules.ytdl import YTDLSource

from datetime import datetime
import lyricsgenius
import os

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.genius = lyricsgenius.Genius(os.getenv("GENIUS_API_TOKEN"))
        self.queue = []
    
    @commands.command()
    async def play(self, ctx, url=""):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
        else:
            return await ctx.send("You are not in a voice channel! Join one to listen to me, ok? ;-;")
        
        print("ogey we got the channel")
        if ctx.voice_client:
            if not ctx.voice_client.is_playing():
                await ctx.voice_client.move_to(channel)
            else:
                async with ctx.typing():
                    player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                    self.queue.append(player)
                    self.queue.pop(0)
                
                return await ctx.send("Added the song to a queue! :FubukiHai:")
        else:
            await channel.connect()
        
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        
        await ctx.send(f"Okie! We are playing **{player.title}** now! >w<")
        if not self.play_queue.is_running():
            await self.play_queue.start(ctx)
    
    @commands.command()
    async def lyrics(self, ctx, *, title):
        song = self.genius.search_song(title)
        
        if not song:
            return await ctx.send("Sorry, i couldn't find lyrics to that song :c")
            
        embed = Embed(
            title=song.artist + " - " + song.title,
            description=song.lyrics,
            timestamp=datetime.now(),
            colour=Colour.green()      
        )
        embed.set_footer(
            text=f"Invoked by {str(ctx.author)}",
            icon_url=ctx.author.avatar_url
        )
        
        await ctx.send(embed=embed)
        
    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
     
    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        
    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
    
    @tasks.loop(seconds=1)
    async def play_queue(self, ctx):
        if ctx.voice_client.is_playing():
            return
        
        if not self.queue:
            return self.play_queue.stop()

        player = self.queue[0]
        self.queue.pop(0)
        
        async with ctx.typing():
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        
        await ctx.send(f"Okie! We are playing **{player.title}** now! >w<")

    @commands.command()
    async def queue(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Music(bot))