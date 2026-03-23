from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SEO(Base):
    __tablename__ = "seo_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    page_url: Mapped[str] = mapped_column(String(2048), unique=True, nullable=False, index=True)
    indexed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_crawled: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    issues: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
