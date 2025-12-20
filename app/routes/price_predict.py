from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
from app.utils.price_model import PriceModel

router = APIRouter()


class PricePredictRequest(BaseModel):
    product_name: str


class PricePredictResponse(BaseModel):
    predicted_price: int
    product_name: str


@router.post("/predict_price", response_model=PricePredictResponse)
def predict_price(req: PricePredictRequest):
    """商品名から価格を推定"""
    try:
        # モデルを取得
        vectorizer = PriceModel.get_vectorizer()
        model = PriceModel.get_model()
        
        # TF-IDF ベクトル化
        X = vectorizer.transform([req.product_name])
        
        # log価格を予測
        log_price = model.predict(X)[0]
        
        # 円に戻す
        predicted_price = int(np.exp(log_price))
        
        # 異常値チェック（100円〜100万円の範囲に制限）
        if predicted_price < 100:
            predicted_price = 100
        elif predicted_price > 1_000_000:
            predicted_price = 1_000_000
        
        return PricePredictResponse(
            predicted_price=predicted_price,
            product_name=req.product_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"価格推定エラー: {str(e)}")