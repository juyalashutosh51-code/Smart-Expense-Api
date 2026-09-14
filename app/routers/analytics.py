from fastapi import APIRouter,Depends
from sqlalchemy import func
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