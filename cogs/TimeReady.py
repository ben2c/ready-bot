import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import settings
import asyncio

class TimeReady (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'tr', description = 'Ready up but expires after certain amount of time', guild_ids=[testServerId])
  async def timeready(self, interaction: Interaction, queue: str = SlashOption(name = "queue", description = "Choose a queue"), time: int = SlashOption(name="time", description="Amount in minutes to stay in queue")):

    gameNameArrLower = [game.lower() for game in settings.gameNameArr]
    queue_id = gameNameArrLower.index(queue.lower())

    time_sec = time * 60
    time_hour = time / 60

    #Shortens display time
    if time < 60:
      display_time = str(time) + "m"
    else:
      display_time = str(round(time_hour, 1)) + "h"

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    if time < 0:
      await interaction.response.send_message("Please enter a positive number", ephemeral=True)
    
    else:
      #Checks if player is already in queue
      if player_id in settings.playerArr[queue_id]:
        await interaction.response.send_message("You're already queued for " + settings.gameNameArr[queue_id])
      
      #Checks if Queue is full
      elif len(settings.playerArr[queue_id]) == settings.queueSize[queue_id]:
        await interaction.response.send_message("This queue is full")

      elif queue_id < len(settings.playerArr):

        #Adds player to queue
        settings.playerArr[queue_id].append(player_id)
        settings.playerArrString[queue_id].append(player_username)

        #Checks if queue is full after player is added
        if len(settings.playerArr[queue_id]) == settings.queueSize[queue_id]:
          await interaction.response.send_message("Get your asses online to play: "+ settings.gameNameArr[queue_id] + str(*settings.playerArr[queue_id]))
        
        else:
          await interaction.response.send_message(settings.gameNameArr[queue_id] + ": " + str(', '.join(settings.playerArrString[queue_id]))  + " | Missing " + str(settings.queueSize[queue_id] - len(settings.playerArr[queue_id])) + " more | Queued for " +  display_time)
      
      else:
        await interaction.response.send_message("Final catch, idk what the fuck you entered, allow me to fix it")

      #removes player from queue after set time
      await asyncio.sleep(time_sec)
      settings.playerArr[queue_id].remove(player_id)
      settings.playerArrString[queue_id].remove(player_username)

  #Autocomplete game selection
  @timeready.on_autocomplete("queue")
  async def readyQueue(self, interaction: Interaction, queue: str):
    if not queue:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(settings.gameNameArr)
        return
    # send a list of nearest matches from the list of queue
    get_near_queue = [queue_name for queue_name in settings.gameNameArr if queue_name.lower().startswith(queue.lower())]
    await interaction.response.send_autocomplete(get_near_queue)

def setup(client):
  client.add_cog(TimeReady(client))