import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class Test (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'testing', description = 'test command', guild_ids=[testServerId])
  async def test(self, interaction: Interaction, message_id: str):
    await interaction.response.send_message("Mesasge: " + message_id)

def setup(client):
  client.add_cog(Test(client))