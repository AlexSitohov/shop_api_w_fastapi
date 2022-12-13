from sqlalchemy import *
from database import Base
from sqlalchemy.orm import relationship

order_items = Table('order_items', Base.metadata,
                    Column('order_id', ForeignKey('orders.id'), primary_key=True),
                    Column('item_id', ForeignKey('items.id'), primary_key=True)
                    )


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    orders = relationship("Order", secondary="order_items", back_populates="items")


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)
    balance = Column(Integer)
    is_staff = Column(Boolean, default=False)
    _orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    date_time_created = Column(DateTime)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))
    # item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'))
    customer = relationship("Customer", back_populates="_orders")
    items = relationship("Item", secondary="order_items", back_populates="orders")


class Rate(Base):
    __tablename__ = 'rates'
    item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), primary_key=True)
    ball = Column(Integer)
