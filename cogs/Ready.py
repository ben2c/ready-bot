import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import settings


class Ready (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'ready', description = 'Ready up for a queue', guild_ids=[testServerId])
  async def ready(self, interaction: Interaction, queue: int):

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    if player_id in settings.playerArr[queue]:
      await interaction.response.send_message("You're already in Queue: " + settings.gameNameArr[queue])
    
    elif len(settings.playerArr[queue]) == settings.queueSize[queue]:
      await interaction.response.send_message("This queue is full")

    elif queue < len(settings.playerArr):
      settings.playerArr[queue].append(player_id)
      settings.playerArrString[queue].append(player_username)

      if len(settings.playerArr[queue]) == settings.queueSize[queue]:
        await interaction.response.send_message("Get your asses online to play: "+ settings.gameNameArr[queue] + str(*settings.playerArr[queue]))
      
      else:
        await interaction.response.send_message("Queue for " + settings.gameNameArr[queue] + ": " + str(*settings.playerArrString[queue])  + " | Missing " + str(settings.queueSize[queue] - len(settings.playerArr[queue])) + " more!")
    
    else:
      await interaction.response.send_message("Final catch, idk what the fuck you entered, allow me to fix it")

  @nextcord.slash_command(name = 'unready', description = 'Unready up for a queue', guild_ids=[testServerId])
  async def unready(self, interaction: Interaction):
    await interaction.response.send_message("Queue 1: " + settings.gameNameArr[1])

def setup(client):
  client.add_cog(Ready(client))