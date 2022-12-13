from fastapi import APIRouter, Depends, HTTPException, status
import models
from sqlalchemy.orm import Session


def payment(customer_id, items, db: Session):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    items_prices = [item.price for item in items]
    result_summa = sum(items_prices)

    if customer.balance - result_summa < 0:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail='не хватает денег')
    customer.balance -= result_summa
    db.commit()
    db.refresh(customer)
