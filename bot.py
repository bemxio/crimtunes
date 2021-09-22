from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot = commands.Bot(
    command_prefix="ct ",
    help_command=None,
    case_insensitive=True
)

@bot.event
async def on_ready():
    print("crimtunes is ready! :D")
    #print(list(map(lambda c: c.name, bot.commands)))

"""
@bot.event
async def on_message(msg):
    print(msg.content)
"""   
 
# adding cogs
bot.load_extension("cogs.music") 
bot.load_extension("cogs.love") 
  
bot.run(os.getenv("TOKEN"))