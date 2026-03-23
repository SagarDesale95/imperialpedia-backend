from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.article import ArticleCreate, ArticleOut, ArticleUpdate
from app.services import articles as article_svc
from app.utils.responses import err, ok

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("")
def get_articles(db: Session = Depends(get_db)):
    rows = article_svc.list_articles(db)
    return ok([ArticleOut.model_validate(r).model_dump() for r in rows])


@router.get("/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    row = article_svc.get_article(db, article_id)
    if not row:
        return err("Article not found", 404)
    return ok(ArticleOut.model_validate(row).model_dump())


@router.post("")
def post_article(body: ArticleCreate, db: Session = Depends(get_db)):
    try:
        row = article_svc.create_article(db, body)
    except ValueError as e:
        return err(str(e), 400)
    return ok(ArticleOut.model_validate(row).model_dump())


@router.put("/{article_id}")
def put_article(article_id: int, body: ArticleUpdate, db: Session = Depends(get_db)):
    try:
        row = article_svc.update_article(db, article_id, body)
    except ValueError as e:
        return err(str(e), 400)
    if not row:
        return err("Article not found", 404)
    return ok(ArticleOut.model_validate(row).model_dump())


@router.delete("/{article_id}")
def delete_article_route(article_id: int, db: Session = Depends(get_db)):
    deleted = article_svc.delete_article(db, article_id)
    if not deleted:
        return err("Article not found", 404)
    return ok({"deleted": True, "id": article_id})
