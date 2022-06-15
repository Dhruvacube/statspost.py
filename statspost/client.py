from typing import (
    TYPE_CHECKING,
    Dict,
    Iterable,
    Literal,
    Mapping,
    Optional,
    Union,
    final,
    get_args,
    overload,
)

if TYPE_CHECKING:
    from discord import AutoShardedClient, Client, ShardInfo  # type: ignore
    from discord.ext import commands  # type: ignore

from ._type import MISSING
from .enums import RequestTypes
from .errors import NoBotListData
from .http import BaseHTTP

SUPPORTED_BOTLISTS = Literal[
    "topgg",
    "discordbotlist",
    "bladelist",
    "discordlistspace",
    "discordbotsgg",
    "discordlabs",
    "discord-botlist.eu",
    "yabl",
    "voidbots",
    "radarbotdirectory",
    "blist",
    "botlist.me",
    "discords",
    "infinity",
    "motiondevelopment",
    "discordservices",
    "vcodes",
    "discordz",
    "fateslist",
    "disforge",
]

VALID_BOTLISTS: Iterable = get_args(SUPPORTED_BOTLISTS)


@final
class StatsPost(BaseHTTP):
    botclass: Union["Client", "AutoShardedClient", "commands.Bot", "commands.AutoShardedBot"] = MISSING  # type: ignore
    botlist_data: Mapping[SUPPORTED_BOTLISTS, str] = MISSING
    retry: bool = True
    retry_times: int = 10

    def __init__(self, *args, **kwargs) -> None:
        if len(kwargs) != 0 and self.botclass is MISSING:
            self.bot_id: int = kwargs.get("bot_id")
            self.servers: int = kwargs.get("servers", MISSING)
            if self.servers is MISSING:
                raise ValueError("You must provide a value for servers")
            self.shards: Mapping[int, "ShardInfo"] = kwargs.get("shards", MISSING)  # type: ignore
            self.shards_length: Union[Mapping[int, "ShardInfo"], int] = kwargs.get("shards_length", 1)  # type: ignore
            self.users: int = kwargs.get("users", None)
            self.voice: int = kwargs.get("voice", None)
            return
        if self.botclass is MISSING:
            raise ValueError("No bot class or kwargs provided")
        self.bot_id = self.botclass.id
        self.servers = len(self.botclass.guilds)
        self.shards: Mapping[int, "ShardInfo"] = self.botclass.shards if isinstance(self.botclass, "AutoShardedClient") or isinstance(self.botclass, "commands.AutoShardedBot") else MISSING  # type: ignore
        self.shards_length: Union[Mapping[int, "ShardInfo"], int] = len(self.shards) if self.shards is not MISSING else 1  # type: ignore
        self.users = len(self.botclass.users)
        self.voice = len(self.botclass.voice_clients)

    def __str__(self) -> str:
        return "<StatusPost servers={} shards={} users={}>".format(
            self.servers, self.shards, self.users
        )

    def __repr__(self) -> str:
        return self.__str__()

    def add_botlist(self, botlist: SUPPORTED_BOTLISTS, token: str) -> None:
        """A helper function to add a botlist from the list of supported botliss

        :param botlist: Botlist name
        :type botlist: SUPPORTED_BOTLISTS
        :param token: The token provided by the botlist
        :type token: str
        """
        if botlist not in VALID_BOTLISTS:
            raise RuntimeError("Invalid botlist")

        if self.botlist_data is MISSING:
            self.botlist_data = {}
        self.botlist_data[botlist] = token

    @overload
    async def post_stats(self, return_post_data: Optional[bool] = None) -> Dict:
        ...

    @overload
    async def post_stats(self, return_post_data=MISSING) -> None:
        ...

    async def post_stats(
        self, return_post_data: Optional[bool] = False
    ) -> Union[Dict, None]:
        if len(self.botlist_data) <= 0:
            raise NoBotListData("No botlist data provided")

        return_dict = {}

        # topgg
        if self.botlist_data.get("topgg"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://top.gg/api/bots/{self.bot_id}/stats",
                api_token=self.botlist_data["topgg"],
                json={
                    "server_count": self.servers,
                    "shard_count": self.shards_length,
                },
            )
            return_dict.update({"topgg": data})

        # discordbotlist
        if self.botlist_data.get("discordbotlist"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://discordbotlist.com/api/v1/bots/{self.bot_id}/stats",
                api_token=self.botlist_data["discordbotlist"],
                json={
                    "guilds": self.servers,
                    "users": self.users,
                    "voice_connections": self.voice,
                },
            )
            return_dict.update({"discordbotlist": data})

        # bladelist
        if self.botlist_data.get("bladelist"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.bladelist.gg/bots/{self.bot_id}/",
                api_token=f'Token {self.botlist_data["bladelist"]}',
                json={
                    "server_count": self.servers,
                    "shard_count": self.users,
                },
            )
            return_dict.update({"bladelist": data})

        # discordlistspace
        if self.botlist_data.get("discordlistspace"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.discordlist.space//bots/v2/bots/{self.bot_id}",
                api_token=self.botlist_data["discordlistspace"],
                json={
                    "serverCount": self.servers,
                },
            )
            return_dict.update({"discordlistspace": data})

        # discordbotsgg
        if self.botlist_data.get("discordbotsgg"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://discord.bots.gg/api/v1/bots/{self.bot_id}/stats",
                api_token=self.botlist_data["discordbotsgg"],
                json={
                    "guildCount": self.servers,
                    "shardCount": self.shards_length,
                },
            )
            return_dict.update({"discordbotsgg": data})

        # discordlabs
        if self.botlist_data.get("discordlabs"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://bots.discordlabs.org/v2/bot/{self.bot_id}/stats",
                api_token=self.botlist_data["discordlabs"],
                json={
                    "server_count": self.servers,
                    "shard_count": self.shards_length,
                },
            )
            return_dict.update({"discordlabs": data})

        # discord-botlist.eu
        if self.botlist_data.get("discord-botlist.eu"):
            data = await self.request(
                method=RequestTypes.PATCH,
                _base_url="https://api.discord-botlist.eu/v1/update",
                api_token=f'Bearer {self.botlist_data["discord-botlist.eu"]}',
                json={"serverCount": self.servers},
            )
            return_dict.update({"discord-botlist.eu": data})

        # yabl
        if self.botlist_data.get("yabl"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://yabl.xyz/api/bot/{self.bot_id}/stats",
                api_token=self.botlist_data["yabl"],
                json={"guildCount": self.servers},
            )
            return_dict.update({"yabl": data})

        # voidbots
        if self.botlist_data.get("voidbots"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.voidbots.net/stats/{self.bot_id}",
                api_token=self.botlist_data["voidbots"],
                json={
                    "server_count": self.servers,
                    "shard_count": self.shards_length,
                },
            )
            return_dict.update({"voidbots": data})

        # radarbotdirectory
        if self.botlist_data.get("radarbotdirectory"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://radarbotdirectory.xyz/api/bot/{self.bot_id}/stats",
                api_token=self.botlist_data["radarbotdirectory"],
                json={
                    "guilds": self.servers,
                    "shards": self.shards_length,
                },
            )
            return_dict.update({"radarbotdirectory": data})

        # blist
        if self.botlist_data.get("blist"):
            data = await self.request(
                method=RequestTypes.PATCH,
                _base_url=f"https://blist.xyz/api/v2/bot/{self.bot_id}/stats/",
                api_token=self.botlist_data["blist"],
                json={
                    "server_count": self.servers,
                    "shard_count": self.shards_length,
                },
            )
            return_dict.update({"blist": data})

        # botlist.me
        if self.botlist_data.get("botlist.me"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://botlist.me/api/v1/bots/{self.bot_id}/stats",
                api_token=self.botlist_data["botlist.me"],
                json={
                    "server_count": self.servers,
                    "shard_count": self.shards_length,
                },
            )
            return_dict.update({"botlist.me": data})

        # discords
        if self.botlist_data.get("discords"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://discords.com/bots/api/bot/{self.bot_id}",
                api_token=self.botlist_data["discords"],
                json={
                    "server_count": self.servers,
                },
            )
            return_dict.update({"discords": data})

        # infinity
        if self.botlist_data.get("infinity"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.infinitybotlist.com/bots/stats",
                api_token=self.botlist_data["infinity"],
                json={
                    "servers": self.servers,
                    "shards": self.shards_length,
                    "users": self.users,
                },
            )
            return_dict.update({"infinity": data})

        # motiondevelopment
        if self.botlist_data.get("motiondevelopment"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://www.motiondevelopment.top/api/v1.2//bots/{self.bot_id}/stats",
                api_token=self.botlist_data["motiondevelopment"],
                json={
                    "guilds": self.servers,
                },
            )
            return_dict.update({"motiondevelopment": data})

        # discordservices
        if self.botlist_data.get("discordservices"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.discordservices.net/bot/{self.bot_id}/stats",
                api_token=self.botlist_data["discordservices"],
                json={
                    "servers": self.servers,
                    "shards": self.shards_length,
                },
            )
            return_dict.update({"discordservices": data})

        # vcodes
        if self.botlist_data.get("vcodes"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://vcodes.xyz/api/v1/stats",
                api_token=self.botlist_data["vcodes"],
                json={
                    "guilds": self.servers,
                    "shards": self.shards_length,
                },
            )
            return_dict.update({"vcodes": data})

        # disforge
        if self.botlist_data.get("disforge"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://disforge.com/api/botstats/{self.bot_id}",
                api_token=self.botlist_data["disforge"],
                json={
                    "servers": self.servers,
                },
            )
            return_dict.update({"disforge": data})

        # fateslist
        if self.botlist_data.get("fateslist"):
            json_req = {
                "servers": self.servers,
                "shard_count": self.shards_length,
                "user_count": self.users,
            }
            if self.shards is not MISSING:
                json_req["shards"] = list(map(lambda x: x.id, self.shards.keys()))
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.fateslist.xyz/bots/{self.bot_id}/stats",
                api_token=self.botlist_data["fateslist"],
                json=json_req,
            )
            return_dict.update({"fateslist": data})

        # discordz
        if self.botlist_data.get("discordz"):
            data = await self.request(
                method=RequestTypes.POST,
                _base_url=f"https://api.discordz.gg/bot/{self.bot_id}/stats",
                api_token=self.botlist_data["discordz"],
                json={
                    "server_count": self.servers,
                    "shard_count": self.shards_length,
                    "user_count": self.users,
                },
            )
            return_dict.update({"discordz": data})

        if return_post_data:
            return return_dict
