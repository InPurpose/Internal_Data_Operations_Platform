
# Internal Data Operations Platform
## Project Overview

This project simulates a backend data operations platform built with FastAPI.
It focuses on authentication, authorization, logging, and backend engineering best practices.

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

Request Flow:

Client
↓
Router
↓
Dependency Injection (JWT Validation)
↓
Business Logic
↓
Database
↓
Response

Logging:

Middleware → Request-level
Business Layer → Auth events

Authentication:

JWT verification happens in dependency layer, not middleware.

## Current Status

- Core authentication system complete

- Basic RBAC implemented

- Logging integrated

- Tests passing

The system now represents a production-style backend foundation.