from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

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
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A budget with these details could not be saved. Check whether a budget already exists for this category, month, and year."
        )
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
@router.put("/{budget_id}")
def update_budget(
    budget_id: int,
    budget: BudgetCreate,
    db: Session = Depends(get_db)
):
    existing_budget = db.query(Budget).filter(
        Budget.id == budget_id
    ).first()

    if existing_budget is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    existing_budget.category = budget.category
    existing_budget.amount = budget.amount
    existing_budget.month = budget.month
    existing_budget.year = budget.year

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail= "A budget with these details could not be saved. Check whether a budget already exists for this category, month, and year."
        )

    db.refresh(existing_budget)

@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db)
):
    budget = db.query(Budget).filter(
        Budget.id == budget_id
    ).first()

    if budget is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    db.delete(budget)
    db.commit()

    return {
        "message": "Budget deleted successfully"
    }
        
    return existing_budget