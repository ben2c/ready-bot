import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays

class ReadyAll (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'rall', description = 'Ready up for all queue', guild_ids=[testServerId])
  async def readyall(self, interaction: Interaction):

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    await interaction.response.send_message("Added to all queues")

    for queue in arrays.gameNameArr:

      queue_id = arrays.gameNameArr.index(queue)

      #Checks if player is already in queue
      if player_id in arrays.playerArr[queue_id]:
       break
      
      elif queue_id <= len(arrays.playerArr):

        #Adds player to queue
        arrays.playerArr[queue_id].append(player_id)
        arrays.playerArrString[queue_id].append(player_username)
        
        #Checks if queue is full after player is added
        if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
          await interaction.followup.send("Get your asses online to play: "+ arrays.gameNameArr[queue_id] +" | " + str(', '.join(arrays.playerArr[queue_id])))


def setup(client):
  client.add_cog(ReadyAll(client))