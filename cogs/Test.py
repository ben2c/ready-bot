import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import settings


class Test (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'ryan', description = 'Reon Fucking Ni', guild_ids=[testServerId])
  async def ryan(self, interaction: Interaction):
    await interaction.response.send_message("REEEONNNNN")
    embed = nextcord.Embed(title="Master Ni")
    embed.set_image(url="https://media1.tenor.com/m/SadoB6GZQe4AAAAd/reon.gif")
    await interaction.channel.send(embed=embed)

  # @nextcord.slash_command(name = 'test2', description = 'check queue', guild_ids=[testServerId])
  # async def test2(self, interaction: Interaction):
  #   await interaction.response.send_message("Queue 1: " + settings.gameNameArr[1])

def setup(client):
  client.add_cog(Test(client))