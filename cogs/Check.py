import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import settings


class Check (commands.Cog):
  
  def __init__(self, client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = 'check', description = 'Check Queues', guild_ids=[testServerId])
  async def check(self, interaction: Interaction):

    allqueues = ""

    for queue_id in range(len(settings.playerArrString)):

      allqueues += settings.gameNameArr[queue_id] + ": " + str(*settings.playerArrString[queue_id]) + " | " + str(len(settings.playerArr[queue_id])) + "/" + str(settings.queueSize[queue_id]) + "\n"

    await interaction.response.send_message(allqueues)

def setup(client):
  client.add_cog(Check(client))