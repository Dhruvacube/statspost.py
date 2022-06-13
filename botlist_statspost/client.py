from typing import Literal, Mapping

from ._type import MISSING
from .enums import RequestTypes
from .errors import NoBotListData
from .http import BaseHTTP

SUPPORTED_BOTLISTS = Literal["topgg", "discordbotlist"]

class StatusPost(BaseHTTP):
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
    
    async def post_stats(self):
        if len(self.botlist_data) <= 0:
            raise NoBotListData("No botlist data provided")
        
        if self.botlist_data.get("topgg"):
            await self.request(
                method=RequestTypes.POST, 
                _base_url=""
            )
