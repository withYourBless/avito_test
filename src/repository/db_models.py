import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship

from src.configuration.dsn import Base


class TransactionType(enum.Enum):
    received = 'received'
    sent = 'sent'


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    coins = Column(Integer, default=0)

    inventory = relationship("Inventory", back_populates="user")
    sent_transactions = relationship("CoinTransaction", foreign_keys="[CoinTransaction.from_user_id]",
                                     back_populates="from_user")
    received_transactions = relationship("CoinTransaction", foreign_keys="[CoinTransaction.to_user_id]",
                                         back_populates="to_user")


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    item_name = Column(String(255))
    quantity = Column(Integer, default=0)

    user = relationship("User", back_populates="inventory")


class CoinTransaction(Base):
    __tablename__ = 'cointransactions'

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    from_user_id = Column(String, ForeignKey('users.id'))
    to_user_id = Column(String, ForeignKey('users.id'))
    amount = Column(Integer)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    timestamp = Column(DateTime, default=func.now())

    user = relationship("User", foreign_keys=[user_id], backref="cointransactions")
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_transactions")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_transactions")


class Item(Base):
    __tablename__ = 'items'

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
