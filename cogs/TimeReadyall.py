import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays
import asyncio

class TimeReadyAll(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.player_timers = {}  # Track player_id -> asyncio.Task

    testServerId = 389588257106690051

    @nextcord.slash_command(
        name='trall',
        description='Ready up for all queues but expires after certain amount of time',
        guild_ids=[testServerId]
    )
    async def timereadyall(self, interaction: Interaction, time: int = SlashOption(name="time", description="Amount in minutes to stay in queue")):

        channel = interaction.channel
        clear_queue = False
        timeout_status = False
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

        await interaction.response.send_message("Added to all queues for " + display_time)
        for queue in arrays.gameNameArr:
            queue_id = arrays.gameNameArr.index(queue)
            # Checks if player is already in queue
            if player_id in arrays.playerArr[queue_id]:
                continue
            elif queue_id <= len(arrays.playerArr):
                # Adds player to queue
                arrays.playerArr[queue_id].append(player_id)
                arrays.playerArrString[queue_id].append(player_username)
                # Checks if queue is full after player is added
                if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                    await interaction.followup.send("Get your asses online to play: " + arrays.gameNameArr[queue_id] + " | " + str(', '.join(arrays.playerArr[queue_id])))
                    clear_queue = True
                    clear_queue_id = queue_id

        if clear_queue:
            await asyncio.sleep(30)
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
        self.player_timers[player_id] = asyncio.create_task(self._timeout_player(player_id, player_username, time_sec, channel))

    async def _timeout_player(self, player_id, player_username, time_sec, channel):
        try:
            await asyncio.sleep(time_sec)
            timeout_status = False
            for queue in arrays.playerArr:
                queue_id = arrays.playerArr.index(queue)
                if player_id in arrays.playerArr[queue_id]:
                    arrays.playerArr[queue_id].remove(player_id)
                    arrays.playerArrString[queue_id].remove(player_username)
                    timeout_status = True
            if timeout_status:
                await channel.send(player_username + " timed out from all queues")
        except asyncio.CancelledError:
            # Timer was cancelled (user unreadied)
            pass
        finally:
            self.player_timers.pop(player_id, None)

def setup(client):
    client.add_cog(TimeReadyAll(client))