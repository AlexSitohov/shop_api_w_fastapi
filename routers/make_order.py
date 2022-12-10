from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

import models
from database import get_db
from schemas import Order, OrderResponse, Customer
from sqlalchemy.orm import Session
from jwt import get_current_user
from services import payment

router = APIRouter(tags=['order'])


@router.post('/make/order/', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def make_order(order: Order, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    new_order = models.Order(date_time_created=datetime.now(), customer_id=current_user.dict().get('id_customer'),
                             item_id=order.item_id)
    payment(current_user.dict().get('id_customer'), order.item_id, db)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get('/orders/', response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    orders = db.query(models.Order).filter(models.Order.customer_id == current_user.dict().get('id_customer')).all()
    return orders