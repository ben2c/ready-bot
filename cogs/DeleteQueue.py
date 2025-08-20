import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays

class DeleteQueue(commands.Cog):
    def __init__(self, client):
        self.client = client

    testServerId = 389588257106690051

    @nextcord.slash_command(
        name='delete',
        description='Delete a queue and remove all players and timers',
        guild_ids=[testServerId]
    )
    async def deletequeue(self, interaction: Interaction, queue: str = SlashOption(name="queue", description="Queue name to delete")):
        gameNameArrLower = [game.lower() for game in arrays.gameNameArr]
        try:
            queue_id = gameNameArrLower.index(queue.lower())
        except ValueError:
            await interaction.response.send_message("Queue not found.", ephemeral=True)
            return

        # Get all player IDs in the queue
        players_to_remove = arrays.playerArr[queue_id].copy()
        player_usernames = arrays.playerArrString[queue_id].copy()

        # Remove queue and associated arrays
        arrays.playerArr.pop(queue_id)
        arrays.playerArrString.pop(queue_id)
        arrays.gameNameArr.pop(queue_id)
        arrays.queueSize.pop(queue_id)

        # Cancel timers for all players in all relevant cogs
        cog_names = ["Ready", "ReadyAll", "TimeReady", "TimeReadyAll"]
        for player_id in players_to_remove:
            for cog_name in cog_names:
                cog = self.client.get_cog(cog_name)
                if cog and hasattr(cog, "player_timers"):
                    timer = cog.player_timers.get(player_id)
                    if timer:
                        timer.cancel()
                        cog.player_timers.pop(player_id, None)

        await interaction.response.send_message(
            f"Queue '{queue}' and all its players have been deleted."
        )

    # Autocomplete for queue names
    @deletequeue.on_autocomplete("queue")
    async def autocomplete_queue(self, interaction: Interaction, queue: str):
        if not queue:
            await interaction.response.send_autocomplete(arrays.gameNameArr)
            return
        matches = [name for name in arrays.gameNameArr if name.lower().startswith(queue.lower())]
        await interaction.response.send_autocomplete(matches)

def setup(client):
    client.add_cog(DeleteQueue(client))