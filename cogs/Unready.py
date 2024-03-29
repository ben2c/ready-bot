import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import settings

class Unready (commands.Cog):
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'nr', description = 'Unready for a queue', guild_ids=[testServerId])
  async def unready(self, interaction: Interaction, queue: str = SlashOption(name = "queue", description = "Choose a queue")):

    gameNameArrLower = [game.lower() for game in settings.gameNameArr]

    queue_id = gameNameArrLower.index(queue.lower())

    player_id = '<@' + f'{interaction.user.id}' + '>'
    player_username = interaction.user.global_name

    if player_id in settings.playerArr[queue_id]:
      settings.playerArr[queue_id].remove(player_id)
      settings.playerArrString[queue_id].remove(player_username)
      await interaction.response.send_message("You have been removed from " + settings.gameNameArr[queue_id], ephemeral=True)

    #sus
    elif player_id not in settings.playerArr:
      await interaction.response.send_message("You're not in this queue", ephemeral=True)

    else:
      await interaction.response.send_message("Final catch, idk what the fuck you entered, allow me to fix it")

  #Autocomplete game selection
  @unready.on_autocomplete("queue")
  async def readyQueue(self, interaction: Interaction, queue: str):
    if not queue:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(settings.gameNameArr)
        return
    # send a list of nearest matches from the list of queue
    get_near_queue = [queue_name for queue_name in settings.gameNameArr if queue_name.lower().startswith(queue.lower())]
    await interaction.response.send_autocomplete(get_near_queue)

def setup(client):
  client.add_cog(Unready(client))