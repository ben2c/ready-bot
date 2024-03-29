import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import settings

class Ready (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'r', description = 'Ready up for a queue', guild_ids=[testServerId])
  async def ready(self, interaction: Interaction, queue: str = SlashOption(name = "queue", description = "Choose a queue")):

    gameNameArrLower = [game.lower() for game in settings.gameNameArr]

    queue_id = gameNameArrLower.index(queue.lower())

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    #Checks if entered queue is in range
    # if queue_id >= len(settings.gameNameArr) or queue_id < 0:
    #   await interaction.response.send_message("Please enter a valid queue ")

    #Checks if player is already in queue
    if player_id in settings.playerArr[queue_id]:
      await interaction.response.send_message("You're already queued for " + settings.gameNameArr[queue_id], ephemeral=True)
    
    #Checks if Queue is full
    elif len(settings.playerArr[queue_id]) == settings.queueSize[queue_id]:
      await interaction.response.send_message("This queue is full", ephemeral=True)

    elif queue_id < len(settings.playerArr):

      #Adds player to queue
      settings.playerArr[queue_id].append(player_id)
      settings.playerArrString[queue_id].append(player_username)

      #Updates channel topic
      # channel = nextcord.utils.get(self.client.get_all_channels(), name="our-glorious-robot-overlords")
      # await channel.edit(topic = 'Hello!')

      #Checks if queue is full after player is added
      if len(settings.playerArr[queue_id]) == settings.queueSize[queue_id]:
        await interaction.response.send_message("Get your asses online to play: "+ settings.gameNameArr[queue_id] + " | " + str(', '.join(settings.playerArr[queue_id])))
      
      else:
        await interaction.response.send_message(settings.gameNameArr[queue_id] + ": " + str(', '.join(settings.playerArrString[queue_id]))  + " | Missing " + str(settings.queueSize[queue_id] - len(settings.playerArr[queue_id])) + " more!")
    
    else:
      await interaction.response.send_message("Final catch, idk what the fuck you entered, allow me to fix it")

  #Autocomplete game selection
  @ready.on_autocomplete("queue")
  async def readyQueue(self, interaction: Interaction, queue: str):
    if not queue:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(settings.gameNameArr)
        return
    # send a list of nearest matches from the list of queue
    get_near_queue = [queue_name for queue_name in settings.gameNameArr if queue_name.lower().startswith(queue.lower())]
    await interaction.response.send_autocomplete(get_near_queue)

def setup(client):
  client.add_cog(Ready(client))