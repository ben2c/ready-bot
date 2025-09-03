import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import arrays
import asyncio

class MultiReady(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.player_timers = {}  # {player_id: {queue_id: asyncio.Task}}

    testServerId = 389588257106690051
    DEFAULT_TIMEOUT_SECONDS = 3600

    @nextcord.slash_command(
        name='mr',
        description='Ready up for multiple queues for 1hr',
        guild_ids=[testServerId]
    )
    async def multiready(self, interaction: Interaction):
        view = MultiQueueSelectView(self)
        await interaction.response.send_message(
            "Select the queues you want to ready up for:",
            view=view,
            ephemeral=True
        )

class MultiQueueSelectView(nextcord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=60)
        self.cog = cog

        select = nextcord.ui.Select(
            placeholder="Choose queues...",
            min_values=1,
            max_values=len(arrays.gameNameArr),
            options=[
                nextcord.SelectOption(label=game, value=str(idx))
                for idx, game in enumerate(arrays.gameNameArr)
            ]
        )
        select.callback = lambda interaction: self.select_queues_callback(select, interaction)
        self.add_item(select)

    async def select_queues_callback(self, select: nextcord.ui.Select, interaction: Interaction):
        player_id = '<@' + str(interaction.user.id) + '>'
        player_username = interaction.user.global_name
        selected_indices = [int(v) for v in select.values]
        queued_games = []
        already_queued = []
        full_queues = []
        full_queue_ids = []

        for queue_id in selected_indices:
            if player_id in arrays.playerArr[queue_id]:
                already_queued.append(arrays.gameNameArr[queue_id])
                continue
            if len(arrays.playerArr[queue_id]) >= arrays.queueSize[queue_id]:
                full_queues.append(arrays.gameNameArr[queue_id])
                continue

            arrays.playerArr[queue_id].append(player_id)
            arrays.playerArrString[queue_id].append(player_username)
            queued_games.append(arrays.gameNameArr[queue_id])

            # Ensure player_timers[player_id] is a dict
            if player_id not in self.cog.player_timers or not isinstance(self.cog.player_timers[player_id], dict):
                self.cog.player_timers[player_id] = {}
            # Cancel any existing timer for this queue
            if queue_id in self.cog.player_timers[player_id]:
                task = self.cog.player_timers[player_id][queue_id]
                if not task.done():
                    task.cancel()
            # Create a new timeout task for this queue
            self.cog.player_timers[player_id][queue_id] = asyncio.create_task(
                self._timeout_player(player_id, player_username, queue_id, self.cog.DEFAULT_TIMEOUT_SECONDS, interaction.channel)
            )

            # If queue is now full, ping all players and schedule clearing
            if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                full_queue_ids.append(queue_id)
                await interaction.channel.send(
                    f"Get your asses online to play: {arrays.gameNameArr[queue_id]} | {', '.join(arrays.playerArr[queue_id])}"
                )

        # Schedule clearing for each full queue
        for queue_id in full_queue_ids:
            asyncio.create_task(self._clear_full_queue(queue_id, interaction.channel))

        # Send feedback to user
        messages = []
        if queued_games:
            messages.append(f"{player_username} queued for: {', '.join(queued_games)}")
        if already_queued:
            messages.append(f"Already queued for: {', '.join(already_queued)}")
        if full_queues:
            messages.append(f"Full queues: {', '.join(full_queues)}")
        await interaction.response.send_message('\n'.join(messages))

    async def _timeout_player(self, player_id, player_username, queue_id, timeout, channel):
        try:
            await asyncio.sleep(timeout)
            if player_id in arrays.playerArr[queue_id]:
                arrays.playerArr[queue_id].remove(player_id)
                arrays.playerArrString[queue_id].remove(player_username)
                # Track timed out queues
                if not hasattr(self, "timed_out_queues"):
                    self.timed_out_queues = {}
                if player_id not in self.timed_out_queues:
                    self.timed_out_queues[player_id] = []
                self.timed_out_queues[player_id].append(arrays.gameNameArr[queue_id])
        except asyncio.CancelledError:
            pass
        finally:
            if player_id in self.cog.player_timers:
                self.cog.player_timers[player_id].pop(queue_id, None)
                # If all timers for this player are done, send one timeout message
                if not self.cog.player_timers[player_id]:
                    self.cog.player_timers.pop(player_id, None)
                    if hasattr(self, "timed_out_queues") and player_id in self.timed_out_queues:
                        timed_out_games = ', '.join(self.timed_out_queues[player_id])
                        await channel.send(f"{player_username} timed out from: {timed_out_games}")
                        self.timed_out_queues.pop(player_id)

    async def _clear_full_queue(self, queue_id, channel):
        await asyncio.sleep(30)
        if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
            tempPlayerArray = arrays.playerArr[queue_id].copy()
            for player in reversed(tempPlayerArray):
                for idx in range(len(arrays.gameNameArr)):
                    if player in arrays.playerArr[idx]:
                        index_player = arrays.playerArr[idx].index(player)
                        arrays.playerArr[idx].remove(player)
                        arrays.playerArrString[idx].pop(index_player)
            await channel.send("Players in full queue were removed from all queues")

def setup(client):
    client.add_cog(MultiReady(client))