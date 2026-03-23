from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.glossary import GlossaryCreate, GlossaryOut, GlossaryUpdate
from app.services import glossary as glossary_svc
from app.utils.responses import err, ok

router = APIRouter(prefix="/api/glossary", tags=["glossary"])


@router.get("")
def get_glossary(db: Session = Depends(get_db)):
    rows = glossary_svc.list_glossary(db)
    return ok([GlossaryOut.model_validate(r).model_dump() for r in rows])


@router.post("")
def post_glossary(body: GlossaryCreate, db: Session = Depends(get_db)):
    try:
        row = glossary_svc.create_glossary(db, body)
    except ValueError as e:
        return err(str(e), 400)
    return ok(GlossaryOut.model_validate(row).model_dump())


@router.put("/{entry_id}")
def put_glossary(entry_id: int, body: GlossaryUpdate, db: Session = Depends(get_db)):
    try:
        row = glossary_svc.update_glossary(db, entry_id, body)
    except ValueError as e:
        return err(str(e), 400)
    if not row:
        return err("Glossary entry not found", 404)
    return ok(GlossaryOut.model_validate(row).model_dump())


@router.delete("/{entry_id}")
def delete_glossary_route(entry_id: int, db: Session = Depends(get_db)):
    deleted = glossary_svc.delete_glossary(db, entry_id)
    if not deleted:
        return err("Glossary entry not found", 404)
    return ok({"deleted": True, "id": entry_id})
