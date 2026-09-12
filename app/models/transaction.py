from sqlalchemy import Column,Integer,String,Numeric,Date

from app.database import Base


class Transaction(Base):
    __tablename__="Transactions"

    id = Column(Integer,primary_key=True,index=True)
    description = Column(String(255),nullable=False)
    amount = Column(Numeric(10,2),nullable=False)
    category = Column(String(100),nullable=True)
    date = Column(Date,nullable=False)