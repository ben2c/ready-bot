import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import settings

class NewQueue (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'new', description = 'Create a new queue', guild_ids=[testServerId])
  async def new(self, interaction: Interaction, queue_name: str, queue_size: int):

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    if queue_name in settings.gameNameArr:
      await interaction.response.send_message("This game already exist")

    else:
      #Adds player to new queue
      settings.playerArr.append([player_id])
      settings.playerArrString.append([player_username])
      settings.gameNameArr.append(queue_name)
      settings.queueSize.append(queue_size)
    
    await interaction.response.send_message("New queue for " + queue_name + " has been created and you have been added to the queue")

    if len(settings.playerArr[len(settings.playerArr) - 1]) == settings.queueSize[len(settings.playerArr) - 1]:
      await interaction.followup.send("Get your own ass online to play: "+ queue_name + "...you loner ... sad")
    

def setup(client):
  client.add_cog(NewQueue(client))