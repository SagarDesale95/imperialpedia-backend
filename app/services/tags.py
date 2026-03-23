from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.schemas.tag import TagCreate


def list_tags(db: Session) -> list[Tag]:
    return list(db.scalars(select(Tag).order_by(Tag.name.asc())).all())


def get_tag_by_slug(db: Session, slug: str) -> Tag | None:
    return db.scalar(select(Tag).where(Tag.slug == slug))


def create_tag(db: Session, data: TagCreate) -> Tag:
    if get_tag_by_slug(db, data.slug.strip()):
        raise ValueError("Slug already exists")
    row = Tag(name=data.name.strip(), slug=data.slug.strip())
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Slug already exists") from None
    db.refresh(row)
    return row
