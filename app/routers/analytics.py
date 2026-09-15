from fastapi import APIRouter,Depends
from sqlalchemy import func, cast, String
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/category-summary")
def category_summary(db:Session = Depends(get_db)):
    results = db.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).group_by(
        Transaction.category
    ).all()

    return [
        {
            "category": category,
            "total": float(total or 0)
        }
        for category, total in results
    ]

@router.get("/monthly-summary")
def monthly_summary(db: Session = Depends(get_db)):
    results = db.query(
        func.year(Transaction.date),
        func.month(Transaction.date),
        func.sum(Transaction.amount)
    ).group_by(
        func.year(Transaction.date),
        func.month(Transaction.date)
    ).order_by(
        func.year(Transaction.date),
        func.month(Transaction.date)
    ).all()

    return[
        {
            "year": year,
            "month": month,
            "total": float(total or 0)
        }
        for year, month, total in results
    ]