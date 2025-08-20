import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays

class Unready(commands.Cog):
    def __init__(self, client):
        self.client = client

    testServerId = 389588257106690051

    @nextcord.slash_command(
        name='nr',
        description='Unready for a queue',
        guild_ids=[testServerId]
    )
    async def unready(self, interaction: Interaction, queue: str = SlashOption(name="queue", description="Choose a queue")):
        gameNameArrLower = [game.lower() for game in arrays.gameNameArr]

        try:
            queue_id = gameNameArrLower.index(queue.lower())
        except ValueError:
            await interaction.response.send_message("Queue not found.", ephemeral=True)
            return

        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

        if player_id in arrays.playerArr[queue_id]:
            arrays.playerArr[queue_id].remove(player_id)
            arrays.playerArrString[queue_id].remove(player_username)
            await interaction.response.send_message("You have been removed from " + arrays.gameNameArr[queue_id])

            # Cancel the user's timer in Ready cog if it exists
            ready_cog = self.client.get_cog("Ready")
            if ready_cog:
                timer = ready_cog.player_timers.get(player_id)
                if timer:
                    timer.cancel()
                    ready_cog.player_timers.pop(player_id, None)

            # Cancel the user's timer in ReadyAll cog if it exists
            readyall_cog = self.client.get_cog("ReadyAll")
            if readyall_cog:
                timer = readyall_cog.player_timers.get(player_id)
                if timer:
                    timer.cancel()
                    readyall_cog.player_timers.pop(player_id, None)

            # Cancel the user's timer in TimeReady cog if it exists
            timeready_cog = self.client.get_cog("TimeReady")
            if timeready_cog:
                timer = timeready_cog.player_timers.get(player_id)
                if timer:
                    timer.cancel()
                    timeready_cog.player_timers.pop(player_id, None)

            # Cancel the user's timer in TimeReadyAll cog if it exists
            timereadyall_cog = self.client.get_cog("TimeReadyAll")
            if timereadyall_cog:
                timer = timereadyall_cog.player_timers.get(player_id)
                if timer:
                    timer.cancel()
                    timereadyall_cog.player_timers.pop(player_id, None)

        elif player_id not in arrays.playerArr[queue_id]:
            await interaction.response.send_message("You're not in this queue", ephemeral=True)
        else:
            await interaction.response.send_message("Final catch, idk what you entered. Please try again.", ephemeral=True)

    # Autocomplete game selection
    @unready.on_autocomplete("queue")
    async def readyQueue(self, interaction: Interaction, queue: str):
        if not queue:
            await interaction.response.send_autocomplete(arrays.gameNameArr)
            return
        get_near_queue = [queue_name for queue_name in arrays.gameNameArr if queue_name.lower().startswith(queue.lower())]
        await interaction.response.send_autocomplete(get_near_queue)

def setup(client):
    client.add_cog(Unready(client))