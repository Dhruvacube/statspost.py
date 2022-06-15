import asyncio
import io
import logging
from typing import Dict, Union

import aiohttp

from . import __version__
from ._type import MISSING
from .enums import RequestTypes
from .errors import *

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


class BaseHTTP:
    """The base class for making http requests"""

    silently_fail: bool = True

    __slots__ = ()

    async def request(
        self,
        method: RequestTypes,
        _base_url: str,
        api_token: str,
        json: dict = MISSING,
        headers: dict = MISSING,
        bot: bool = False,
        bots: bool = False,
        retry: bool = True,
        retry_times: int = 1,
    ) -> Union[aiohttp.ClientResponse, Dict, io.IOBase]:
        """Makes an API request

        :raises RateLimited: When the 429 response is returned
        :raises WrongReturnType: When the :exc:`UnicodeDecodeError` is raised
        :raises ParameterError: When the 400 response is returned
        :raises Unauthorised: When the 401 response is returned
        :raises ApiError: When the 500 response is returned
        :raises HttpException: For the other and generall http exceptions
        :return: Bytes data for the image
        :rtype: Union[aiohttp.ClientResponse, dict, io.IOBase]
        """

        if json is MISSING:
            json = {}
        __base_url: str = (
            _base_url if _base_url.endswith("/") else _base_url.strip() + "/"
        )
        headers = {} if headers is MISSING else headers

        headers["Authorization"] = (
            api_token
            if not bot or not bots
            else f"Bot {api_token}"
            if bot
            else f"Bots {api_token}"
        )
        headers["User-Agent"] = f"botlist_statspost/{__version__}"
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"

        async with aiohttp.ClientSession() as session:
            async with session.request(
                str(method.name).upper(), __base_url, headers=headers, json=json
            ) as response:
                if response.status == 429:
                    if not retry:
                        raise RateLimited("Too many requests, try again later")
                    await asyncio.sleep(response.headers.get("Retry-After"))
                    return await self.request(
                        method,
                        __base_url,
                        json,
                        headers,
                        retry=retry_times <= 10,
                        retry_times=retry_times + 1,
                    )

                try:
                    result = await response.json(content_type="application/json")
                except UnicodeDecodeError:
                    logging.error(
                        "Something wrong with the return type, please check the API"
                    )
                    if not self.silently_fail:
                        raise WrongReturnType(
                            "Something wrong with the return type, please check the API"
                        )

                if response.status == 200:
                    return result

                logging.warning(result)
                if response.status == 400 and not self.silently_fail:
                    raise ParameterError(result)

                if response.status == 401:
                    logging.warning(result)
                    if not self.silently_fail:
                        raise Unauthorised(result)

                if response.status == 500 and not self.silently_fail:
                    raise ApiError(result)

                if not self.silently_fail:
                    raise HttpException(response.status, result)
