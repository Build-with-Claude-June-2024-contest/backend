import logging
import uuid

import firebase_admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_profiler import PyInstrumentProfilerMiddleware
from firebase_admin import credentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.config.logging_config import logger
from app.config.settings import settings
from app.controllers.talent_query_controller import talent_query_router
from app.infrastructure.apis import router as common_router
from app.user.apis import router as user_router

logging.getLogger().setLevel(logging.INFO)

app = FastAPI(title="AI Service", docs_url="/")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


app.add_middleware(RequestIDMiddleware)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# profiler
if settings.PROFILING_ENABLED:
    app.add_middleware(
        middleware_class=PyInstrumentProfilerMiddleware,
    )

app.include_router(common_router, prefix="/internal/common", tags=["common"])
app.include_router(user_router, prefix="/user", tags=["user"])

app.include_router(
    router=talent_query_router, prefix="/talent-query", tags=["talent-query"]
)


if settings.AUTH_METHOD == "firebase":
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred)


@app.on_event("startup")
async def startup_event():
    logger.critical("Application start")


@app.on_event("shutdown")
def shutdown_event():
    # scheduler.shutdown()
    logger.critical("Application shutdown")
