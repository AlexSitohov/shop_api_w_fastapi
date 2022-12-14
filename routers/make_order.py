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
    if not order.items_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Вы не выбрали ни одного продукта')
    items = []
    for i in order.items_id:
        item = db.query(models.Item).filter(models.Item.id == i).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'продукта с id {i} нет')

        items.append(item)
    new_order = models.Order(date_time_created=datetime.now(), customer_id=current_user.dict().get('id_customer'),
                             items=items)
    payment(current_user.dict().get('id_customer'), items, db)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get('/orders/', response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    orders = db.query(models.Order).filter(models.Order.customer_id == current_user.dict().get('id_customer')).all()
    return orders
