import nextcord
from nextcord import Interaction
from nextcord.ext import commands

class Meme(commands.Cog):
  
  def __init__(self,client):
    self.client = client

  #Event
  @commands.Cog.listener()
  async def on_message(self, message):
    
    if message.author == self.client.user:
      return
    
    if("meme" or "Meme") in message.content:
      embed = nextcord.Embed(title="")
      embed.set_image(url="https://tenor.com/fbJBtpz7zbV.gif")
      await message.channel.send(embed=embed)

    elif ("chicken") in message.content:
      await message.channel.send("Did someone say meme?")
      embed = nextcord.Embed(title="")
      embed.set_image(url="https://media1.tenor.com/m/Kcd9s-ao_VkAAAAC/kekw.gif")
      await message.channel.send(embed=embed)

def setup(client):
  client.add_cog(Meme(client))