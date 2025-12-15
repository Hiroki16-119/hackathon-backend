from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    user_id: str
    category_code: str
    price: int

class PredictResponse(BaseModel):
    probability: float

class ProductItem(BaseModel):
    product_id: str
    category_code: str
    price: float

class PredictBatchRequest(BaseModel):
    user_id: str
    products: List[ProductItem]

class PredictItem(BaseModel):
    product_id: str
    probability: float

class PredictBatchResponse(BaseModel):
    results: List[PredictItem]