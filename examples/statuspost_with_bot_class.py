from statspost import StatsPost
import asyncio, sys

import discord # type: ignore

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


a = StatsPost(botclass=client)
a.add_botlist("topgg", "topgg_token")


# setting up the windows loop policy according to the operating system
if sys.platform.startswith(("win32", "cygwin")):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@client.command()
async def post_stats(ctx):
    await ctx.send(f'```json\n{await a.post_stats(return_post_data=True)}\n```')

client.run('token')