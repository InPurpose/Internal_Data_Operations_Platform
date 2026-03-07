import time
import logging
import uuid

from fastapi import Request

logger = logging.getLogger(__name__)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):

    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id

    start_time = time.time()
    
    # client_ip = request.client.host
    # logger.info(
    #     f"{client_ip} {request.method} {request.url}"
    #     )
    # logger.info(f"Incoming request: {request.method} {request.url}")
    
    logger.info(
        f"[req-{request_id}] {request.client.host} "
        f"{request.method} {request.url.path} started"
    )
    
    # logger.info(
    #     f"{request.client.host} "
    #     f"{request.method} {request.url.path} "
    #     f"Status:{response.status_code} "
    #     f"Time:{process_time:.4f}s"
    # )

    response = await call_next(request)

    process_time = time.time() - start_time

    # logger.info(
    #     f"Completed {request.method} {request.url} "
    #     f"Status: {response.status_code} "
    #     f"Time: {process_time:.4f}s"
    # )

    logger.info(
        f"[req-{request_id}] {request.client.host} "
        f"{request.method} {request.url.path} "
        f"Status:{response.status_code} "
        f"Time:{process_time:.4f}s"
    )

    return response