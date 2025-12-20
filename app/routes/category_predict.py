from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.openai_client import predict_category_with_openai

router = APIRouter()

class CategoryPredictRequest(BaseModel):
    product_name: str

class CategoryPredictResponse(BaseModel):
    category: str

@router.post("/predict_category", response_model=CategoryPredictResponse)
def predict_category(req: CategoryPredictRequest):
    """OpenAI API を使って商品名からカテゴリーを推定"""
    try:
        category = predict_category_with_openai(req.product_name)
        return CategoryPredictResponse(category=category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"カテゴリー推定エラー: {str(e)}")