from app.db.session import engine
from app.db.base import Base

from app.models.user import User

from app.models.product import Product
from app.models.order import Order


# Do run this line anymore, use <alembic> instead
# Base.metadata.create_all(bind=engine)
