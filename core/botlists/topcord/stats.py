import aiohttp
from discord.ext import commands, tasks
from os import getenv


class TopCordStats(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.token: str = getenv("TOPCORD")
        self.post_topcord_stats.start()

    @tasks.loop(minutes=15)
    async def post_topcord_stats(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://topcord.xyz/api/bot/stats/{self.client.user.id}",
                                    json={"guilds": len(self.client.guilds), "shards": 0},
                                    headers={"Content-Type": "application/json", "Authorization": self.token}) as res:
                res_ = await res.json()
            if res.status != 200:
                print(f"\ntopcord API error:\n\n{res_}\n")
            else:
                print("topcord stats posted successfully")

    @post_topcord_stats.before_loop
    async def wait_until_ready(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(TopCordStats(client))
