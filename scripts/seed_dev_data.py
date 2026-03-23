#!/usr/bin/env python3
"""Insert sample rows for Swagger / manual API tests. Run after: alembic upgrade head"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from sqlalchemy import select

from app.database import SessionLocal
from app.models.article import Article, ArticleStatus
from app.models.category import Category
from app.models.glossary import Glossary
from app.models.seo import SEO
from app.models.tag import Tag


def _get_or_create_category(db) -> Category:
    row = db.scalar(select(Category).where(Category.slug == "sample-investing"))
    if row:
        return row
    row = Category(name="Sample Investing", slug="sample-investing")
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def _get_or_create_tag(db) -> None:
    if db.scalar(select(Tag).where(Tag.slug == "sample-markets")):
        return
    db.add(Tag(name="Sample Markets", slug="sample-markets"))
    db.commit()


def _get_or_create_article(db, category_id: int) -> None:
    if db.scalar(select(Article).where(Article.slug == "sample-welcome-article")):
        return
    db.add(
        Article(
            title="Sample welcome article",
            slug="sample-welcome-article",
            content="<p>Hello from Imperialpedia API seed.</p>",
            category_id=category_id,
            tags=["sample-markets", "demo"],
            status=ArticleStatus.published,
            seo_title="Welcome | Imperialpedia",
            seo_description="Seeded article for API tests",
            featured_image=None,
            author_id=1,
        )
    )
    db.commit()


def _get_or_create_glossary(db) -> None:
    if db.scalar(select(Glossary).where(Glossary.slug == "sample-dividend")):
        return
    db.add(
        Glossary(
            term="Sample dividend",
            definition="A seeded glossary term for testing the glossary API.",
            slug="sample-dividend",
            related_terms=["yield", "payout"],
        )
    )
    db.commit()


def _get_or_create_seo(db) -> None:
    url = "https://imperialpedia.com/sample-page"
    if db.scalar(select(SEO).where(SEO.page_url == url)):
        return
    db.add(
        SEO(
            page_url=url,
            indexed=True,
            last_crawled=None,
            issues=None,
        )
    )
    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        cat = _get_or_create_category(db)
        _get_or_create_tag(db)
        _get_or_create_article(db, cat.id)
        _get_or_create_glossary(db)
        _get_or_create_seo(db)
        print("Seed complete (idempotent). Use GET /api/articles, /api/categories, etc.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
