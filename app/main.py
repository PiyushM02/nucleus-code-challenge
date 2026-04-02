import logging
import sys
import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("app")

app = FastAPI(title="HTTPS demo")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    log.info("%s %s -> %s (%.1fms)", request.method, request.url.path, response.status_code, ms)
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return HTMLResponse(
        "<h1>HTTPS demo</h1><p>TLS is terminated in the app container (Uvicorn).</p>"
        "<p><a href='/health'>/health</a></p>"
    )
