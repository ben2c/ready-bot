import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays

class UnreadyAll (commands.Cog):
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'nrall', description = 'Unready for all queues', guild_ids=[testServerId])
  async def unreadyall(self, interaction: Interaction):

    await interaction.response.send_message("You have been removed from all queues")

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name
    
    for queue in arrays.playerArr:

      queue_id = arrays.playerArr.index(queue)

      if player_id in arrays.playerArr[queue_id]:
        arrays.playerArr[queue_id].remove(player_id)
        arrays.playerArrString[queue_id].remove(player_username)



def setup(client):
  client.add_cog(UnreadyAll(client))