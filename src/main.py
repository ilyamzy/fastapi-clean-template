import os
import json
import logging
import firebase_admin

from contextlib import asynccontextmanager
from fastapi import FastAPI
from firebase_admin import credentials

from presentation.api import (
    auth_router,
    image_router
)
from infrastructure.config import settings
from presentation.dependencies import engine


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", mode='a')
    ]
)

logger = logging.getLogger()
logger.info("Logging is configured")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not firebase_admin._apps:
        firebase_json_str = os.getenv('FIREBASE')
        firebase_config = json.loads(firebase_json_str)
        firebase_config["private_key"] = firebase_config["private_key"].replace("\\n", "\n")
    
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
    yield
    
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# app.include_router(auth_router)
app.include(image_router)
