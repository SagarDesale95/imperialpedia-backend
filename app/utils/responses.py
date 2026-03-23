from typing import Any

from fastapi.responses import JSONResponse


def ok(data: Any) -> dict:
    return {"success": True, "data": data}


def err(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message},
    )
