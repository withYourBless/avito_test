import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from pydantic import StrictStr
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, Query

from src.Exceptions import NotEnoughMoneyException, UserGetException
from src.endpoints.models import db_models, dto
from src.endpoints.security_api import get_password_hash


def create_user(db: Session, username: str, password: str):
    u = db_models.User(id=str(uuid.uuid4()), username=username, password=password)
    u.password = get_password_hash(u.password)
    u.coins = 1000
    db.add(u)
    db.commit()
    db.refresh(u)


def add_inventory(db: Session, user_id: StrictStr, item_name: StrictStr):
    inventory = (
        db.query(db_models.Inventory)
        .filter(and_
                (db_models.Inventory.user_id == user_id,
                 db_models.Inventory.item_name == item_name)
                )
    ).first()
    logger.info(f"!!!!!!! Inventory: {inventory}")
    if inventory is not None:
        inventory.quantity = inventory.quantity + 1
    else:
        inventory = db_models.Inventory(id=str(uuid.uuid4()), item_name=item_name, user_id=user_id, quantity=1)
        db.add(inventory)
    db.commit()
    db.refresh(inventory)


def add_transaction(db: Session, from_user: db_models.User, to_user: db_models.User, amount: int):
    t_from = (db_models.CoinTransaction
        (
        id=str(uuid.uuid4()),
        user_id=from_user.id,
        from_user_id=from_user.id,
        to_user_id=to_user.id,
        amount=amount,
        transaction_type=db_models.TransactionType.sent))

    t_to = (db_models.CoinTransaction
        (
        id=str(uuid.uuid4()),
        user_id=to_user.id,
        from_user_id=from_user.id,
        to_user_id=to_user.id,
        amount=amount,
        transaction_type=db_models.TransactionType.received))
    db.add(t_to)
    db.add(t_from)
    db.commit()
    db.refresh(t_to)
    db.refresh(t_from)


def get_transaction(db: Session, user_id: str, transaction_type: dto.TransactionType):
    return (
        db.query(db_models.CoinTransaction)
        .filter(and_
                (db_models.CoinTransaction.user_id == user_id,
                 db_models.CoinTransaction.transaction_type == transaction_type)
                )
        .all()
    )


def get_user_by_name(db: Session, user_name: StrictStr):
    return db.query(db_models.User).filter(db_models.User.username == user_name).first()


def get_user_by_id(db: Session, user_id: StrictStr):
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()


def get_item_by_name(db: Session, item_name: StrictStr):
    return db.query(db_models.Item).filter(db_models.Item.name == item_name).first()


def buy_item(db: Session, user: dto.User, item_price: int):
    if user.coins < item_price:
        raise NotEnoughMoneyException

    user.coins -= item_price
    db.commit()
    db.refresh(user)


def get_inventory_by_user_id(db: Session, user_id: StrictStr):
    return db.query(db_models.Inventory).filter(db_models.Inventory.user_id == user_id).all()


def transfer_money(db: Session, from_user_id: StrictStr, to_user_name: StrictStr, coins: int):
    from_user = get_user_by_id(db, from_user_id)

    if from_user.coins < coins:
        raise NotEnoughMoneyException

    from_user.coins -= coins

    to_user = get_user_by_name(db, to_user_name)

    if to_user is None:
        raise UserGetException

    to_user.coins += coins

    db.commit()
    db.refresh(from_user)
    db.refresh(to_user)

    add_transaction(db, from_user, to_user, coins)
