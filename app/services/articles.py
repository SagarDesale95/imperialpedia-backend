from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.article import Article, ArticleStatus
from app.schemas.article import ArticleCreate, ArticleUpdate


def list_articles(db: Session) -> list[Article]:
    return list(db.scalars(select(Article).order_by(Article.id.desc())).all())


def get_article(db: Session, article_id: int) -> Article | None:
    return db.get(Article, article_id)


def get_article_by_slug(db: Session, slug: str) -> Article | None:
    return db.scalar(select(Article).where(Article.slug == slug))


def create_article(db: Session, data: ArticleCreate) -> Article:
    if get_article_by_slug(db, data.slug):
        raise ValueError("Slug already exists")
    article = Article(
        title=data.title.strip(),
        slug=data.slug.strip(),
        content=data.content,
        category_id=data.category_id,
        tags=data.tags,
        status=ArticleStatus(data.status.value),
        seo_title=data.seo_title,
        seo_description=data.seo_description,
        featured_image=data.featured_image,
        author_id=data.author_id,
    )
    db.add(article)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Slug already exists or invalid reference") from None
    db.refresh(article)
    return article


def update_article(db: Session, article_id: int, data: ArticleUpdate) -> Article | None:
    article = get_article(db, article_id)
    if not article:
        return None
    payload = data.model_dump(exclude_unset=True)
    if "slug" in payload and payload["slug"] is not None:
        other = get_article_by_slug(db, payload["slug"].strip())
        if other and other.id != article_id:
            raise ValueError("Slug already exists")
        article.slug = payload["slug"].strip()
    if "title" in payload and payload["title"] is not None:
        article.title = payload["title"].strip()
    if "content" in payload:
        article.content = payload["content"]
    if "category_id" in payload:
        article.category_id = payload["category_id"]
    if "tags" in payload:
        article.tags = payload["tags"]
    if "status" in payload and payload["status"] is not None:
        article.status = ArticleStatus(payload["status"].value)
    if "seo_title" in payload:
        article.seo_title = payload["seo_title"]
    if "seo_description" in payload:
        article.seo_description = payload["seo_description"]
    if "featured_image" in payload:
        article.featured_image = payload["featured_image"]
    if "author_id" in payload:
        article.author_id = payload["author_id"]
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Slug already exists or invalid reference") from None
    db.refresh(article)
    return article


def delete_article(db: Session, article_id: int) -> bool:
    article = get_article(db, article_id)
    if not article:
        return False
    db.delete(article)
    db.commit()
    return True
