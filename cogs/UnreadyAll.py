import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import settings

class UnreadyAll (commands.Cog):
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'unreadyall', description = 'Unready for all queues', guild_ids=[testServerId])
  async def unreadyall(self, interaction: Interaction):

    await interaction.response.send_message("You have been removed from all queues")

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name
    
    for queue in settings.playerArr:

      queue_id = settings.playerArr.index(queue)

      if player_id in settings.playerArr[queue_id]:
        settings.playerArr[queue_id].remove(player_id)
        settings.playerArrString[queue_id].remove(player_username)



def setup(client):
  client.add_cog(UnreadyAll(client))