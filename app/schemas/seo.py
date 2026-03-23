from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SEOOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    page_url: str
    indexed: bool
    last_crawled: Optional[datetime]
    issues: Optional[str]
