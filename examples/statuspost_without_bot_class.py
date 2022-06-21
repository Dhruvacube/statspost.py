from statspost import StatsPost
import asyncio, sys

a = StatsPost(bot_id=935242576343224352, servers=80)
a.add_botlist("topgg", "topgg_token")

# setting up the windows loop policy according to the operating system
if sys.platform.startswith(("win32", "cygwin")):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

print(asyncio.run(a.post_stats(return_post_data=True)))
