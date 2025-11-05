import logging

from fastapi import FastAPI

from app.api.v1 import api_user, api_account, api_mall
from app.core.config import config
from app.core.logging_core import setup_logging
from app.db.schema import Base, engine


setup_logging()  # Set up root logging before emitting any log
logging.info("Logging initialized")

# Create DB tables when starting app
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)


# Register routes
app.include_router(api_user.router, prefix="/api/v1")
app.include_router(api_account.router, prefix="/api/v1")
app.include_router(api_mall.router, prefix="/api/v1")
