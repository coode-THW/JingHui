import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings
from .database import Base, SessionLocal, engine
from .errors import ApiError, ok
from .routers import admin, ai, auth, catalog, messages, orders
from .seed import seed_database

logger = logging.getLogger("jinghui")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.static_dir.mkdir(parents=True, exist_ok=True)
    (settings.static_dir / "generated").mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_database(db)
    if settings.app_env == "production" and settings.secret_key.startswith("jinghui-local"):
        logger.warning("生产环境必须修改 SECRET_KEY")
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI 形象生成与画师手作定制平台 API",
    lifespan=lifespan,
)

origins = settings.cors_origin_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials="*" not in origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(catalog.router)
app.include_router(orders.router)
app.include_router(messages.router)
app.include_router(admin.router)
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "data": jsonable_encoder(exc.data)},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(part) for part in error["loc"]), "message": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"code": 42200, "message": "请求参数校验失败", "data": {"errors": errors}},
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code * 100, "message": str(exc.detail), "data": None},
        headers=exc.headers,
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.exception("未处理异常：%s %s", request.method, request.url.path)
    message = f"服务器内部错误：{exc}" if settings.debug else "服务器内部错误"
    return JSONResponse(status_code=500, content={"code": 50000, "message": message, "data": None})


@app.get("/api/health", tags=["系统"])
def health():
    database_status = "ok"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        database_status = "unavailable"
    return ok({
        "status": "ok" if database_status == "ok" else "degraded",
        "service": settings.app_name,
        "version": "1.0.0",
        "database": database_status,
        "ai_provider": settings.ai_provider.lower(),
        "demo_mode": settings.ai_provider.lower() == "demo",
        "time": datetime.now(timezone.utc).isoformat(),
    })
