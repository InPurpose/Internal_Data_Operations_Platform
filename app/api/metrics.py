from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import func

from app.db.session import SessionLocal
from app.models import *

from app.core.security import get_current_user
from app.core.redis import redis_client

from datetime import datetime, timedelta
import time
import json



cache_store = {}
CACHE_TTL = 60 # seconds

router = APIRouter()
@router.get("/metrics/gmv")
def get_gmv(days: int = 7,status: str = "paid",current_user: str = Depends(get_current_user)):

    # cache_key = f"gmv:{days}:{status}"

    cache_key = f"gmv:{days}"
    cached = redis_client.get(cache_key)

    # now = time.time()
    session = SessionLocal()

    if cached:
        print(f"cache hits")
        return json.loads(cached)
    
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
    redis_client.set(cache_key, json.dumps(response), ex=CACHE_TTL)

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

        query = query.offset(offset=offset).limit(limit)

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
    # print("====================")
    # print(res)
    return {
        "dates":dates,
        "values":values
    }



@router.get("/orders")
def getOrder(user_id:str,start_date:datetime,end_date:datetime,status:str = 'paid',page:int = 1,page_size:int = 20):
    session = SessionLocal()
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id required")
        
        query = session.query(
            Order.id,
            func.date(Order.order_time).label("date"),
            Order.status,
            Order.snapshot_price,
            Order.total_amount,
            Product.name.label("product_name")
        ).join(Product,Product.id == Order.product_id)
        query = query.filter(Order.user_id == user_id)

        VALID_STATUS = {"paid", "pending", "cancelled"}

        if status in VALID_STATUS:
            query = query.filter(Order.status == status)

        if start_date:
            query = query.filter(Order.order_time > start_date)
        
        if end_date:
            query = query.filter(Order.order_time < end_date)

        query = query.offset((page-1)*page_size).limit(page_size)
        result = query.all()
        total_order = session.query(
            func.count(Order.id)
        ).filter(Order.user_id==user_id).one()[0]

        # print(f"total_order: {(total_order)} ================")
        
        
        
    finally:
        session.close()

    return {
        "User_id": user_id,
        "page": {page},
        "page_size": {page_size},
        "total_order": {total_order},
        "total_page": {total_order//page_size + 1},
        "Orders":[
            {
                "id":{rows.id},
                "date": {rows.date},
                "product":{rows.product_name},
                "status":{rows.status},
                "price":{rows.snapshot_price}, 
            }
            for rows in result]
    } 

if __name__ == "__main__":
    checkGMVbyDate(30)
