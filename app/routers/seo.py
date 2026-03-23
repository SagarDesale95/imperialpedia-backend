from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.seo import SEOOut
from app.services import seo as seo_svc
from app.utils.responses import ok

router = APIRouter(prefix="/api/seo", tags=["seo"])


@router.get("/index-status")
def get_index_status(db: Session = Depends(get_db)):
    rows = seo_svc.list_seo_records(db)
    return ok([SEOOut.model_validate(r).model_dump() for r in rows])


@router.get("/sitemap")
def get_sitemap(db: Session = Depends(get_db)):
    urls = seo_svc.list_page_urls(db)
    return ok(urls)
