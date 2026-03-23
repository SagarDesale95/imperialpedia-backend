import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")

log = logging.getLogger(__name__)

_PLACEHOLDER_HOST = "ep-xxxxx.region.aws.neon.tech"


def _resolve_database_url() -> str:
    raw = os.getenv("DATABASE_URL", "").strip()
    if not raw or _PLACEHOLDER_HOST in raw:
        if raw and _PLACEHOLDER_HOST in raw:
            log.warning(
                "DATABASE_URL still uses the example Neon host (%s). "
                "Using local SQLite instead: set a real Neon URI when you want cloud Postgres.",
                _PLACEHOLDER_HOST,
            )
        p = (_ROOT / "local_dev.db").resolve()
        return "sqlite:///" + str(p)
    return raw


DATABASE_URL = _resolve_database_url()

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    connect_args: dict = {}
    if DATABASE_URL.startswith("postgresql") and "sslmode=" not in DATABASE_URL:
        connect_args["sslmode"] = "require"
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
