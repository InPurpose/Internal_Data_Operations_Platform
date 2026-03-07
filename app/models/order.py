from sqlalchemy import Column, Integer, String, Numeric, DateTime,ForeignKey, Index
from app.db.base import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        Index("idx_orders_status_time", "status", "order_time"),
        Index("idx_orders_user_time","user_id", "order_time"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer,index=True)
    amount = Column(Numeric(10, 2),index=True)
    order_time= Column(DateTime, index=True)
    status = Column(String(20), index=True, nullable=False)

    user = relationship("User", back_populates="orders")
    product = relationship("Product")

    # new added line
    # snapshot_price = Column(Numeric(10, 2), nullable=True)
    # total_amount = Column(Numeric(10, 2), nullable=True)
    # status = Column(String(20), nullable=True)

    snapshot_price = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    paid_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)








"""id
user_id (ForeignKey)
product_id (ForeignKey)
quantity
amount
order_time
status
"""