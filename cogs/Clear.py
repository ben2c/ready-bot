import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import settings

class Clear (commands.Cog):
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'clear', description = 'Clears all queues', guild_ids=[testServerId])
  async def clear(self, interaction: Interaction):

    await interaction.response.send_message("All queues cleared")
  
    for queue in settings.playerArr:

      queue_id = settings.playerArr.index(queue)

      settings.playerArr[queue_id].clear()
      settings.playerArrString[queue_id].clear()



def setup(client):
  client.add_cog(Clear(client))