import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import settings


class Test (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'testing', description = 'test command', guild_ids=[testServerId])
  async def test(self, interaction: Interaction, message_id: str):
    await interaction.response.send_message("Mesasge: " + message_id)

  @nextcord.slash_command(name = 'test2', description = 'check queue', guild_ids=[testServerId])
  async def test2(self, interaction: Interaction):
    await interaction.response.send_message("Queue 1: " + settings.gameNameArr[1])

def setup(client):
  client.add_cog(Test(client))