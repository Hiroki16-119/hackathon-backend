import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException
import os
import json

# サービスアカウントキーを環境変数から取得
service_account_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
if not service_account_json:
    raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_JSON 環境変数が設定されていません")

service_account_info = json.loads(service_account_json)
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print("Firebase認証エラー:", e)  # ← 追加
        raise HTTPException(status_code=401, detail="Invalid Firebase token")