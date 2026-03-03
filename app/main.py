from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api import metrics, dashboard, auth

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.logging_config import setup_logging

import logging
from app.core.middleware import logging_middleware

setup_logging()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

app.middleware("http")(logging_middleware)

app.include_router(metrics.router)
app.include_router(dashboard.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# templates = Jinja2Templates(directory="app/templates")

def main():
    print("Hello from internal-data-operations-platform!")


if __name__ == "__main__":
    main()
