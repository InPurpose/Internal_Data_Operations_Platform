from fastapi import FastAPI, APIRouter

from sqlalchemy import func

from app.db.session import SessionLocal
from app.core.security import get_current_user
from app.models import *

from datetime import datetime, timedelta
import time


from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401)
#         return email
#     except JWTError:
#         raise HTTPException(status_code=401)

cache_store = {}
CACHE_TTL = 30 # seconds

router = APIRouter()
@router.get("/metrics/gmv")
def get_gmv(days: int = 7,status: str = "paid",current_user: str = Depends(get_current_user)):

    session = SessionLocal()
    cache_key = f"gmv:{days}:{status}"
    now = time.time()

    if cache_key in cache_store:
        data, expire_time = cache_store[cache_key]
        if now < expire_time:
            print("🔥 cache hit")
            return data
    try:
        query = session.query(
            func.count(Order.id),
            func.sum(Order.total_amount)
        ).filter(
            Order.order_time >= datetime.now() - timedelta(days=days),
            # Order.status == status
        )
        if status != "all":
            query = query.filter(Order.status == status)

        
        result = query.one()
        # print("===================")
        # print(result)
        
    finally:
        session.close()
    paid_count, paid_gmv = result
    response =  {
        "days": days,
        "paid_order_count": paid_count,
        "paid_gmv": float(paid_gmv or 0)
    }

    cache_store[cache_key] = (response, now + CACHE_TTL)

    return response


@router.get(path="/metrics/top-users")
def get_top_users(
    days: int = 7,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "gmv",
    order: str = "desc",
    min_gmv: float = 0):

    session = SessionLocal()

    try:
        gmv_expr = func.sum(Order.total_amount).label("gmv")

        query = session.query(
            Order.user_id,
            gmv_expr
        ).filter(Order.order_time >= datetime.now() - timedelta(days=days),Order.status == 'paid'
        ).group_by(Order.user_id)
        

        query = query.having(gmv_expr > min_gmv)

        if sort_by == "gmv":
            expr = gmv_expr
        elif sort_by == "user_id":
            expr = Order.user_id
        else:
            raise ValueError("Invalid sort field")

        if order == "desc":
            query = query.order_by(expr.desc())
        elif order != "desc":
            query = query.order_by(expr)
        else:
            raise ValueError("Invalid order")

        query = query.offset(offset).limit(limit)

        result = query.all()
    finally:
        session.close()
    # print(result)
    res = [{"user_id":item.user_id,"gmv":item.gmv} for item in result]
    return {
                "days": days,
                "users": [
                    {"user_id":item.user_id,"gmv":float(item.gmv)} 
                    for item in result
                ]
            }

@router.get("/metrics/trend")
def checkGMVbyDate(days:int =7):
    
    session = SessionLocal()

    try:
        query = session.query(
            func.date(Order.order_time).label("date"),
            func.sum(Order.total_amount).label("gmv")
        ).filter(
        Order.order_time >= datetime.now() - timedelta(days=days),
        Order.status == "paid"
        ).group_by(
            func.date(Order.order_time)
        ).order_by(func.date(Order.order_time)
        )#.limit(20)
        
        result = query.all()
    finally:
        session.close()

    dates, values = [], []

    for row in result:
        dates.append(row.date.strftime('%Y-%m-%d'))
        values.append(float(row.gmv))
    # res = [{f"{row.date.strftime('%Y-%m-%d')}":float(row.gmv)} for row in result]
    print("====================")
    # print(res)
    return {
        "dates":dates,
        "values":values
    }



if __name__ == "__main__":
    checkGMVbyDate(30)
