import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays

class NewQueue (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'new', description = 'Create a new queue', guild_ids=[testServerId])
  async def new(self, interaction: Interaction, queue_name: str, queue_size: int):

    if queue_size > 0:
      player_id = '<@' + f'{interaction.user.id}' + '>'
      player_username = interaction.user.global_name

      if queue_name in arrays.gameNameArr:
        await interaction.response.send_message("This game already exist")

      else:
        # Create empty queue, do not add player
        arrays.playerArr.append([])
        arrays.playerArrString.append([])
        arrays.gameNameArr.append(queue_name)
        arrays.queueSize.append(queue_size)
      
      await interaction.response.send_message("New queue has been created for " + queue_name + " with a size of " + str(queue_size))

      if len(arrays.playerArr[len(arrays.playerArr) - 1]) == arrays.queueSize[len(arrays.playerArr) - 1]:
        await interaction.followup.send("Get your own ass online to play: "+ queue_name + "...you loner ... sad")
    else:
      await interaction.response.send_message("Please enter a number that is greater than 1", ephemeral=True)
    

def setup(client):
  client.add_cog(NewQueue(client))