from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GlossaryCreate(BaseModel):
    term: str = Field(..., min_length=1)
    definition: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1)
    related_terms: Optional[list[str]] = None


class GlossaryUpdate(BaseModel):
    term: Optional[str] = Field(None, min_length=1)
    definition: Optional[str] = Field(None, min_length=1)
    slug: Optional[str] = Field(None, min_length=1)
    related_terms: Optional[list[str]] = None


class GlossaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    term: str
    definition: str
    slug: str
    related_terms: Optional[list[str]]
    created_at: datetime
