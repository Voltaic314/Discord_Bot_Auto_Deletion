"""
Author: Logan Maupin

This is just a simple discord bot that deletes messages from a specified channel given certain parameters. Such as:
What channel to delete from and how long should the messages last.
"""
import discord
import asyncio
import time
import secrets


class Focus_Bot_Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Enable the GUILD_MEMBERS intent
        super().__init__(intents=intents)
        self.synced = False  # we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        # wait for the bot to be set up properly
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")

        # when we start up the bot, run the check to remove anyone in the database who shouldn't be in there anymore.
        self.loop.create_task(self.bot_routines())

    async def bot_routines(self):
        await self.wait_until_ready()

        # PLEASE NOTE: if you input your server id and the channel id, you need to replace the quotes as well.
        # Just input the numbers without quotes around them.
        server_id = secrets.secret_stuff["server_id"]
        guild = client.get_guild(server_id)
        auto_delete_channel = guild.get_channel(secrets.secret_stuff["auto_delete_channel_id"])

        # now we'll look to see if any messages need to be deleted from the auto delete channel
        # if so, then delete them, if not just ignore.
        while True:
            async for message in auto_delete_channel.history(limit=None, oldest_first=True):
                current_time = time.time()
                desired_hours_until_deletion = 24
                number_of_seconds_in_an_hour = 3600
                expiration_time_in_seconds = number_of_seconds_in_an_hour * desired_hours_until_deletion
                time_difference = current_time - message.created_at.timestamp()
                message_is_overdue_for_deletion = time_difference >= expiration_time_in_seconds

                if not message.pinned and message_is_overdue_for_deletion:
                    await message.delete()

            await asyncio.sleep(60)


client = Focus_Bot_Client()
tree = discord.app_commands.CommandTree(client)
TOKEN = secrets.secret_stuff["discord_bot_api_token"]
client.run(TOKEN)
