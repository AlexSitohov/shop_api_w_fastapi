from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import models
from database import engine
from routers import items, customers, make_order, authentication,rate

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(items.router)
app.include_router(customers.router)
app.include_router(make_order.router)
app.include_router(authentication.router)
app.include_router(rate.router)

