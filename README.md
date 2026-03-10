
# Internal Data Operations Platform

## Motivation

This project was created to practice backend engineering patterns commonly used in production systems, including authentication, authorization, logging, and automated testing.


## How to run this project?

```
git clone https://github.com/InPurpose/Internal_Data_Operations_Platform.git
```

We provide **project.toml** and **requirement.txt** for this project. Thus, you can either use **uv** or pip to install the requirements:
```
uv sync
```
or 
```
pip install -r requirements.txt
```

Next, you need to manully create a new file called **.env** under root directory. And then, you need to copy all the varaibles from **.env.example** fill in the values for each of them. Or you can run this command:
```
mv -i ".env.example" ".env"
``` 

After that, you need to create the tables and indexes in database:
```
alembic upgarde head
```

If you have data, you can import your data into the database. Otherwise, you may want to use our script to generate some fake data for testing:
```
uv run uvicorn app.main:app --reload 
```
or 
```
uvicorn app.main:app --reload
```

## Project Overview

This project simulates a backend data operations platform built with FastAPI.
It focuses on authentication, authorization, logging, and backend engineering best practices.

### Project Structure
````
.
├── app
│   ├── api
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   └── metrics.py
│   ├── check_models.py
│   ├── core
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   ├── middleware.py
│   │   └── security.py
│   ├── database
│   │   ├── base.py
│   │   ├── query.sql
│   │   └── session.py
│   ├── main.py
│   ├── models
│   │   ├── order.py
│   │   ├── product.py
│   │   └── user.py
│   ├── pipelines
│   ├── services
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   ├── images
│   │   └── js
│   │       └── dashboard.js
│   └── templates
│       └── dashboard.html
├── logs
│   └── app.log
├── migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 098d3a44ab2b_make_order_fields_non_nullable.py
│       ├── 1e7dcf9f14ae_add_business_fields_to_orders.py
│       ├── 32d0070d02ed_add_auth_fields.py
│       ├── 445eab7d64b5_set_nullability_product_category_to_true.py
│       ├── 77e018c1ec29_add_orders_table.py
│       ├── b94c162989bc_add_index_to_orders_status.py
│       ├── c1d9742eb39c_add_users_table.py
│       ├── c41f6ef90208_add_products_table.py
│       ├── c5dcd55f3af1_add_index_on_orders_status_order_time.py
│       └── ef898edea7ce_make_order_fields_non_nullable_.py
├── pyproject.toml
├── README.md
├── scripts
│   ├── db
│   │   └── run_query.sh
│   └── generate_fake_data.py
├── test
│   ├── test_auth.py
│   ├── test_metrics.py
│   └── test_rbac.py
└── uv.lock
````

## Tech Stack

- FastAPI

- SQLAlchemy

- PostgreSQL

- Alembic

- JWT (python-jose)

- passlib (bcrypt)

- pytest

- uv (package management)

## Features Implemented
### 1. Authentication (JWT-based)

- User login endpoint

- Password hashing with bcrypt

- JWT token generation

- Token expiration support

- Protected endpoints via dependency injection

Result:

✔ Stateless authentication

✔ Secure password storage

✔ Token-based authorization

### 2. Role-Based Access Control (RBAC)

- Role field in user model

- Admin-only endpoint

- Permission check in dependency layer

Result:

✔ Basic role-based permission enforcement

### 3. Logging System

Layer 1: Middleware Logging

- Request method

- URL

- Client IP

- Response status

- Execution time

Layer 2: Business Logging

- Login attempts

- Login failures

- Successful authentication

Logging Strategy:

- RotatingFileHandler (10MB rollover)

- Console + File output

Result:

✔ Request-level observability

✔ Security event tracking

✔ Production-style logging structure

### 4. Automated Testing

Using pytest + TestClient

Tests include:

- Login success

- Protected route access

- Unauthorized access

- RBAC enforcement

Result:

✔ Authentication correctness verified

✔ Authorization logic validated

✔ Reduced regression risk

## Current System Architecture

#### Request Flow:

Client

↓

FastAPI Router

↓

Dependency Injection (JWT Auth)

↓

Service Layer

↓

Database Layer

↓

Response

#### Logging:

Middleware → Request-level

Business Layer → Auth events

#### Authentication:

JWT verification happens in dependency layer, not middleware.

## Caching Layer

To reduce database load, Redis caching is used for analytics endpoints.

Example:
- /metrics/gmv
- /metrics/trend

Cache strategy:
- Key: gmv:{days}
- TTL: 60 seconds

Workflow:
1. Check Redis cache
2. If hit → return cached result
3. If miss → query PostgreSQL
4. Store result in Redis

## Key Engineering Decisions
JWT authentication is implemented using dependency injection rather than middleware to allow fine-grained control over which endpoints require authentication.

Logging is separated into two layers:
- Middleware logging for request lifecycle
- Business logging for security events such as login attempts.

Logging Layer

Middleware → access logs

Service → business logs

Testing is implemented with pytest and FastAPI TestClient to verify authentication and authorization flows.
## Current Status

- Core authentication system complete

- Basic RBAC implemented

- Logging integrated

- Tests passing

The system now represents a production-style backend foundation.