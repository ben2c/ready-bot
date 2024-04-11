import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays
import asyncio

class Ready (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'r', description = 'Ready up for a queue for 1 hour', guild_ids=[testServerId])
  async def ready(self, interaction: Interaction, queue: str = SlashOption(name = "queue", description = "Choose a queue")):

    channel = self.client.get_channel(716158981470421052)
    gameNameArrLower = [game.lower() for game in arrays.gameNameArr]
    queue_id = gameNameArrLower.index(queue.lower())

    clear_queue = False

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    #Checks if player is already in queue
    if player_id in arrays.playerArr[queue_id]:
      await interaction.response.send_message("You're already queued for " + arrays.gameNameArr[queue_id], ephemeral=True)
    
    #Checks if Queue is full
    elif len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
      await interaction.response.send_message("This queue is full", ephemeral=True)

    elif queue_id < len(arrays.playerArr):

      #Adds player to queue
      arrays.playerArr[queue_id].append(player_id)
      arrays.playerArrString[queue_id].append(player_username)

      #Updates channel topic
      # channel = nextcord.utils.get(self.client.get_all_channels(), name="our-glorious-robot-overlords")
      # await channel.edit(topic = 'Hello!')

      #Checks if queue is full after player is added
      if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
        await interaction.response.send_message("Get your asses online to play: "+ arrays.gameNameArr[queue_id] + " | " + str(', '.join(arrays.playerArr[queue_id])))
        clear_queue = True
        clear_queue_id = queue_id
      
      else:
        await interaction.response.send_message(arrays.gameNameArr[queue_id] + ": " + str(', '.join(arrays.playerArrString[queue_id]))  + " | Missing " + str(arrays.queueSize[queue_id] - len(arrays.playerArr[queue_id])) + " more!")
    
    else:
      await interaction.response.send_message("Final catch, idk what the fuck you entered, allow me to fix it")
    
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
    await asyncio.sleep(3600)
    if player_id in arrays.playerArr[queue_id]:  
      arrays.playerArr[queue_id].remove(player_id)
      arrays.playerArrString[queue_id].remove(player_username)
      await channel.send(player_username + " timed out from " + arrays.gameNameArr[queue_id])

  #Autocomplete game selection
  @ready.on_autocomplete("queue")
  async def readyQueue(self, interaction: Interaction, queue: str):
    if not queue:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(arrays.gameNameArr)
        return
    # send a list of nearest matches from the list of queue
    get_near_queue = [queue_name for queue_name in arrays.gameNameArr if queue_name.lower().startswith(queue.lower())]
    await interaction.response.send_autocomplete(get_near_queue)

def setup(client):
  client.add_cog(Ready(client))