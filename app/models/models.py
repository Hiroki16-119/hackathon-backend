from typing import Optional
from pydantic import BaseModel, Field

# リクエストはフロントが camelCase を送る想定 (imageUrl)
class ProductBase(BaseModel):
    name: str
    price: int
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    user_hint: Optional[str] = None
    seller_id: Optional[str] = None
    seller_name: Optional[str] = None
    is_purchased: bool = False  # ← 追加

    class Config:
        validate_by_name = True
        from_attributes = True

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    user_hint: Optional[str] = None
    is_purchased: Optional[bool] = None  # ← 追加

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class UserRead(BaseModel):
    id: str
    name: str | None = None
    email: str

    class Config:
        from_attributes = True  # Pydantic v2用

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2用