import time
import logging
from fastapi import Request

logger = logging.getLogger("app")

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    client_ip = request.client.host
    logger.info(f"{client_ip} {request.method} {request.url}")
    logger.info(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"Completed {request.method} {request.url} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.4f}s"
    )

    return response