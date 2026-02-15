from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    country = Column(String, index=True)
    device_type = Column(String)
    register_time = Column(DateTime, index=True)

    orders = relationship("Order", back_populates="user")


# Indexed: id, email, country, register_time

 