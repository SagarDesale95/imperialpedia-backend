from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def list_categories(db: Session) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.id.asc())).all())


def get_category(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def get_category_by_slug(db: Session, slug: str) -> Category | None:
    return db.scalar(select(Category).where(Category.slug == slug))


def create_category(db: Session, data: CategoryCreate) -> Category:
    if get_category_by_slug(db, data.slug.strip()):
        raise ValueError("Slug already exists")
    row = Category(
        name=data.name.strip(),
        slug=data.slug.strip(),
        parent_id=data.parent_id,
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Slug already exists or invalid parent_id") from None
    db.refresh(row)
    return row


def update_category(db: Session, category_id: int, data: CategoryUpdate) -> Category | None:
    row = get_category(db, category_id)
    if not row:
        return None
    payload = data.model_dump(exclude_unset=True)
    if "slug" in payload and payload["slug"] is not None:
        other = get_category_by_slug(db, payload["slug"].strip())
        if other and other.id != category_id:
            raise ValueError("Slug already exists")
        row.slug = payload["slug"].strip()
    if "name" in payload and payload["name"] is not None:
        row.name = payload["name"].strip()
    if "parent_id" in payload:
        if payload["parent_id"] == category_id:
            raise ValueError("Category cannot be its own parent")
        row.parent_id = payload["parent_id"]
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Slug already exists or invalid parent_id") from None
    db.refresh(row)
    return row


def delete_category(db: Session, category_id: int) -> bool:
    row = get_category(db, category_id)
    if not row:
        return False
    db.delete(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Cannot delete category: referenced by articles or child categories") from None
    return True
