import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.hybrid_command()
async def ping(ctx: commands.Context):
    await ctx.send('pong')

@bot.hybrid_command()
async def sync(ctx: commands.Context):
    await ctx.send('Syncing...')
    await bot.tree.sync(guild= ctx.guild)

bot.run(os.getenv('TOKEN'))