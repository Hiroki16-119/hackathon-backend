import joblib
import os

class PriceModel:
    _vectorizer = None
    _model = None
    
    @classmethod
    def load_models(cls):
        """モデルを一度だけロード"""
        if cls._vectorizer is None or cls._model is None:
            # app/utils/price_model.py から app/models/ml/ へのパス
            current_dir = os.path.dirname(__file__)  # app/utils/
            vectorizer_path = os.path.join(current_dir, "..", "models", "ml", "tfidf_vectorizer.joblib")
            model_path = os.path.join(current_dir, "..", "models", "ml", "ridge_price_model.joblib")
            
            # デバッグ用
            print(f"Loading vectorizer from: {vectorizer_path}")
            print(f"Loading model from: {model_path}")
            print(f"Vectorizer exists: {os.path.exists(vectorizer_path)}")
            print(f"Model exists: {os.path.exists(model_path)}")
            
            try:
                cls._vectorizer = joblib.load(vectorizer_path)
                cls._model = joblib.load(model_path)
                print("Models loaded successfully!")
            except FileNotFoundError as e:
                raise RuntimeError(f"モデルファイルが見つかりません: {e}")
        
        return cls._vectorizer, cls._model
    
    @classmethod
    def get_vectorizer(cls):
        """ベクトライザーを取得"""
        cls.load_models()
        return cls._vectorizer
    
    @classmethod
    def get_model(cls):
        """モデルを取得"""
        cls.load_models()
        return cls._model