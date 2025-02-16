from unittest.mock import patch
from pydantic import StrictStr  # noqa: F401
from typing import Any  # noqa: F401

from src.endpoints.models.auth_request import AuthRequest
from src.endpoints.models.send_coin_request import SendCoinRequest
from src.logic.extra_models import TokenModel
from src.endpoints.security_api import decode_token, get_password_hash

from src.logic.default_api_base import MyBaseApi
from src.repository import db_models
from unittest import IsolatedAsyncioTestCase


class TestLogic(IsolatedAsyncioTestCase):
    async def test_api_auth_post(self):
        with (patch('src.logic.default_api_base.get_user_by_name') as get_user_by_name):
            get_user_by_name.return_value = db_models.User(username='nastya', password=get_password_hash('password'), id="2")

            service = MyBaseApi()
            auth = await service.api_auth_post(None, AuthRequest(username='nastya', password='password'))

            dec_token = decode_token(auth.token)

            assert dec_token.username == 'nastya'
            assert get_user_by_name.call_count == 2



    async def test_api_buy_item_get(self):
        with (patch('src.logic.default_api_base.get_item_by_name') as get_item_by_name,
              patch('src.logic.default_api_base.get_user_by_id') as get_user_by_id,
              patch('src.logic.default_api_base.buy_item') as buy_item_f,
              patch('src.logic.default_api_base.add_inventory') as add_inventory):

            get_item_by_name.return_value = db_models.Item(id="1", name="t-shirt", price=10)
            get_user_by_id.return_value = db_models.User(coins=100)

            service = MyBaseApi()
            buy_item_get = await service.api_buy_item_get(None, "t-shirt", TokenModel(user_id="1", username="nastya"))

            assert get_item_by_name.call_count == 1
            assert get_user_by_id.call_count == 1
            assert buy_item_f.call_count == 1
            assert add_inventory.call_count == 1


    async def test_api_send_coin_post(self):
        with (patch('src.logic.default_api_base.transfer_money') as transfer_money):
            service = MyBaseApi()
            # Act
            send_coins = await service.api_send_coin_post(None, SendCoinRequest(to_user="nastya2", amount=10), TokenModel(user_id="1", username="nastya"))

            assert transfer_money.call_count == 1


    async def test_api_info_get(self):
        with (patch('src.logic.default_api_base.get_transaction') as get_transaction,
              patch('src.logic.default_api_base.get_user_by_id') as get_user_by_id,
              patch('src.logic.default_api_base.get_inventory_by_user_id') as get_inventory_by_user_id):
            get_transaction.side_effect = [[db_models.CoinTransaction(user_id="1", amount=100)],
                                           [db_models.CoinTransaction(user_id="2", amount=100)]]

            get_user_by_id.return_value = db_models.User(coins=100)

            get_inventory_by_user_id.return_value = [
                db_models.Inventory(id="1", user_id="2", item_name="t-shirt", quantity=1)
            ]
            service = MyBaseApi()

            # Act
            info_response = await service.api_info_get(None, TokenModel(user_id="1", username="nastya"))

            # Assert
            assert info_response.coins == 100
            assert get_transaction.call_count == 2


