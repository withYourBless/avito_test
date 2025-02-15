from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = None
    username: str
    password: str
    coins: int = 0

class InventoryItem(BaseModel):
    id: Optional[str] = None
    user_id: str
    item_name: str
    quantity: int = 0

class TransactionType(str):
    RECEIVED = "received"
    SENT = "sent"

class CoinTransaction(BaseModel):
    id: Optional[str] = None
    user_id: str
    from_user_id: Optional[str] = None
    to_user_id: Optional[str] = None
    amount: int
    transaction_type: TransactionType
    timestamp: datetime = datetime.utcnow()

class Item(BaseModel):
    id: Optional[str] = None
    name: str
    price: int
    type: Optional[str] = None