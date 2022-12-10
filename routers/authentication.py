from fastapi import APIRouter, Depends, HTTPException, status

import models
# from schemas import Login
from database import get_db
from sqlalchemy.orm import Session
from hash import verify_password
from jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['authentication'])


@router.post('/login', status_code=status.HTTP_200_OK)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.name == login_data.username)
    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid username')
    if not verify_password(login_data.password, customer.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')
    access_token = create_access_token(data={'id_customer': customer.id,
                                             'name_customer': customer.name,
                                             'is_staff': customer.is_staff})
    return {"access_token": access_token, "token_type": "bearer"}
