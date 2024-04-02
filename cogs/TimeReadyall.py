import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays
import asyncio

class TimeReadyAll (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'trall', description = 'Ready up for all queues but expires after certain amount of time', guild_ids=[testServerId])
  async def timereadyall(self, interaction: Interaction, time: int = SlashOption(name="time", description="Amount in minutes to stay in queue")):

    channel = self.client.get_channel(716158981470421052)
    clear_queue = False
    time_sec = time * 60

    #Shortens display time
    if time < 60:
      display_time = str(time) + "m"
    else:
      display_time = str(time // 60) + "h " + str(time % 60) + "m"

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    if time < 0:
      await interaction.response.send_message("Please enter a positive number", ephemeral=True)

    else:
      await interaction.response.send_message("Added to all queues for " +  display_time)
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


    #removes player from queue after set time
    await asyncio.sleep(time_sec)
    for queue in arrays.playerArr:

      queue_id = arrays.playerArr.index(queue)

      if player_id in arrays.playerArr[queue_id]:
        arrays.playerArr[queue_id].remove(player_id)
        arrays.playerArrString[queue_id].remove(player_username)
    await channel.send(player_username + " timed out from all queues")


def setup(client):
  client.add_cog(TimeReadyAll(client))