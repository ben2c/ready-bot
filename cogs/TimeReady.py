import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays
import asyncio

class TimeReady(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.player_timers = {}  # Track player_id -> asyncio.Task

    testServerId = 389588257106690051

    @nextcord.slash_command(
        name='tr',
        description='Ready up but expires after certain amount of time',
        guild_ids=[testServerId]
    )
    async def timeready(self, interaction: Interaction, queue: str = SlashOption(name="queue", description="Choose a queue"), time: int = SlashOption(name="time", description="Amount in minutes to stay in queue")):

        gameNameArrLower = [game.lower() for game in arrays.gameNameArr]
        try:
            queue_id = gameNameArrLower.index(queue.lower())
        except ValueError:
            await interaction.response.send_message("Queue not found.", ephemeral=True)
            return

        channel = interaction.channel
        clear_queue = False
        time_sec = time * 60

        # Shortens display time
        if time < 60:
            display_time = str(time) + "m"
        else:
            display_time = str(time // 60) + "h " + str(time % 60) + "m"

        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

        if time < 0:
            await interaction.response.send_message("Please enter a positive number", ephemeral=True)
            return

        # Checks if player is already in queue
        if player_id in arrays.playerArr[queue_id]:
            await interaction.response.send_message("You're already queued for " + arrays.gameNameArr[queue_id], ephemeral=True)
            return

        # Checks if Queue is full
        if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
            await interaction.response.send_message("This queue is full", ephemeral=True)
            return

        if queue_id < len(arrays.playerArr):
            # Adds player to queue
            arrays.playerArr[queue_id].append(player_id)
            arrays.playerArrString[queue_id].append(player_username)

            # Checks if queue is full after player is added
            if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                await interaction.response.send_message("Get your asses online to play: "+ arrays.gameNameArr[queue_id] + " | " + str(', '.join(arrays.playerArr[queue_id])))
                clear_queue = True
                clear_queue_id = queue_id
            else:
                await interaction.response.send_message(arrays.gameNameArr[queue_id] + ": " + str(', '.join(arrays.playerArrString[queue_id]))  + " | Missing " + str(arrays.queueSize[queue_id] - len(arrays.playerArr[queue_id])) + " more | Queued for " +  display_time)
        else:
            await interaction.response.send_message("Final catch, idk what you entered.", ephemeral=True)
            return

        if clear_queue:
            await asyncio.sleep(200)  # Wait 3 minutes before checking if the queue is still full
            if len(arrays.playerArr[clear_queue_id]) == arrays.queueSize[clear_queue_id]:
                tempPlayerArray = arrays.playerArr[clear_queue_id]
                for player in reversed(tempPlayerArray):
                    for index_game in range(len(arrays.gameNameArr)):
                        if player in arrays.playerArr[index_game]:
                            index_player = arrays.playerArr[index_game].index(player)
                            arrays.playerArr[index_game].remove(player)
                            arrays.playerArrString[index_game].pop(index_player)
                await interaction.followup.send("Players in full queue were removed from all queues")

        # Cancel any existing timer for this player
        if player_id in self.player_timers:
            self.player_timers[player_id].cancel()

        # Start timeout task for this player
        self.player_timers[player_id] = asyncio.create_task(self._timeout_player(player_id, player_username, queue_id, time_sec, channel))

    async def _timeout_player(self, player_id, player_username, queue_id, time_sec, channel):
        try:
            await asyncio.sleep(time_sec)
            if player_id in arrays.playerArr[queue_id]:
                arrays.playerArr[queue_id].remove(player_id)
                arrays.playerArrString[queue_id].remove(player_username)
                await channel.send(player_username + " timed out from " + arrays.gameNameArr[queue_id])
        except asyncio.CancelledError:
            # Timer was cancelled (user unreadied)
            pass
        finally:
            self.player_timers.pop(player_id, None)

    # Autocomplete game selection
    @timeready.on_autocomplete("queue")
    async def readyQueue(self, interaction: Interaction, queue: str):
        if not queue:
            await interaction.response.send_autocomplete(arrays.gameNameArr)
            return
        get_near_queue = [queue_name for queue_name in arrays.gameNameArr if queue_name.lower().startswith(queue.lower())]
        await interaction.response.send_autocomplete(get_near_queue)

def setup(client):
    client.add_cog(TimeReady(client))