from typing import ClassVar, Dict, List, Tuple  # noqa: F401
import bcrypt
from pydantic import StrictStr

from src.endpoints.models.auth_request import AuthRequest
from src.endpoints.models.auth_response import AuthResponse
from src.logic.extra_models import TokenModel
from src.endpoints.models.info_response import InfoResponse, InfoResponseInventoryInner, InfoResponseCoinHistory
from src.endpoints.models.info_response_coin_history_received_inner import InfoResponseCoinHistoryReceivedInner
from src.endpoints.models.info_response_coin_history_sent_inner import InfoResponseCoinHistorySentInner
from src.endpoints.models.send_coin_request import SendCoinRequest
from sqlalchemy.orm import Session
from src.endpoints.security_api import create_access_token, get_password_hash
from src.repository import dto
from src.Exceptions import ItemGetException, UserGetException

from src.repository.repositories import add_inventory, get_transaction, create_user, get_item_by_name, \
    get_user_by_id, buy_item, get_inventory_by_user_id, transfer_money, get_user_by_name


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)


class MyBaseApi(BaseDefaultApi):
    async def api_auth_post(self, db: Session, auth_request: AuthRequest, ) -> AuthResponse:
        username = auth_request.username
        password = auth_request.password.get_secret_value()

        user = get_user_by_name(db, username)
        if user is not None:
            hashed_password = user.password
        else:
            create_user(db, username, password)
            hashed_password = get_password_hash(password)

        if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            return AuthResponse(token=None)

        user_id = get_user_by_name(db, username).id

        token = create_access_token(
            data={"username": username, "user_id": user_id}
        )

        return AuthResponse(token=token)

    async def api_buy_item_get(
            self, db: Session, item: StrictStr, token_user: TokenModel) -> None:
        item_obj = get_item_by_name(db, item)
        if not item_obj:
            raise ItemGetException

        item_price = item_obj.price

        user_id = token_user.user_id
        user = get_user_by_id(db, user_id)
        if not user:
            raise UserGetException

        buy_item(db, user, item_price)

        add_inventory(db, user_id, item)

    async def api_info_get(self, db: Session, token_user: TokenModel) -> InfoResponse:
        user = token_user
        user_id = user.user_id
        user = get_user_by_id(db, user_id)
        coins = user.coins
        inventory = get_inventory_by_user_id(db, user_id)
        transaction_sent = get_transaction(db, user_id, dto.TransactionType.SENT)
        transaction_received = get_transaction(db, user_id, dto.TransactionType.RECEIVED)
        response_inventory = []
        for item in inventory:
            response_inventory.append(InfoResponseInventoryInner(type=item.item_name, quantity=item.quantity))

        sent_transactions = []
        for s_transaction in transaction_sent:
            (sent_transactions.append
                (
                InfoResponseCoinHistorySentInner
                    (
                    to_user=s_transaction.to_user_id,
                    amount=s_transaction.amount
                )
            )
            )

        received_transactions = []
        for r_transaction in transaction_received:
            (
                received_transactions.append
                    (
                    InfoResponseCoinHistoryReceivedInner
                        (
                        to_user=r_transaction.from_user_id,
                        amount=r_transaction.amount
                    )
                )
            )

        history = InfoResponseCoinHistory(received=received_transactions, sent=sent_transactions)
        return InfoResponse(coins=coins, inventory=response_inventory, coin_history=history)

    async def api_send_coin_post(self, db: Session, send_coin_request: SendCoinRequest, token_user: TokenModel) -> None:
        from_user_id = token_user.user_id
        to_user_name = send_coin_request.to_user
        coins = send_coin_request.amount

        transfer_money(db, from_user_id, to_user_name, coins)
