import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError

from app.routers import ai, articles, categories, glossary, seo, tags

app = FastAPI(title="Imperialpedia Backend", version="1.0.0", redirect_slashes=False)

# Default CORS origins for official domains.
# Override via CORS_ORIGINS env var (comma-separated) for flexibility.
_origins = os.getenv(
    "CORS_ORIGINS",
    "https://ir.baalvion.com,https://imperialpedia.com",
).strip()
_cors_list = [o.strip() for o in _origins.split(",") if o.strip()] or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)
app.include_router(categories.router)
app.include_router(tags.router)
app.include_router(glossary.router)
app.include_router(seo.router)
app.include_router(ai.router)


@app.exception_handler(RequestValidationError)
async def validation_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(IntegrityError)
async def integrity_handler(_, exc: IntegrityError):
    raw = getattr(exc, "orig", None)
    detail = str(raw) if raw is not None else str(exc)
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "Constraint violation (duplicate slug, invalid foreign key, etc.).",
            "detail": detail,
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_handler(_, exc: SQLAlchemyError):
    hint = "From project root run: alembic upgrade head (and verify DATABASE_URL in .env)."
    raw = getattr(exc, "orig", None)
    detail = str(raw) if raw is not None else str(exc)
    status = 503 if isinstance(exc, DBAPIError) else 500
    return JSONResponse(
        status_code=status,
        content={
            "success": False,
            "message": "Database error. Check DATABASE_URL, run alembic upgrade head, or use local SQLite (placeholder Neon URL auto-switches to local_dev.db).",
            "detail": detail,
            "hint": hint,
        },
    )