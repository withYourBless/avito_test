# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from endpoints.apis.default_api_base import BaseDefaultApi
import endpoints

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from endpoints.models.extra_models import TokenModel  # noqa: F401
from pydantic import StrictStr
from typing import Any
from endpoints.models.auth_request import AuthRequest
from endpoints.models.auth_response import AuthResponse
from endpoints.models.error_response import ErrorResponse
from endpoints.models.info_response import InfoResponse
from endpoints.models.send_coin_request import SendCoinRequest
from endpoints.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = endpoints
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/api/auth",
    responses={
        200: {"model": AuthResponse, "description": "Успешная аутентификация."},
        400: {"model": ErrorResponse, "description": "Неверный запрос."},
        401: {"model": ErrorResponse, "description": "Неавторизован."},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера."},
    },
    tags=["default"],
    summary="Аутентификация и получение JWT-токена. При первой аутентификации пользователь создается автоматически.",
    response_model_by_alias=True,
)
async def api_auth_post(
    auth_request: AuthRequest = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> AuthResponse:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_auth_post(auth_request)


@router.get(
    "/api/buy/{item}",
    responses={
        200: {"description": "Успешный ответ."},
        400: {"model": ErrorResponse, "description": "Неверный запрос."},
        401: {"model": ErrorResponse, "description": "Неавторизован."},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера."},
    },
    tags=["default"],
    summary="Купить предмет за монеты.",
    response_model_by_alias=True,
)
async def api_buy_item_get(
    item: StrictStr = Path(..., description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_buy_item_get(item)


@router.get(
    "/api/info",
    responses={
        200: {"model": InfoResponse, "description": "Успешный ответ."},
        400: {"model": ErrorResponse, "description": "Неверный запрос."},
        401: {"model": ErrorResponse, "description": "Неавторизован."},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера."},
    },
    tags=["default"],
    summary="Получить информацию о монетах, инвентаре и истории транзакций.",
    response_model_by_alias=True,
)
async def api_info_get(
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> InfoResponse:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_info_get()


@router.post(
    "/api/sendCoin",
    responses={
        200: {"description": "Успешный ответ."},
        400: {"model": ErrorResponse, "description": "Неверный запрос."},
        401: {"model": ErrorResponse, "description": "Неавторизован."},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера."},
    },
    tags=["default"],
    summary="Отправить монеты другому пользователю.",
    response_model_by_alias=True,
)
async def api_send_coin_post(
    send_coin_request: SendCoinRequest = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(
        get_token_BearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_send_coin_post(send_coin_request)
