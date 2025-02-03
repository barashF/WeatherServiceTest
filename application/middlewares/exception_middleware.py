from configuration.logger import setup_logger

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from logging import Logger


class ExceptionMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
        self.logger = setup_logger()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        try:
            await self.app(scope, receive, send)
        except StarletteHTTPException as exc:
            self.logger.error(f"HTTPException: {exc.detail}")
            response = JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail, "type": "HTTPException"},
            )
            await response(scope, receive, send)
        except Exception as exc:
            self.logger.exception("Unhandled Exception occurred")
            response = JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal Server Error",
                    "type": "InternalServerError",
                    "message": str(exc),
                },
            )
            await response(scope, receive, send)