from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ArticleStatusSchema(str, Enum):
    draft = "draft"
    review = "review"
    published = "published"


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1)
    content: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[list[str]] = None
    status: ArticleStatusSchema = ArticleStatusSchema.draft
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    featured_image: Optional[str] = None
    author_id: Optional[int] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    slug: Optional[str] = Field(None, min_length=1)
    content: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[list[str]] = None
    status: Optional[ArticleStatusSchema] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    featured_image: Optional[str] = None
    author_id: Optional[int] = None


class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    content: Optional[str]
    category_id: Optional[int]
    tags: Optional[list[str]]
    status: str
    seo_title: Optional[str]
    seo_description: Optional[str]
    featured_image: Optional[str]
    author_id: Optional[int]
    created_at: datetime
    updated_at: datetime
