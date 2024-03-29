import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import settings
import os
from dotenv import load_dotenv

#Loads Token & Intents
load_dotenv()
intents = nextcord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = '!', intents=intents)

#Server for testing purposes, need to remove once in prod, but takes some time for commands to load
testServerId = 389588257106690051

#Initializes arrays
settings.init()

#Bot Startup
@client.event
async def on_ready():
    print('The bot is online')
    print('------')


#Cogs
initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)


#Bot Start Up Token
client.run(os.getenv('TOKEN')) #Need .env file with bot token