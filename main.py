import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = nextcord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)
testServerId = 758151181494255646

#Arrays
playerArr = [[], []]
gameNameArr = ["League", "Valorant"]
playerArrString = [[], []]
queueSize = [[5], [5]]

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

@client.slash_command(name= "hello", description= "Hello World", guild_ids=[testServerId])
async def hello(interaction: Interaction):
    await interaction.response.send_message("Hello!")

#Commands
# @bot.hybrid_command()
# async def sync(ctx: commands.Context):
#     """Sync Commands"""
#     await ctx.send('Syncing...')
#     await bot.tree.sync()

# @bot.hybrid_command()
# async def display(ctx: commands.Context):
#     """Displays Array"""
#     await ctx.send(gameNameArr[0])

# @bot.hybrid_command()
# async def check(ctx: commands.Context, message_id: int):
#     """Check Specific Queue"""
#     await ctx.send('Your Message' + message_id)
#     await ctx.send(CheckQueue(message_id))

#testServerId only needed for testing for commands to show up instantly
# @bot.hybrid_command(guild_ids=[testServerId])
# async def test(ctx: commands.Context, message_id: str):
#     """Test Command"""
#     await ctx.send(Test(message_id))


#Bot Start Up Token
client.run(os.getenv('TOKEN')) #Need .env file with bot token