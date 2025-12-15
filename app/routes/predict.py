from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.predictor import PurchasePredictor
from app.dao.db import get_db
from app.models.predict import (
    PredictRequest, PredictResponse,
    ProductItem, PredictBatchRequest, PredictItem, PredictBatchResponse
)

router = APIRouter()
predictor = PurchasePredictor("app/models/ml/model4.pt", "app/models/ml/tfidf4.pkl")

@router.post("/predict", response_model=PredictResponse)
def predict_purchase(req: PredictRequest, db: Session = Depends(get_db)):
    try:
        prob = predictor.predict(
            db=db,
            user_id=req.user_id,
            category_code=req.category_code,
            price=req.price
        )
        return PredictResponse(probability=prob)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict_batch", response_model=PredictBatchResponse)
def predict_batch(req: PredictBatchRequest, db: Session = Depends(get_db)):
    try:
        user_emb, user_avg_price = predictor.get_user_stats(db, req.user_id)
        results = []
        for p in req.products:
            try:
                prob = predictor.predict_with_user_stats(user_emb, user_avg_price, p.category_code, p.price)
            except Exception:
                prob = 0.0
            results.append(PredictItem(product_id=p.product_id, probability=float(prob)))
        results.sort(key=lambda x: x.probability, reverse=True)
        return PredictBatchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))