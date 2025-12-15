import torch
import joblib
import numpy as np
from sqlalchemy.orm import Session
from app.dao.product_table import ProductTable
from app.dao.purchase_table import PurchaseTable

class PurchasePredictor:
    def __init__(self, model_path="app/models/ml/model4.pt", tfidf_path="app/models/ml/tfidf4.pkl"):
        self.tfidf = joblib.load(tfidf_path)
        self.EMB_DIM = len(self.tfidf.get_feature_names_out())
        input_dim = 2 * self.EMB_DIM + 1  # user_emb, price_diff, cat_emb
        self.model = self._load_model(model_path, input_dim)
        self.model.eval()

    def _load_model(self, path, input_dim):
        import torch.nn as nn
        class PurchaseMLP(nn.Module):
            def __init__(self, input_dim):
                super().__init__()
                self.net = nn.Sequential(
                    nn.Linear(input_dim, 128),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(128, 1)
                )
            def forward(self, x):
                return self.net(x).squeeze(1)
        model = PurchaseMLP(input_dim)
        model.load_state_dict(torch.load(path, map_location="cpu"))
        return model

    def _compute_global_avg_price(self, db: Session):
        q = (
            db.query(ProductTable.price)
            .join(PurchaseTable, ProductTable.id == PurchaseTable.product_id)
            .filter(ProductTable.price != None)
        )
        prices = [r[0] for r in q.all()]
        if not prices:
            return 0.0
        prices = np.array(prices, dtype=float)
        return float(np.mean(np.log1p(prices)))

    def get_user_stats(self, db: Session, user_id: str):
        purchases = db.query(PurchaseTable).filter(PurchaseTable.user_id == user_id).all()
        if not purchases:
            global_avg = self._compute_global_avg_price(db)
            return np.zeros(self.EMB_DIM), global_avg

        category_codes = []
        prices = []
        for purchase in purchases:
            product = db.query(ProductTable).filter(ProductTable.id == purchase.product_id).first()
            if not product:
                continue
            if getattr(product, "category", None):
                category_codes.append(product.category)
            if getattr(product, "price", None) is not None:
                try:
                    prices.append(float(product.price))
                except Exception:
                    pass

        if category_codes:
            cat_embs = self.tfidf.transform(category_codes).toarray()
            user_emb = np.mean(cat_embs, axis=0)
        else:
            user_emb = np.zeros(self.EMB_DIM)

        if prices:
            prices = np.array(prices, dtype=float)
            user_avg_price = float(np.mean(np.log1p(prices)))
        else:
            user_avg_price = self._compute_global_avg_price(db)

        return user_emb, user_avg_price

    def predict(self, db: Session, user_id: str, category_code: str, price: float) -> float:
        user_emb, user_avg_price = self.get_user_stats(db, user_id)
        item_price_log = float(np.log1p(price))  # 学習時log1pしている場合
        price_diff = user_avg_price - item_price_log
        cat_emb = self.tfidf.transform([category_code]).toarray()[0]
        X = np.hstack([user_emb, np.array([price_diff]), cat_emb])
        X_tensor = torch.tensor([X], dtype=torch.float32)
        with torch.no_grad():
            logit = self.model(X_tensor)
            prob = torch.sigmoid(logit).item()
        return prob

    def predict_with_user_stats(self, user_emb: np.ndarray, user_avg_price: float, category_code: str, price: float) -> float:
        item_price_log = float(np.log1p(price))
        price_diff = user_avg_price - item_price_log
        cat_emb = self.tfidf.transform([category_code]).toarray()[0]
        X = np.hstack([user_emb, np.array([price_diff]), cat_emb])
        X_tensor = torch.tensor([X], dtype=torch.float32)
        with torch.no_grad():
            logit = self.model(X_tensor)
            prob = torch.sigmoid(logit).item()
        return prob