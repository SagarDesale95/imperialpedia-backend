from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.services import categories as category_svc
from app.utils.responses import err, ok

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("")
def get_categories(db: Session = Depends(get_db)):
    rows = category_svc.list_categories(db)
    out = [CategoryOut.model_validate(r).model_dump() for r in rows]
    return ok(out)


@router.post("")
def post_category(body: CategoryCreate, db: Session = Depends(get_db)):
    try:
        row = category_svc.create_category(db, body)
    except ValueError as e:
        return err(str(e), 400)
    return ok(CategoryOut.model_validate(row).model_dump())


@router.put("/{category_id}")
def put_category(category_id: int, body: CategoryUpdate, db: Session = Depends(get_db)):
    try:
        row = category_svc.update_category(db, category_id, body)
    except ValueError as e:
        return err(str(e), 400)
    if not row:
        return err("Category not found", 404)
    return ok(CategoryOut.model_validate(row).model_dump())


@router.delete("/{category_id}")
def delete_category_route(category_id: int, db: Session = Depends(get_db)):
    try:
        deleted = category_svc.delete_category(db, category_id)
    except ValueError as e:
        return err(str(e), 400)
    if not deleted:
        return err("Category not found", 404)
    return ok({"deleted": True, "id": category_id})
