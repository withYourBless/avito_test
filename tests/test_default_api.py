# coding: utf-8
from http.client import responses

from fastapi.testclient import TestClient

from pydantic import StrictStr  # noqa: F401
from typing import Any  # noqa: F401
import requests

from src.endpoints.models.auth_request import AuthRequest  # noqa: F401
from src.endpoints.models.auth_response import AuthResponse  # noqa: F401
from src.endpoints.models.error_response import ErrorResponse  # noqa: F401
from src.endpoints.models.info_response import InfoResponse  # noqa: F401
from src.endpoints.models.send_coin_request import SendCoinRequest  # noqa: F401

base_url = "http://localhost:8080"


def create_user(username: str, password: str) -> str:
    data = {
        "username": username,
        "password": password,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(base_url + "/api/auth", json=data, headers=headers)
    assert response.status_code == 200

    return AuthResponse.from_dict(response.json()).token


def get_info(token: str) -> InfoResponse:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(base_url + "/api/info", headers=headers)
    assert response.status_code == 200
    return InfoResponse.from_dict(response.json())


def test_api_auth_post():
    """Test case for api_auth_post

    Аутентификация и получение JWT-токена. При первой аутентификации пользователь создается автоматически.
    """
    token1 = create_user("user1", "password")
    assert token1 != " "


def test_api_buy_item_get():
    """Test case for api_buy_item_get

    Купить предмет за монеты.
    """
    token1 = create_user("user1", "password")
    item = "book"

    headers = {
        "Authorization": f"Bearer {token1}",
        "Content-Type": "application/json"
    }

    info_before = get_info(token1)

    response = requests.get(base_url + "/api/buy/" + item, headers=headers)
    assert response.status_code == 200

    info_after = get_info(token1)

    assert info_after.coins == info_before.coins - 50
    assert info_after.inventory[0].type == "book"


def test_api_send_coin_post():
    """Test case for api_send_coin_post

    Отправить монеты другому пользователю.
    """
    token1 = create_user("user1", "password")
    token2 = create_user("user2", "password")

    user1 = get_info(token1)
    user2 = get_info(token2)

    coin_request = {
        "to_user": "user2",
        "amount": 1,
    }

    headers = {
        "Authorization": f"Bearer {token1}",
        "Content-Type": "application/json"
    }

    response = requests.post(base_url + "/api/sendCoin", json=coin_request, headers=headers)
    assert response.status_code == 200

    assert get_info(token1).coins == user1.coins - 1
    assert get_info(token2).coins == user2.coins + 1
