from fastapi import FastAPI

from app.database import Base, engine
from app.models.transaction import Transaction
from app.routers.transaction import router as transaction_router
from app.routers.analytics import router as analytics_router
from app.models.budget import Budget
from app.routers.budget import router as budget_router

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(transaction_router) 
app.include_router(analytics_router)
app.include_router(budget_router)

@app.get("/")
def home():
    return{"message":"Smart Expense API is Running"}