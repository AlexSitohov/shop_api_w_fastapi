from fastapi import APIRouter, Depends, HTTPException, status

import models
from database import get_db
from jwt import get_current_user
from schemas import Customer
from sqlalchemy.orm import Session
from hash import hash

router = APIRouter(tags=['customers'])


@router.post('/customers/', status_code=status.HTTP_201_CREATED)
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    customer.password = hash(customer.password)
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@router.get('/customers/', response_model=list[Customer])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return customers


@router.get('/customers/{customer_id}/')
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return customer, {"orders": orders}


@router.delete('/customer/{customer_id}/')
def delete_item(customer_id: int, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    customer_query = db.query(models.Customer).filter(models.Customer.id == customer_id)
    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    if current_user.dict().get('id_customer') != customer.id and current_user.dict().get('is_stuff'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not allowed')
    customer_query.delete()
    db.commit()
    return {"msg": "deleted"}
