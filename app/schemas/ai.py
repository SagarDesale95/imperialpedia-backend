from pydantic import BaseModel, Field


class AIGenerateIn(BaseModel):
    prompt: str = Field(..., min_length=1)


class AIGenerateOut(BaseModel):
    success: bool = True
    data: str
