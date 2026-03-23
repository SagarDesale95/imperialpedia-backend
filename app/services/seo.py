from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.seo import SEO


def list_seo_records(db: Session) -> list[SEO]:
    return list(db.scalars(select(SEO).order_by(SEO.id.asc())).all())


def list_page_urls(db: Session) -> list[str]:
    rows = db.scalars(select(SEO.page_url).order_by(SEO.id.asc())).all()
    return [r for r in rows]
