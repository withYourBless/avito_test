from typing import Dict, List  # noqa: F401

from sqlalchemy.orm import Session

from src.logic.default_api_base import BaseDefaultApi

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

from src.logic.extra_models import TokenModel  # noqa: F401
from pydantic import StrictStr
from ..models.auth_request import AuthRequest
from ..models.auth_response import AuthResponse
from ..models.error_response import ErrorResponse
from ..models.info_response import InfoResponse
from ..models.send_coin_request import SendCoinRequest
from ..security_api import get_token_BearerAuth
from ...Exceptions import ItemGetException, UserGetException, NotEnoughMoneyException
from ...configuration.dsn import get_db

router = APIRouter()


@router.post(
    "/api/auth",
    responses={
        200: {"model": AuthResponse, "description": "Успешная аутентификация."},
        400: {"model": ErrorResponse, "description": "Неверный запрос."},
        401: {"model": ErrorResponse, "description": "Не авторизован."},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера."},
    },
    tags=["default"],
    summary="Аутентификация и получение JWT-токена. При первой аутентификации пользователь создается автоматически.",
    response_model_by_alias=True,
)
async def api_auth_post(
        auth_request: AuthRequest = Body(None, description=""),
        db: Session = Depends(get_db)
) -> AuthResponse:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_auth_post(db, auth_request)


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
        item: StrictStr = Path(..., description="Название товара"),
        token_BearerAuth: TokenModel = Security(
            get_token_BearerAuth),
        db: Session = Depends(get_db)
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseDefaultApi.subclasses[0]().api_buy_item_get(db, item, token_BearerAuth)
    except ItemGetException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(errors="Item not found").model_dump(),
        )
    except UserGetException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(errors="User not authorized").model_dump(),
        )
    except NotEnoughMoneyException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(errors="Not enough money").model_dump(),
        )


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
        db: Session = Depends(get_db)
) -> InfoResponse:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_info_get(db, token_BearerAuth)


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
        db: Session = Depends(get_db)
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseDefaultApi.subclasses[0]().api_send_coin_post(db, send_coin_request, token_BearerAuth)
    except NotEnoughMoneyException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(errors="Not enough money").model_dump(),
        )
