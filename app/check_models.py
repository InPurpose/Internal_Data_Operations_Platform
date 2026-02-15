from app.db.base import Base
import app.models  # 触发所有 model import

print(Base.metadata.tables.keys())
