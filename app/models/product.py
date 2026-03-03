from sqlalchemy import Column, Integer, String, Numeric, DateTime
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255),unique=True,nullable=False)
    category = Column(String,nullable=True, index=True)
    price=Column(Numeric(10, 2),unique=False,nullable=False)
    created_at= Column(DateTime, index=True)




"""
id
name
category
price
created_at
"""

