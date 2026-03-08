import logging
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import config  # Import config before the other custom code
from app.api.v1 import api_user, api_account, api_mall
from app.core.logging_core import setup_logging
from app.db.schema import Base, engine


setup_logging()  # Set up root logging before emitting any log
logging.info(f"Logging initialized for {config.app_name}")

# Create DB tables when starting app
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)
app.mount("/static", StaticFiles(directory=Path("./app/resources/static")), name="static")
templates = Jinja2Templates(directory=Path("./app/resources/templates"))

# Register routes
app.include_router(api_user.router, prefix="/api/v1")
app.include_router(api_account.router, prefix="/api/v1")
app.include_router(api_mall.router, prefix="/api/v1")

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


# Possibility to run uvicorn directly with main.py
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, log_level="trace")
