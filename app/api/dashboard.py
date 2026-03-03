from fastapi import FastAPI, APIRouter, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.metrics import checkGMVbyDate

from fastapi import Depends
from app.core.security import get_current_user


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
@router.get("/dashboard")#, response_class=HTMLResponse)
def dashboard(request:Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@router.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user.email}"
    }