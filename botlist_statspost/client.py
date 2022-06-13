from typing import Dict, Literal, Mapping, Optional, final, overload

from ._type import MISSING
from .enums import RequestTypes
from .errors import NoBotListData
from .http import BaseHTTP

SUPPORTED_BOTLISTS = Literal["topgg", "discordbotlist"]

@final
class StatusPost(BaseHTTP):
    bot_id: int
    botlist_data: Mapping[SUPPORTED_BOTLISTS, str] = MISSING
    retry: bool = True
    retry_times: int = 10

    def __init__(self,servers: int, shards: int = 1, users: int = MISSING) -> None:
        self.servers = servers
        self.shards = shards
        self.users = users

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
                    "shard_count": self.shards,
                }
            )
            return_dict.update({"topgg": data})

