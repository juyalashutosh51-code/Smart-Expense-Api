from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate
from app.models.transaction import Transaction

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

@router.post("/")
def create_budget(
    budget: BudgetCreate,
    db:Session = Depends(get_db)
):
    new_budget = Budget(
        category=budget.category,
        amount=budget.amount,
        month=budget.month,
        year=budget.year
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return new_budget

@router.get("/")
def get_budgets(db:Session = Depends(get_db)):
    budgets = db.query(Budget).all()

    return budgets

@router.get("/summary")
def budget_summary(db: Session = Depends(get_db)):
    budgets = db.query(Budget).all()
    summary = []

    for budget in budgets:

        spent = db.query(
            func.sum(Transaction.amount)
        ).filter(
            Transaction.category == budget.category,
            Transaction.transaction_type == "expense",
            func.month(Transaction.date) == budget.month,
            func.year(Transaction.date) == budget.year
        ).scalar()

        spent = float(spent or 0)

        budget_amount = float(budget.amount)

        remaining = budget_amount - spent

        usage_percentage = (
            (spent / budget_amount) * 100
            if budget_amount>0
            else 0
        )
        status = "Over Budget" if spent > budget_amount else "Within Budget"

        summary.append({
            "category": budget.category,
            "budget": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "usage_percentage": round(usage_percentage,2),
            "status": status
        })

    return summary