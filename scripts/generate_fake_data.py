# scripts/generate_fake_data.py

import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

from app.db.session import SessionLocal
from app.models import User, Product, Order
from app.core.security import hash_password
import os


def clear_data(session):
    session.query(Order).delete()
    session.query(User).delete()
    session.query(Product).delete()

def generate_users(session, n=100):
    users = []
    common_hash = hash_password("password")

    for i in range(n):
        users.append(
            User(
                email=f"user{i}@example.com",
                register_time=datetime.now(),
                hashed_password=common_hash
            )
        )
    session.add_all(users)


def generate_products(session, n=50):
    products = []
    for i in range(n):
        price = round(random.uniform(10, 500), 2)
        products.append(
            Product(
                name = f"product_{i}",
                category= '',
                price=price,
                created_at=datetime.now(),
            )
        )
    session.add_all(products)


def generate_orders(session, n=1000):
    users = session.query(User).all()
    products = session.query(Product).all()

    orders = []
    
    for i in range(n):
        user = random.choice(users)
        product = random.choice(products)

        quantity = random.randint(1, 5)

        status = random.choices(
            ["paid", "pending", "cancelled"],
            weights=[0.7, 0.2, 0.1],
        )[0]

        total_amount = product.price * quantity

        orders.append(
            Order(
                user_id=user.id,
                product_id=product.id,
                quantity=quantity,
                snapshot_price=product.price,
                total_amount=total_amount,
                status=status,
                order_time=datetime.now() - timedelta(days=random.randint(0, 30)),
            )
        )

    session.add_all(orders)


def main():
    
    if not os.getenv("DATABASE_URL"):
        raise ValueError("DATABASE_URL is required but not provided")
    
    session = SessionLocal()
    clear_data(session)

    generate_users(session,10000)
    generate_products(session,5000)

    session.flush() 

    generate_orders(session,100000)

    session.commit()
    session.close()

# 100k



if __name__ == "__main__":
    main()