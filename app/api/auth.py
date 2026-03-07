from fastapi import APIRouter, HTTPException
from sqlalchemy import func

from app.db.session import SessionLocal
from app.models import *
from app.core.security import verify_password, create_access_token, require_role

from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
# def login(email: str, password: str):
    logger.info(f"Login attempt: {form_data.username}")
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == form_data.username).first()

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not user:
            logger.warning(f"Login failed - user not found: {form_data.username}")

        if not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Login failed - wrong password: {form_data.username}")

        logger.info(f"Login success: {form_data.username}")

        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}

    finally:
        session.close()



@router.get("/admin-only")
def admin_route(current_user = Depends(require_role("admin"))):
    return {"message": "Welcome admin"}