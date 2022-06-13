import asyncio
import io
from typing import Union, Dict
from ._type import MISSING

import aiohttp

from . import __version__
from .enums import RequestTypes
from .errors import *


class BaseHTTP:
    def __init__(self) -> None:
        self.__user_agent: str = f"botlist_statspost/{__version__}"

    async def request(
        self,
        method: RequestTypes,
        _base_url: str,
        api_token: str,
        json: dict = MISSING,
        headers: dict = MISSING,
        bot: bool = MISSING,
        bots: bool = MISSING,
        retry: bool = True,
        retry_times: int = 1
    ) -> Union[aiohttp.ClientResponse, Dict, io.IOBase]:
        """Makes an API request"""
        if json is MISSING:
            json = {}
        __base_url: str = _base_url if _base_url.endswith('/') else _base_url.strip() + '/'
        headers = {} if headers is MISSING else headers

        headers["Authorization"] = api_token if bots is not MISSING or bots is not MISSING else f"Bot {api_token}" if bot else f"Bots {api_token}"
        headers["User-Agent"] = self.__user_agent
        headers["Content-Type"] = "application/json"

        async with aiohttp.ClientSession() as session:
            async with session.request(str(method.name).upper(), __base_url, headers=headers, json=json) as response:
                if response.status == 429:
                    if not retry:
                        raise RateLimited("Too many requests, try again later")
                    await asyncio.sleep(response.headers.get('Retry-After'))
                    return await self.request(method, __base_url, json, headers, retry=retry_times <= 10, retry_times=retry_times+1)

                if response.status == 200:
                    try:
                        result = await response.json(content_type="application/json")
                    except UnicodeDecodeError:
                        raise WrongReturnType("Something wrong with the return type, please check the API")
                    return result

                result = await response.json()
                if response.status == 400:
                    raise ParameterError(result["message"])

                if response.status == 401:
                    raise Unauthorised(result["message"])

                if response.status == 500:
                    raise ApiError(result["message"])

                raise HttpException(response.status, result)
