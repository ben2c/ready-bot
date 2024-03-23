import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import settings


class Ready (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'ready', description = 'Ready up for a queue', guild_ids=[testServerId])
  async def ready(self, interaction: Interaction, queue_id: int):
    settings.playerArr[queue_id].append('<@' + f'{interaction.user.id}' + '>')
    await interaction.response.send_message("Readied up for Queue: " + f'{queue_id}')

  @nextcord.slash_command(name = 'unready', description = 'Unready up for a queue', guild_ids=[testServerId])
  async def unready(self, interaction: Interaction):
    await interaction.response.send_message("Queue 1: " + settings.gameNameArr[1])

def setup(client):
  client.add_cog(Ready(client))