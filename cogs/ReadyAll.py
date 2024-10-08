import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays
import asyncio

class ReadyAll (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051
  TROLL_TIMEOUT_SECONDS = 60
  DEFAULT_TIMEOUT_SECONDS = 3600
  listOfTrolls = ["255976924428500993"]

  @nextcord.slash_command(name = 'rall', description = 'Ready up for all queue for 1 hour', guild_ids=[testServerId])
  async def readyall(self, interaction: Interaction):
    
    timeout_status=False
    channel = self.client.get_channel(716158981470421052)
    clear_queue = False
    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    await interaction.response.send_message("Added to all queues for 1h")

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
          clear_queue = True
          clear_queue_id = queue_id

    #Wait 5 minutes and clears the queue that queue is still full, also removes the players from the other queues that they're in
    if clear_queue == True:

      await asyncio.sleep(300)
      if len(arrays.playerArr[clear_queue_id]) == arrays.queueSize[clear_queue_id]:
          
        tempPlayerArray = arrays.playerArr[clear_queue_id]

        for player in reversed(tempPlayerArray):

          for index_game in range(len(arrays.gameNameArr)):

            if player in arrays.playerArr[index_game]:

              index_player = arrays.playerArr[index_game].index(player)

              arrays.playerArr[index_game].remove(player)
              arrays.playerArrString[index_game].pop(index_player)

        await interaction.followup.send("Players in full queue were removed from all queues")

    #removes player from queue after 1H
    if interaction.user.id in self.listOfTrolls:
      await asyncio.sleep(self.TROLL_TIMEOUT_SECONDS)
    else:
      await asyncio.sleep(self.DEFAULT_TIMEOUT_SECONDS)
    for queue in arrays.playerArr:

      queue_id = arrays.playerArr.index(queue)

      if player_id in arrays.playerArr[queue_id]:
        arrays.playerArr[queue_id].remove(player_id)
        arrays.playerArrString[queue_id].remove(player_username)
        timeout_status=True

    if timeout_status == True:
      await channel.send(player_username + " timed out from all queues")

def setup(client):
  client.add_cog(ReadyAll(client))