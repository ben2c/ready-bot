import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import arrays

class UnreadyAll(commands.Cog):
    def __init__(self, client):
        self.client = client

    testServerId = 389588257106690051

    @nextcord.slash_command(
        name='nrall',
        description='Unready for all queues',
        guild_ids=[testServerId]
    )
    async def unreadyall(self, interaction: Interaction):

        player_id = '<@' + f'{interaction.user.id}' + '>'
        player_username = interaction.user.global_name

        removed = False
        for queue in arrays.playerArr:
            queue_id = arrays.playerArr.index(queue)
            if player_id in arrays.playerArr[queue_id]:
                arrays.playerArr[queue_id].remove(player_id)
                arrays.playerArrString[queue_id].remove(player_username)
                removed = True

        # Cancel the user's timer in MultiReady cog if it exists
        multiready_cog = self.client.get_cog("MultiReady")
        if multiready_cog:
            timers = multiready_cog.player_timers.get(player_id)
            if timers:
                for task in timers.values():
                    task.cancel()
                multiready_cog.player_timers.pop(player_id, None)

        # Cancel the user's timer in ReadyAll cog if it exists
        readyall_cog = self.client.get_cog("ReadyAll")
        if readyall_cog:
            timer = readyall_cog.player_timers.get(player_id)
            if timer:
                if isinstance(timer, dict):
                    for task in timer.values():
                        task.cancel()
                else:
                    timer.cancel()
                readyall_cog.player_timers.pop(player_id, None)

        # Cancel the user's timer in Ready cog if it exists
        ready_cog = self.client.get_cog("Ready")
        if ready_cog:
            timer = ready_cog.player_timers.get(player_id)
            if timer:
                if isinstance(timer, dict):
                    for task in timer.values():
                        task.cancel()
                else:
                    timer.cancel()
                ready_cog.player_timers.pop(player_id, None)

        # Cancel the user's timer in TimeReady cog if it exists
        timeready_cog = self.client.get_cog("TimeReady")
        if timeready_cog:
            timer = timeready_cog.player_timers.get(player_id)
            if timer:
                if isinstance(timer, dict):
                    for task in timer.values():
                        task.cancel()
                else:
                    timer.cancel()
                timeready_cog.player_timers.pop(player_id, None)

        # Cancel the user's timer in TimeReadyAll cog if it exists
        timereadyall_cog = self.client.get_cog("TimeReadyAll")
        if timereadyall_cog:
            timer = timereadyall_cog.player_timers.get(player_id)
            if timer:
                if isinstance(timer, dict):
                    for task in timer.values():
                        task.cancel()
                else:
                    timer.cancel()
                timereadyall_cog.player_timers.pop(player_id, None)

        if removed:
            await interaction.response.send_message("You have been removed from all queues")
        else:
            await interaction.response.send_message("You're not in any queues", ephemeral=True)

def setup(client):
    client.add_cog(UnreadyAll(client))