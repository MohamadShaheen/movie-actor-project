import os
import logging
from routers import movies
from fastapi import FastAPI, Request, HTTPException

if not os.path.exists('logs'):
    os.mkdir('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='[%d-%m-%Y] (%H:%M:%S)',
    force=True
)

app = FastAPI()


@app.middleware("http")
async def log_request(request: Request, call_next):
    logging.info(f"Accessing {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        if response.status_code >= 400:
            logging.error(f"Error {response.status_code}: {request.method} {request.url.path}")
        else:
            logging.info(f"Success: {request.method} {request.url.path}")
        return response
    except Exception as err:
        logging.error(f"Error: {request.method} {request.url.path} - {str(err)}")
        raise err


@app.get("/")
async def root(request: Request):
    return "Welcome to Movie and Actor Server"


app.include_router(movies.router, prefix="/movies", tags=["movies"])
