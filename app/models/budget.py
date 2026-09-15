from sqlalchemy import Column,Integer,String,Numeric

from app.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer,primary_key=True,index=True)
    category = Column(String(100),nullable=False)
    amount = Column(Numeric(10,2),nullable=False)
    month = Column(Integer,nullable=False)
    year = Column(Integer,nullable=False)