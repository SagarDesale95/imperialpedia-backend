from __future__ import annotations

from fastapi import APIRouter

from app.schemas.ai import AIGenerateIn
from app.services import ai as ai_svc
from app.utils.responses import err, ok

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/generate")
def post_generate(body: AIGenerateIn):
    try:
        text = ai_svc.generate_text(body.prompt.strip())
    except ValueError as e:
        return err(str(e), 400)
    except Exception:
        return err("OpenAI request failed", 502)
    return ok(text)
