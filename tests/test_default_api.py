# coding: utf-8

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

def test_api_auth_post():
    """Test case for api_auth_post

    Аутентификация и получение JWT-токена. При первой аутентификации пользователь создается автоматически.
    """
    token1 = create_user("user1", "password")
    assert token1 != " "




def test_api_buy_item_get(client: TestClient):
    """Test case for api_buy_item_get

    Купить предмет за монеты.
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/api/buy/{item}".format(item='item_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_api_info_get(client: TestClient):
    """Test case for api_info_get

    Получить информацию о монетах, инвентаре и истории транзакций.
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/api/info",
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_api_send_coin_post(client: TestClient):
    """Test case for api_send_coin_post

    Отправить монеты другому пользователю.
    """
    send_coin_request = {"to_user": "toUser", "amount": 0}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/api/sendCoin",
    #    headers=headers,
    #    json=send_coin_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
