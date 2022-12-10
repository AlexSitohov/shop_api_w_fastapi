from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

import models
from database import get_db
from schemas import Order, OrderResponse, Customer
from sqlalchemy.orm import Session


def payment(customer_id, item_id, db: Session):
    client = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    dish = db.query(models.Item).filter(models.Item.id == item_id).first()
    if client.balance - dish.price < 0:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail='не хватает денег')
    client.balance -= dish.price
    db.commit()
    db.refresh(client)
