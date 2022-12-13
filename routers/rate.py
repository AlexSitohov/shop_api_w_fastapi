from fastapi import APIRouter, Depends, status, HTTPException
from database import get_db
import models
from jwt import get_current_user
from schemas import Rate, Customer
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['rate']
)


@router.post('/rate/')
def rate(rate_data: Rate, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    rate_query = db.query(models.Rate).filter(models.Rate.item_id == rate_data.item_id,
                                              models.Rate.customer_id == current_user.dict().get('id_customer'))
    rate = rate_query.first()
    if rate:
        rate_query.delete()
        db.commit()
        return {'msg': 'оценка убрана'}
    if not rate:
        new_rate = models.Rate(**rate_data.dict(), customer_id=current_user.dict().get('id_customer'))
        db.add(new_rate)
        db.commit()
        db.refresh(new_rate)
        return {'msg': f'вы поставили оценку {new_rate.ball}'}
