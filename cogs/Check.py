import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import settings


class Check (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'check', description = 'Check Queue', guild_ids=[testServerId])
  async def check(self, interaction: Interaction, queue_id: int):
    await interaction.response.send_message("Queue : " + str(settings.playerArr[queue_id]))

def setup(client):
  client.add_cog(Check(client))