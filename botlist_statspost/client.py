from typing import Dict, Literal, Mapping, Optional, Union, final, overload

from discord import AutoShardedClient, Client, ShardInfo
from discord.ext import commands

from ._type import MISSING
from .enums import RequestTypes
from .errors import NoBotListData
from .http import BaseHTTP

SUPPORTED_BOTLISTS = Literal[
    "topgg", 
    "discordbotlist", 
    "bladelist", 
    "discordlistspace", 
    "discordbotsgg"
]

@final
class StatusPost(BaseHTTP):
    botclass: Union[Client, AutoShardedClient, commands.Bot, commands.AutoShardedBot]
    botlist_data: Mapping[SUPPORTED_BOTLISTS, str] = MISSING
    retry: bool = True
    retry_times: int = 10

    def __init__(self) -> None:
        self.bot_id = self.botclass.id
        self.servers = len(self.botclass.guilds)
        self.shards: Mapping[int, ShardInfo] = self.botclass.shards if isinstance(self.botclass, AutoShardedClient) or isinstance(self.botclass, commands.AutoShardedBot) else MISSING
        self.shards_length: Union[Mapping[int, ShardInfo], int] = len(self.shards) if self.shards is not MISSING else 1
        self.users = len(self.botclass.users)
        self.voice = len(self.botclass.voice_clients)

    def __str__(self) -> str:
        return '<StatusPost servers={} shards={} users={}>'.format(self.servers, self.shards, self.users)
    
    def __repr__(self) -> str:
        return self.__str__()

    def add_botlist(self, botlist: SUPPORTED_BOTLISTS, token: str) -> None:
        """A helper function to add a botlist from the list of supported botliss

        :param botlist: Botlist name
        :type botlist: SUPPORTED_BOTLISTS
        :param token: The token provided by the botlist
        :type token: str
        """        
        self.botlist_data[botlist] = token
    
    @overload
    async def post_stats(self, return_post_data: Optional[bool] = None) -> Dict:
        ...
    
    @overload
    async def post_stats(self, return_post_data: MISSING) -> None:
        ...

    async def post_stats(self, return_post_data):
        if len(self.botlist_data) <= 0:
            raise NoBotListData("No botlist data provided")

        return_dict = {}

        #topgg
        if self.botlist_data.get("topgg"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://top.gg/api/bots/{self.bot_id}/stats",
                api_token=self.botlist_data["topgg"],
                json={
                    "server_count": self.servers,
                    "shard_count": self.shards_length,
                }
            )
            return_dict.update({"topgg": data})

        #discordbotlist
        if self.botlist_data.get("discordbotlist"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://discordbotlist.com/api/v1/bots/{self.bot_id}/stats",
                api_token=self.botlist_data["discordbotlist"],
                json={
                    "guilds": self.servers,
                    "users": self.users,
                    "voice_connections": self.voice,
                }
            )
            return_dict.update({"discordbotlist": data})
        
        #bladelist
        if self.botlist_data.get("bladelist"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.bladelist.gg/bots/{self.bot_id}/",
                api_token=f'Token self.botlist_data["bladelist"]',
                json={
                    "server_count": self.servers,
                    "shard_count": self.users,
                }
            )
            return_dict.update({"bladelist": data})
        
        #discordlistspace
        if self.botlist_data.get("discordlistspace"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.discordlist.space//bots/v2/bots/{self.bot_id}",
                api_token=self.botlist_data["discordlistspace"],
                json={
                    "serverCount": self.servers,
                }
            )
            return_dict.update({"discordlistspace": data})
        
        #discordbotsgg
        if self.botlist_data.get("discordbotsgg"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://discord.bots.gg/api/v1/bots/{self.bot_id}/stats",
                api_token=self.botlist_data["discordbotsgg"],
                json={
                    "guildCount": self.servers,
                    "shardCount": self.shards_length,
                }
            )
            return_dict.update({"discordbotsgg": data})
        
                    
