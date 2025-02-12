# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import StrictStr
from typing import Any
from endpoints.models.auth_request import AuthRequest
from endpoints.models.auth_response import AuthResponse
from endpoints.models.error_response import ErrorResponse
from endpoints.models.info_response import InfoResponse
from endpoints.models.send_coin_request import SendCoinRequest
from endpoints.security_api import get_token_BearerAuth

class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def api_auth_post(
        self,
        auth_request: AuthRequest,
    ) -> AuthResponse:
        ...


    async def api_buy_item_get(
        self,
        item: StrictStr,
    ) -> None:
        ...


    async def api_info_get(
        self,
    ) -> InfoResponse:
        ...


    async def api_send_coin_post(
        self,
        send_coin_request: SendCoinRequest,
    ) -> None:
        ...
