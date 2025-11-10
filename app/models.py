from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    price: int
    description: str
    imageUrl: str
    user_hint: Optional[str] = None
