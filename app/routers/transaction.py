from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Query
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from datetime import date
from typing import Literal

from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.categorizer import categorize_transaction


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post("/")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    category = transaction.category

    if category is None:
        category = categorize_transaction(transaction.description)

    new_transaction = Transaction(
        description = transaction.description,
        amount = transaction.amount,
        category = category,
        date = transaction.date,
        transaction_type=transaction.transaction_type   
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@router.get("/")
def get_transactions(
    category: str | None = None,
    transaction_type: Literal["income","expense"] | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(default=20, ge=1,le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
    
):
    query = db.query(Transaction)

    if category is not None:
        query = query.filter(
            Transaction.category == category
        )
    if transaction_type is not None:
            query = query.filter(
                Transaction.transaction_type == transaction_type
        )
    if start_date is not None:
            query = query.filter(
                Transaction.date >= start_date
        )
    if end_date is not None:
            query = query.filter(
                Transaction.date <= end_date
        )
    if start_date is not None and end_date is not None:
         if start_date>end_date:
              raise HTTPException(
                   status_code=400,
                   detail="start_date cannot be after end_date"
              )
    transactions = query.order_by(
         Transaction.date.desc(),
         Transaction.id.desc()
    ).offset(offset).limit(limit).all()

    return transactions

@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction =db.query(Transaction).filter(
        Transaction.id==transaction_id
    ).first()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )
    return transaction

@router.put("/{transaction_id}")
def  update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id ==transaction_id
    ).first()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction.description=transaction_data.description
    transaction.amount=transaction_data.amount
    transaction.category=transaction_data.category
    transaction.date=transaction_data.date
    transaction.transaction_type=transaction_data.transaction_type

    db.commit()
    db.refresh(transaction)

    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session=Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return{
        "message":"Transaction deleted successfully"
    }

@router.post("/import-csv")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    df = pd.read_csv(BytesIO(contents))

    required_columns = {"date","description","amount","transaction_type"}

    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail="CSV must contain date, description, and amount columns"
        )

    ## Checking for empty Descriptions
    df["description"] = df["description"].astype("string").str.strip()

    if df["description"].isna().any() or df["description"].eq("").any():
        raise HTTPException(
            status_code=400,
            detail="Description cannot be empty"
        )

    ## Converting the Daters
    df["date"]= pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    if df["date"].isna().any():
        raise HTTPException(
            status_code=400,
            detail="CSV contains invalid dates"
        )

    ## Convert Amounts
    df["amount"]=pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    if df["amount"].isna().any():
        raise HTTPException(
            status_code=400,
            detail="CSV contains invalid amounts"
        )
    if (df["amount"]<=0).any():
        raise HTTPException(
            status_code=400,
            detail="Amounts must be greater than 0"
        )

    df["transaction_type"] = (
        df["transaction_type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )
    valid_types = {"income","expense"}

    if not df["transaction_type"].isin(valid_types).all():
        raise HTTPException(
            status_code=400,
            detail="transaction_type must be income or expense"
        )

    transactions = []

    for _, row in df.iterrows():

        category = categorize_transaction(
            row["description"]
        )

        transaction = Transaction(
            description=row["description"],
            amount=row["amount"],
            category=category,
            date=row["date"].date(),
            transaction_type=row["transaction_type"]
        )

        transactions.append(transaction)

    db.add_all(transactions)
    db.commit()

    return{
        "message": "CSV imported successfully",
        "rows_imported": len(transactions)
    }