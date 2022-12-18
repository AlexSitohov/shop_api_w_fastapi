from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.sql.functions import count, sum, array_agg

import models
from database import get_db
from schemas import Item
from sqlalchemy.orm import Session

router = APIRouter(tags=['items'])


@router.post('/items/', status_code=status.HTTP_201_CREATED)
def create_item(item: Item, db: Session = Depends(get_db)):
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get('/items/', response_model=list[Item])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    # items_result = db.query(models.Item, func.sum(models.Rate.ball)).join(models.Rate,
    #                                                                       models.Rate.item_id == models.Item.id,
    #                                                                       isouter=True).group_by(
    #     models.Item.id).all()
    return items


@router.get('/items/{item_id}/')
def get_item(item_id: int, db: Session = Depends(get_db)):
    item_query = db.query(models.Item).filter(models.Item.id == item_id)
    item = item_query.first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    rating_item = db.query(models.Rate).filter(models.Rate.item_id == item_id).all()
    # items_result = db.query(models.Item, (func.sum(models.Rate.bal)
    #                         func.count(models.Rate.bal)).label('bal')).join(models.Rate,
    #                                                                           models.Rate.item_id == models.Item.id,
    #                                                                           isouter=True).group_by(
    #     models.Item.id).filter(models.Item.id == item_id).first()
    bal = 0
    for i in rating_item:
        bal += i.ball
    if len(rating_item) != 0:
        bal = bal / len(rating_item)

    return item, {'rating': bal}


@router.delete('/items/{item_id}/')
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    item.delete()
    db.commit()
    return {"msg": "deleted"}
