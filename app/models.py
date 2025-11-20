from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    price: int
    description: str
    imageUrl: str
    user_hint: Optional[str] = None
