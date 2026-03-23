from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.glossary import Glossary
from app.schemas.glossary import GlossaryCreate, GlossaryUpdate


def list_glossary(db: Session) -> list[Glossary]:
    return list(db.scalars(select(Glossary).order_by(Glossary.term.asc())).all())


def get_glossary_entry(db: Session, entry_id: int) -> Glossary | None:
    return db.get(Glossary, entry_id)


def get_by_slug(db: Session, slug: str) -> Glossary | None:
    return db.scalar(select(Glossary).where(Glossary.slug == slug))


def create_glossary(db: Session, data: GlossaryCreate) -> Glossary:
    if get_by_slug(db, data.slug.strip()):
        raise ValueError("Slug already exists")
    row = Glossary(
        term=data.term.strip(),
        definition=data.definition.strip(),
        slug=data.slug.strip(),
        related_terms=data.related_terms,
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Slug already exists") from None
    db.refresh(row)
    return row


def update_glossary(db: Session, entry_id: int, data: GlossaryUpdate) -> Glossary | None:
    row = get_glossary_entry(db, entry_id)
    if not row:
        return None
    payload = data.model_dump(exclude_unset=True)
    if "slug" in payload and payload["slug"] is not None:
        other = get_by_slug(db, payload["slug"].strip())
        if other and other.id != entry_id:
            raise ValueError("Slug already exists")
        row.slug = payload["slug"].strip()
    if "term" in payload and payload["term"] is not None:
        row.term = payload["term"].strip()
    if "definition" in payload and payload["definition"] is not None:
        row.definition = payload["definition"].strip()
    if "related_terms" in payload:
        row.related_terms = payload["related_terms"]
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Slug already exists") from None
    db.refresh(row)
    return row


def delete_glossary(db: Session, entry_id: int) -> bool:
    row = get_glossary_entry(db, entry_id)
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True
