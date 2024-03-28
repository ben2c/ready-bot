import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import settings

class ReadyAll (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'rall', description = 'Ready up for all queue', guild_ids=[testServerId])
  async def readyall(self, interaction: Interaction):

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    await interaction.response.send_message("Added to all queues")

    for queue in settings.playerArr:

      queue_id = settings.playerArr.index(queue)

      #Checks if player is already in queue
      if player_id in settings.playerArr[queue_id]:
       break
      
      elif queue_id <= len(settings.playerArr):

        #Adds player to queue
        settings.playerArr[queue_id].append(player_id)
        settings.playerArrString[queue_id].append(player_username)
        
                #Checks if queue is full after player is added
        if len(settings.playerArr[queue_id]) == settings.queueSize[queue_id]:
          await interaction.followup.send("Get your asses online to play: "+ settings.gameNameArr[queue_id] +" | " + str(*settings.playerArr[queue_id]))


def setup(client):
  client.add_cog(ReadyAll(client))