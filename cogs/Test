import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import arrays
import asyncio


class Test (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'meme', description = 'Reon Fucking Ni', guild_ids=[testServerId])
  async def ryan(self, interaction: Interaction):
    await interaction.response.send_message("REEEONNNNN FUCCKING NIII")
    embed = nextcord.Embed(title="")
    embed.set_image(url="https://media1.tenor.com/m/SadoB6GZQe4AAAAd/reon.gif")
    await interaction.channel.send(embed=embed)

  # @nextcord.slash_command(name = 'test2', description = 'delayed response', guild_ids=[testServerId])
  # async def test2(self, interaction: Interaction):
  #   await asyncio.sleep(10)
  #   await interaction.followup.send("After 10 seconds ")

def setup(client):
  client.add_cog(Test(client))