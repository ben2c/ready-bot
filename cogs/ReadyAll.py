import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays
import asyncio
from cogs.MultiReady import MultiQueueSelectView

class ReadyAll(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.player_timers = {}  # Track player_id -> asyncio.Task

    testServerId = 389588257106690051
    TROLL_TIMEOUT_SECONDS = 60
    DEFAULT_TIMEOUT_SECONDS = 3600
    listOfTrolls = ["255976924428500993"]

    @nextcord.slash_command(
        name='rall', 
        description='Ready up for all queue for 1 hour', 
        guild_ids=[testServerId]
    )
    async def readyall(self, interaction: Interaction):
        channel = interaction.channel
        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

        # Check if player is already in all queues
        in_all_queues = all(
            player_id in arrays.playerArr[queue_id]
            for queue_id in range(len(arrays.gameNameArr))
        )
        if in_all_queues:
            await interaction.response.send_message("You are already in all queues!", ephemeral=True)
            return

        # Check if any queue is full
        full_queues = [
            arrays.gameNameArr[queue_id]
            for queue_id in range(len(arrays.gameNameArr))
            if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]
        ]
        if full_queues:
            await interaction.response.send_message(
                f"The following queues are already full: {', '.join(full_queues)}.\nPlease use the /r command for individual queues",
                ephemeral=True
            )
            return

        # Button view for joining all queues
        view = JoinAllQueuesView(self)

        await interaction.response.send_message(
            "Added to all queues for 1h",
            view=view
        )

        clear_queue = False
        for queue in arrays.gameNameArr:
            queue_id = arrays.gameNameArr.index(queue)
            if player_id not in arrays.playerArr[queue_id]:
                arrays.playerArr[queue_id].append(player_id)
                arrays.playerArrString[queue_id].append(player_username)
                if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                    await interaction.followup.send("Get online to play: " + arrays.gameNameArr[queue_id] + " | " + str(', '.join(arrays.playerArr[queue_id])))
                    clear_queue = True
                    clear_queue_id = queue_id

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
        self.player_timers[player_id] = asyncio.create_task(self._timeout_player(player_id, player_username, timeout, channel))

    async def _timeout_player(self, player_id, player_username, timeout, channel):
        try:
            await asyncio.sleep(timeout)
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
            pass
        finally:
            self.player_timers.pop(player_id, None)

class JoinAllQueuesView(nextcord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @nextcord.ui.button(label="Join All Queues", style=nextcord.ButtonStyle.primary)
    async def join_all_queues(self, button: nextcord.ui.Button, interaction: Interaction):
        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

        # Check if player is already in all queues
        in_all_queues = all(
            player_id in arrays.playerArr[queue_id]
            for queue_id in range(len(arrays.gameNameArr))
        )
        if in_all_queues:
            await interaction.response.send_message("You are already in all queues!", ephemeral=True)
            return

        # Check if any queue is full
        full_queues = [
            arrays.gameNameArr[queue_id]
            for queue_id in range(len(arrays.gameNameArr))
            if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]
        ]
        if full_queues:
            await interaction.response.send_message(
                f"The following queues are already full: {', '.join(full_queues)}.\nPlease use the /ready command for individual queues",
                ephemeral=True
            )
            return

        clear_queue = False
        clear_queue_id = None

        for queue in arrays.gameNameArr:
            queue_id = arrays.gameNameArr.index(queue)
            if player_id not in arrays.playerArr[queue_id]:
                arrays.playerArr[queue_id].append(player_id)
                arrays.playerArrString[queue_id].append(player_username)
                # Check if queue is now full after joining
                if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                    clear_queue = True
                    clear_queue_id = queue_id
                    await interaction.response.send_message(
                        f"Get online to play: {arrays.gameNameArr[queue_id]} | {', '.join(arrays.playerArr[queue_id])}"
                    )

        # Cancel any existing timer for this player
        if player_id in self.cog.player_timers:
            self.cog.player_timers[player_id].cancel()

        # Start timeout task for this player
        timeout = self.cog.TROLL_TIMEOUT_SECONDS if interaction.user.id in self.cog.listOfTrolls else self.cog.DEFAULT_TIMEOUT_SECONDS
        channel = interaction.channel
        self.cog.player_timers[player_id] = asyncio.create_task(
            self.cog._timeout_player(player_id, player_username, timeout, channel)
        )

        if clear_queue == False:
            await interaction.channel.send(player_username + " has joined all queues for 1h")

        # If any queue is full, clear it after 200 seconds
        if clear_queue and clear_queue_id is not None:
            await asyncio.sleep(200)
            if len(arrays.playerArr[clear_queue_id]) == arrays.queueSize[clear_queue_id]:
                tempPlayerArray = arrays.playerArr[clear_queue_id].copy()
                for player in reversed(tempPlayerArray):
                    for index_game in range(len(arrays.gameNameArr)):
                        if player in arrays.playerArr[index_game]:
                            index_player = arrays.playerArr[index_game].index(player)
                            arrays.playerArr[index_game].remove(player)
                            arrays.playerArrString[index_game].pop(index_player)
                await channel.send("Players in full queue were removed from all queues")

    @nextcord.ui.button(label="Remove From All Queues", style=nextcord.ButtonStyle.danger)
    async def not_ready(self, button: nextcord.ui.Button, interaction: Interaction):
        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

        removed = False
        for queue in arrays.playerArr:
            queue_id = arrays.playerArr.index(queue)
            if player_id in arrays.playerArr[queue_id]:
                arrays.playerArr[queue_id].remove(player_id)
                arrays.playerArrString[queue_id].remove(player_username)
                removed = True

        # Cancel the user's timer if it exists
        timer = self.cog.player_timers.get(player_id)
        if timer:
            if isinstance(timer, dict):
                for task in timer.values():
                    task.cancel()
            else:
                timer.cancel()
            self.cog.player_timers.pop(player_id, None)

        if removed:
            await interaction.response.send_message(player_username + " has been removed from all queues")
        else:
            await interaction.response.send_message("You were not in any queues", ephemeral=True)

    @nextcord.ui.button(label="MultiReady", style=nextcord.ButtonStyle.success)
    async def multiready_button(self, button: nextcord.ui.Button, interaction: Interaction):
        # Show the MultiReady multi-select view
        view = MultiQueueSelectView(self.cog)
        await interaction.response.send_message(
            "Select the queues you want to ready up for:",
            view=view,
            ephemeral=True
        )

def setup(client):
    client.add_cog(ReadyAll(client))