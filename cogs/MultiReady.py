import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import arrays
import asyncio

class MultiReady(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.player_timers = {}  # Track player_id -> {queue_id: asyncio.Task}

    testServerId = 389588257106690051
    TROLL_TIMEOUT_SECONDS = 60
    DEFAULT_TIMEOUT_SECONDS = 3600
    listOfTrolls = ["255976924428500993"]

    @nextcord.slash_command(
        name='mr',
        description='Ready up for multiple specific queues for 1 hour',
        guild_ids=[testServerId]
    )
    async def multiready(
        self,
        interaction: Interaction
    ):
        # Multi-select menu for queues
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
        self.timed_out_queues = {}

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
        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name
        selected_indices = [int(v) for v in select.values]
        queued_games = []
        already_queued = []
        full_queues = []
        for queue_id in selected_indices:
            if player_id in arrays.playerArr[queue_id]:
                already_queued.append(arrays.gameNameArr[queue_id])
                continue
            if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                full_queues.append(arrays.gameNameArr[queue_id])
                continue
            arrays.playerArr[queue_id].append(player_id)
            arrays.playerArrString[queue_id].append(player_username)
            queued_games.append(arrays.gameNameArr[queue_id])

            if player_id in self.cog.player_timers and queue_id in self.cog.player_timers[player_id]:
                self.cog.player_timers[player_id][queue_id].cancel()

            timeout = self.cog.TROLL_TIMEOUT_SECONDS if interaction.user.id in self.cog.listOfTrolls else self.cog.DEFAULT_TIMEOUT_SECONDS
            channel = interaction.channel
            if player_id not in self.cog.player_timers:
                self.cog.player_timers[player_id] = {}
            if player_id not in self.timed_out_queues:
                self.timed_out_queues[player_id] = []
            self.cog.player_timers[player_id][queue_id] = asyncio.create_task(
                self._timeout_player(player_id, player_username, queue_id, timeout, channel)
            )

            if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                await interaction.channel.send(
                    f"Get your asses online to play: {arrays.gameNameArr[queue_id]} | {', '.join(arrays.playerArr[queue_id])}"
                )
                await asyncio.sleep(200)
                if len(arrays.playerArr[queue_id]) == arrays.queueSize[queue_id]:
                    tempPlayerArray = arrays.playerArr[queue_id].copy()
                    for player in reversed(tempPlayerArray):
                        for index_game in range(len(arrays.gameNameArr)):
                            if player in arrays.playerArr[index_game]:
                                index_player = arrays.playerArr[index_game].index(player)
                                arrays.playerArr[index_game].remove(player)
                                arrays.playerArrString[index_game].pop(index_player)
                    await interaction.channel.send("Players in full queue were removed from all queues")

        messages = []
        if queued_games:
            messages.append(f"{player_username} queued for: {', '.join(queued_games)} for 1h")
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
                # Add to timed out queues
                if player_id not in self.timed_out_queues:
                    self.timed_out_queues[player_id] = []
                self.timed_out_queues[player_id].append(arrays.gameNameArr[queue_id])
        except asyncio.CancelledError:
            pass
        finally:
            if player_id in self.cog.player_timers:
                self.cog.player_timers[player_id].pop(queue_id, None)
                if not self.cog.player_timers[player_id]:
                    self.cog.player_timers.pop(player_id, None)
                    # Send single timeout message when all timers are done
                    if player_id in self.timed_out_queues and self.timed_out_queues[player_id]:
                        await channel.send(
                            f"{player_username} timed out from: {', '.join(self.timed_out_queues[player_id])}"
                        )
                        self.timed_out_queues.pop(player_id)

def setup(client):
    client.add_cog(MultiReady(client))