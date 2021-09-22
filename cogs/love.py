from discord.ext import commands, tasks
from discord import User
import os.path
import random
import json

class Love(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.huggies = []
        self.kisses = []
        
        self.load()
        self.save_task.start()

    def load(self):
        if os.path.exists("jsons/huggies.json"):
            with open("jsons/huggies.json", "r") as f:
                self.huggies = json.load(f)
        
            return

        if os.path.exists("jsons/huggies.json"):
            with open("jsons/kisses.json", "r") as f:
                self.kisses = json.load(f)
            
            return

        self.save()
    
    def save(self):
        with open("jsons/huggies.json", "w") as f:
            json.dump(self.huggies, f)
        
        with open("jsons/kisses.json", "w") as f:
            json.dump(self.kisses, f)
    
    @commands.command()
    async def savehugkiss(self, ctx):
        self.save()
        await ctx.send("Done! :D")
    
    @tasks.loop(hours=1)
    async def save_task(self):
        self.save()
    
    @commands.command()
    async def addhug(self, ctx, url):
        self.huggies.append(url)
        await ctx.send(f"Added {url} to the list!")
        
    @commands.command()
    async def addkiss(self, ctx, url):
        self.kisses.append(url)
        await ctx.send(f"Added {url} to the list!")
    
    @commands.command()
    async def hug(self, ctx, someone: User):
        someone = someone or ctx.author
        
        if someone == ctx.author:
            return await ctx.send(f"Ahh, you need a hug? Come here!! <3 \n{random.choice(self.huggies)}")
            
        await ctx.send(f"Hii {someone.name}! {ctx.author.name} just wanted to hug you!!! \n{random.choice(self.huggies)}")

    @commands.command()
    async def kiss(self, ctx, someone: User):
        someone = someone or ctx.author
        
        if someone == ctx.author:
            return await ctx.send(f"Come to me and show me your forehead, and I will kiss you right in the center!!! \n{random.choice(self.kisses)}")
            
        await ctx.send(f"Hii {someone.name}! {ctx.author.name} just wanted to kiss you!! :D \n{random.choice(self.kisses)}")
        
def setup(bot):
    bot.add_cog(Love(bot))