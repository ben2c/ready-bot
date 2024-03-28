import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import settings
import asyncio

class TimeReadyAll (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'trall', description = 'Ready up for all queues but expires after certain amount of time', guild_ids=[testServerId])
  async def timereadyall(self, interaction: Interaction, time: int = SlashOption(name="time", description="Amount in minutes to stay in queue")):

    time_sec = time * 60
    time_hour = time / 60

    #Shortens display time
    if time < 60:
      display_time = str(time) + "m"
    else:
      display_time = str(round(time_hour, 1)) + "h"

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    await interaction.response.send_message("Added to all queues for " +  display_time)

    for queue in settings.gameNameArr:

      queue_id = settings.gameNameArr.index(queue)

      #Checks if player is already in queue
      if player_id in settings.playerArr[queue_id]:
       break
      
      elif queue_id <= len(settings.playerArr):

        #Adds player to queue
        settings.playerArr[queue_id].append(player_id)
        settings.playerArrString[queue_id].append(player_username)
        
        #Checks if queue is full after player is added
        if len(settings.playerArr[queue_id]) == settings.queueSize[queue_id]:
          await interaction.followup.send("Get your asses online to play: "+ settings.gameNameArr[queue_id] +" | " + str(', '.join(settings.playerArr[queue_id])))


    #removes player from queue after set time
    await asyncio.sleep(time_sec)
    for queue in settings.playerArr:

      queue_id = settings.playerArr.index(queue)

      if player_id in settings.playerArr[queue_id]:
        settings.playerArr[queue_id].remove(player_id)
        settings.playerArrString[queue_id].remove(player_username)


def setup(client):
  client.add_cog(TimeReadyAll(client))