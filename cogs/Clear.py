import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays
import asyncio

class Clear (commands.Cog):
  def __init__(self, client):
    self.client = client

  testServerId = 389588257106690051

  @nextcord.slash_command(name = 'clear', description = 'Clears all queues', guild_ids=[testServerId])
  async def clear(self, interaction: Interaction):

    await interaction.response.send_message("All queues cleared")
  
    for queue in arrays.playerArr:

      queue_id = arrays.playerArr.index(queue)

      arrays.playerArr[queue_id].clear()
      arrays.playerArrString[queue_id].clear()

    # async def cancel_me():
    #   print('cancel_me(): before sleep')

    #   try:
    #       # Wait for 1 hour
    #       await asyncio.sleep(3600)
    #   except asyncio.CancelledError:
    #       print('cancel_me(): cancel sleep')
    #       raise
    #   finally:
    #       print('cancel_me(): after sleep')

    # async def main():
    #     # Create a "cancel_me" Task
    #     task = asyncio.create_task(cancel_me())

    #     # Wait for 1 second
    #     await asyncio.sleep(1)

    #     task.cancel()
    #     try:
    #         await task
    #     except asyncio.CancelledError:
    #         print("main(): cancel_me is cancelled now")

    # asyncio.run(main())



def setup(client):
  client.add_cog(Clear(client))