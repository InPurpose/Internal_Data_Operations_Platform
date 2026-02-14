from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,unique=True,nullable=False)
    category = Column(String,unique=False,nullable=False)
    price=Column(Float,unique=False,nullable=False)
    created_at= Column(DateTime, index=True)




"""
id
name
category
price
created_at
"""

