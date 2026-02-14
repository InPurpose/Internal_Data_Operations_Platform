from sqlalchemy import Column, Integer, String, Float, DateTime,ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer,unique=False,index=True)
    amount = Column(Float,unique=False,index=True)
    order_time= Column(DateTime, index=True)
    status = Column(String)
    
    user = relationship("User", back_populates="orders")







"""id
user_id (ForeignKey)
product_id (ForeignKey)
quantity
amount
order_time
status
"""