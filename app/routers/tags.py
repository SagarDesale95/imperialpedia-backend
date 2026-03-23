from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.tag import TagCreate, TagOut
from app.services import tags as tag_svc
from app.utils.responses import err, ok

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("")
def get_tags(db: Session = Depends(get_db)):
    rows = tag_svc.list_tags(db)
    return ok([TagOut.model_validate(r).model_dump() for r in rows])


@router.post("")
def post_tag(body: TagCreate, db: Session = Depends(get_db)):
    try:
        row = tag_svc.create_tag(db, body)
    except ValueError as e:
        return err(str(e), 400)
    return ok(TagOut.model_validate(row).model_dump())
