# app/db/base.py
from sqlalchemy.orm import DeclarativeBase , declarative_base

Base = declarative_base()


from app.models.user import User
from app.models.product import Product
from app.models.order import Order

# class Base(DeclarativeBase):
#     pass
