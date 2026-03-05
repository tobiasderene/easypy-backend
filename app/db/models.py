from sqlalchemy import (
    Column, Integer, String, Numeric, Boolean,
    TIMESTAMP, ForeignKey
)
from sqlalchemy.orm import relationship
from app.db.database import Base


class Logistics(Base):
    __tablename__ = 'logistics'

    logistic_id = Column(Integer, primary_key=True)

    orders = relationship("Order", back_populates="logistics")


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_nickname = Column(String, nullable=False)
    user_role = Column(String, nullable=False)
    user_status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    user_description = Column(String, nullable=False)

    wallet = relationship("Wallet", back_populates="user", uselist=False)
    products = relationship("Product", back_populates="user")
    orders_as_buyer = relationship("Order", foreign_keys="Order.buyer_id", back_populates="buyer")
    orders_as_supplier = relationship("Order", foreign_keys="Order.supplier_id", back_populates="supplier")
    order_status_changes = relationship("OrderStatusHistory", back_populates="changed_by_user")
    oauth_account = relationship("OAuthAccount", back_populates="user", uselist=False)
    images = relationship("Image", back_populates="user")

class Wallet(Base):
    __tablename__ = 'wallets'

    wallet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    balance_available = Column(Numeric(15, 2), nullable=False)
    balance_pending = Column(Numeric(15, 2), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="wallet")
    transactions = relationship("Transaction", back_populates="wallet")
    withdrawals = relationship("Withdrawal", back_populates="wallet")


class Withdrawal(Base):
    __tablename__ = 'withdrawls'

    withdrawls_id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Numeric(15, 2), nullable=False)
    wallet_id = Column(Integer, ForeignKey('wallets.wallet_id'), nullable=False)
    status = Column(String, nullable=False)
    bank_account_address = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    processed_at = Column(TIMESTAMP, nullable=False)

    wallet = relationship("Wallet", back_populates="withdrawals")
    bank_movements = relationship("BankMovement", back_populates="withdrawal")


class BankMovement(Base):
    __tablename__ = 'bank_movements'

    bank_movement_id = Column(Integer, primary_key=True, autoincrement=True)
    bank_movement_type = Column(String, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    reference_number = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    withdrawls_id = Column(Integer, ForeignKey('withdrawls.withdrawls_id'), nullable=True)

    withdrawal = relationship("Withdrawal", back_populates="bank_movements")
    orders_for_bank_movements = relationship("OrderForBankMovement", back_populates="bank_movement")


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    product_base_cost = Column(Numeric(15, 2), nullable=False)
    product_sku = Column(String, nullable=False)
    product_status = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_category = Column(String, nullable=False)
    product_discount = Column(Numeric, nullable=False)

    user = relationship("User", back_populates="products")
    orders = relationship("Order", back_populates="product")
    images = relationship("Image", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    logistic_id = Column(Integer, ForeignKey('logistics.logistic_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    final_price = Column(Numeric(15, 2), nullable=False)
    supplier_cost = Column(Numeric(15, 2), nullable=False)
    logistic_cost = Column(Numeric(15, 2), nullable=False)
    platform_fee = Column(Numeric(15, 2), nullable=False)
    buyer_profit = Column(Numeric(15, 2), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="orders_as_buyer")
    supplier = relationship("User", foreign_keys=[supplier_id], back_populates="orders_as_supplier")
    logistics = relationship("Logistics", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    transactions = relationship("Transaction", back_populates="order")
    status_history = relationship("OrderStatusHistory", back_populates="order")
    orders_for_bank_movements = relationship("OrderForBankMovement", back_populates="order")


class OrderForBankMovement(Base):
    __tablename__ = 'orders_for_bank_movements'

    bank_movement_id = Column(Integer, ForeignKey('bank_movements.bank_movement_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)

    bank_movement = relationship("BankMovement", back_populates="orders_for_bank_movements")
    order = relationship("Order", back_populates="orders_for_bank_movements")


class Transaction(Base):
    __tablename__ = 'transactions'

    id_transaction = Column(Integer, primary_key=True, autoincrement=True)
    wallet_id = Column(Integer, ForeignKey('wallets.wallet_id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=True)
    transaction_category = Column(String, nullable=False)
    transaction_direction = Column(String, nullable=False)
    transaction_amount = Column(Numeric(15, 2), nullable=False)
    transaction_status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    wallet = relationship("Wallet", back_populates="transactions")
    order = relationship("Order", back_populates="transactions")


class OrderStatusHistory(Base):
    __tablename__ = 'order_status_history'

    order_status_history_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    previous_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    changed_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    order = relationship("Order", back_populates="status_history")
    changed_by_user = relationship("User", back_populates="order_status_changes")


class Image(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, nullable=False, default=False)
    position = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)

    product = relationship("Product", back_populates="images")
    user = relationship("User", back_populates="images")


class OAuthAccount(Base):
    __tablename__ = 'oauth_accounts'

    oauth_account_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    google_id = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="oauth_account")
