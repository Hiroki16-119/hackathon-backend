from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: int
    description: str
    imageUrl: str = Field(alias="imageUrl")
    user_hint: Optional[str] = None

    class Config:
        populate_by_name = True


class ProductRead(BaseModel):
    id: str
    name: str
    price: int
    description: str
    image_url: str   # ← DB の命名
    user_hint: Optional[str]