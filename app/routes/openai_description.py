from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.utils.openai_client import generate_description_text

router = APIRouter()

class GenerateRequest(BaseModel):
    name: str
    user_hint: Optional[str] = None

@router.post("")
def generate_description(req: GenerateRequest):
    try:
        description = generate_description_text(req.name, req.user_hint)
        return {"description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
