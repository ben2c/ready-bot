import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays
import asyncio

class Ready(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.player_timers = {}  # Track player_id -> asyncio.Task

    testServerId = 389588257106690051
    TROLL_TIMEOUT_SECONDS = 60
    DEFAULT_TIMEOUT_SECONDS = 3600
    listOfTrolls = ["255976924428500993"]

    @nextcord.slash_command(
        name='r',
        description='Ready up for a queue for 1 hour',
        guild_ids=[testServerId]
    )
    async def ready(self, interaction: Interaction, queue: str = SlashOption(name="queue", description="Choose a queue")):

        channel = interaction.channel
        gameNameArrLower = [game.lower() for game in arrays.gameNameArr]
        try:
            queue_id = gameNameArrLower.index(queue.lower())
        except ValueError:
            await interaction.response.send_message("Queue not found.", ephemeral=True)
            return

        clear_queue = False

        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

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

            # Button view for others to join this queue
            view = JoinQueueView(self, queue_id)

            # Checks if queue is full after player is added
            if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                await interaction.response.send_message(
                    "Get your asses online to play: "+ arrays.gameNameArr[queue_id] + " | " + str(', '.join(arrays.playerArr[queue_id])),
                    view=view
                )
                clear_queue = True
                clear_queue_id = queue_id
            else:
                await interaction.response.send_message(
                    arrays.gameNameArr[queue_id] + ": " + str(', '.join(arrays.playerArrString[queue_id]))  + " | Missing " + str(arrays.queueSize[queue_id] - len(arrays.playerArr[queue_id])) + " more!",
                    view=view
                )
        else:
            await interaction.response.send_message("Final catch, idk what you entered.", ephemeral=True)
            return

        # Wait 3 minutes before checking if the queue is still full
        if clear_queue:
            await asyncio.sleep(200)  
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
        timeout = self.TROLL_TIMEOUT_SECONDS if interaction.user.id in self.listOfTrolls else self.DEFAULT_TIMEOUT_SECONDS
        self.player_timers[player_id] = asyncio.create_task(self._timeout_player(player_id, player_username, queue_id, timeout, channel))

    async def _timeout_player(self, player_id, player_username, queue_id, timeout, channel):
        try:
            await asyncio.sleep(timeout)
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
    @ready.on_autocomplete("queue")
    async def readyQueue(self, interaction: Interaction, queue: str):
        if not queue:
            await interaction.response.send_autocomplete(arrays.gameNameArr)
            return
        get_near_queue = [queue_name for queue_name in arrays.gameNameArr if queue_name.lower().startswith(queue.lower())]
        await interaction.response.send_autocomplete(get_near_queue)

class JoinQueueView(nextcord.ui.View):
    def __init__(self, cog, queue_id):
        super().__init__(timeout=None)
        self.cog = cog
        self.queue_id = queue_id

    @nextcord.ui.button(label="Join This Queue", style=nextcord.ButtonStyle.primary)
    async def join_queue(self, button: nextcord.ui.Button, interaction: Interaction):
        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

        # Checks if player is already in queue
        if player_id in arrays.playerArr[self.queue_id]:
            await interaction.response.send_message("You're already queued for " + arrays.gameNameArr[self.queue_id], ephemeral=True)
            return

        # Checks if Queue is full
        if len(arrays.playerArr[self.queue_id]) == arrays.queueSize[self.queue_id]:
            await interaction.response.send_message("This queue is full", ephemeral=True)
            return

        arrays.playerArr[self.queue_id].append(player_id)
        arrays.playerArrString[self.queue_id].append(player_username)

        # Cancel any existing timer for this player
        if player_id in self.cog.player_timers:
            self.cog.player_timers[player_id].cancel()

        # Start timeout task for this player
        timeout = self.cog.TROLL_TIMEOUT_SECONDS if interaction.user.id in self.cog.listOfTrolls else self.cog.DEFAULT_TIMEOUT_SECONDS
        channel = interaction.channel
        self.cog.player_timers[player_id] = asyncio.create_task(
            self.cog._timeout_player(player_id, player_username, self.queue_id, timeout, channel)
        )

        # Check if queue is now full after joining
        if len(arrays.playerArr[self.queue_id]) == arrays.queueSize[self.queue_id]:
            await interaction.response.send_message(
                f"Get your asses online to play: {arrays.gameNameArr[self.queue_id]} | {', '.join(arrays.playerArr[self.queue_id])}"
            )
            # Clear the queue after 200 seconds
            await asyncio.sleep(200)
            if len(arrays.playerArr[self.queue_id]) == arrays.queueSize[self.queue_id]:
                tempPlayerArray = arrays.playerArr[self.queue_id].copy()
                for player in reversed(tempPlayerArray):
                    for index_game in range(len(arrays.gameNameArr)):
                        if player in arrays.playerArr[index_game]:
                            index_player = arrays.playerArr[index_game].index(player)
                            arrays.playerArr[index_game].remove(player)
                            arrays.playerArrString[index_game].pop(index_player)
                await interaction.followup.send("Players in full queue were removed from all queues")
        else:
            await interaction.response.send_message(
                player_username + f" has joined {arrays.gameNameArr[self.queue_id]}! Current queue: {', '.join(arrays.playerArrString[self.queue_id])}"
            )

    @nextcord.ui.button(label="Remove From Queue", style=nextcord.ButtonStyle.danger)
    async def remove_from_queue(self, button: nextcord.ui.Button, interaction: Interaction):
        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

        if player_id in arrays.playerArr[self.queue_id]:
            arrays.playerArr[self.queue_id].remove(player_id)
            arrays.playerArrString[self.queue_id].remove(player_username)
            # Cancel the user's timer if it exists
            if player_id in self.cog.player_timers:
                self.cog.player_timers[player_id].cancel()
                self.cog.player_timers.pop(player_id, None)
            await interaction.response.send_message(
                player_username + f" has been removed from {arrays.gameNameArr[self.queue_id]}."
            )
        else:
            await interaction.response.send_message(
                "You are not in this queue.",
                ephemeral=True
            )

def setup(client):
    client.add_cog(Ready(client))