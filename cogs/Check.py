import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import arrays


class Check (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'check', description = 'Check Queues', guild_ids=[testServerId])
  async def check(self, interaction: Interaction):

    allqueues = ""

    for queue_id in range(len(arrays.playerArrString)):

      allqueues += arrays.gameNameArr[queue_id] + ": " + str(', '.join(arrays.playerArrString[queue_id])) + " | " + str(len(arrays.playerArr[queue_id])) + "/" + str(arrays.queueSize[queue_id]) + "\n"

    await interaction.response.send_message(allqueues)

def setup(client):
  client.add_cog(Check(client))