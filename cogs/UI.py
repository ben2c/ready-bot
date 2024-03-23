import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class Subscription(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout= 1000)
    self.value = None

  @nextcord.ui.button(label = "Ready up for this queue", style=nextcord.ButtonStyle.green)
  async def ready(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.send_message('You are now in this queue', ephemeral=True)
    self.value = True
    self.stop()

  @nextcord.ui.button(label = "Unready", style=nextcord.ButtonStyle.red)
  async def unready(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.send_message('You are taken off of this queue', ephemeral=True)
    self.value = False
    self.stop()

class UI(commands.Cog):

  def __init__(self,client):
    self.client = client

  testServerId = 758151181494255646

  @nextcord.slash_command(name = "button", description = "Ready up for Queue", guild_ids=[testServerId])
  async def readyQueue(self, interaction: Interaction):
    view = Subscription()
    await interaction.response.send_message("You can ready or unready up", view = view)
    await view.wait()

    if view.value is None:
      return
    elif view.value:
      print("ready up")
    else:
      print("Huh?")


def setup(client):
  client.add_cog(UI(client))