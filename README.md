# hackathon-backend

東京大学のエンジニアコミュニティ「UT.code();」のハッカソン（UTTC）で **個人開発** したフリマアプリのバックエンドAPIです。
商品の出品・売買といった基本機能に加えて、**機械学習による価格予測・購入確率予測**、および **生成AIによる商品説明文・カテゴリの自動生成** を備えています。

> フロントエンド: https://github.com/Hiroki16-119/hackathon-frontend

## 主な機能

### 基本機能
- 商品の出品・一覧・詳細・編集・削除（CRUD）
- ユーザー認証（Firebase Authentication）
- 商品画像のアップロード（Google Cloud Storage）
- 購入処理・購入履歴

### 機械学習 / AI 機能（本プロジェクトの中心）
| 機能 | 概要 | 技術 |
|---|---|---|
| 💰 価格予測 | 商品名から適正な出品価格を推定 | TF-IDF + Ridge回帰（scikit-learn） |
| 🎯 購入確率予測 | ユーザーの購買履歴をもとに各商品の購入見込みを推定（パーソナライズ） | PyTorch（MLP） |
| 🏷️ カテゴリ自動推定 | 商品名からカテゴリを推定 | OpenAI API |
| ✍️ 説明文の自動生成 | 商品名・ヒントから出品用の説明文を生成 | OpenAI API |

#### 価格予測モデル（`app/utils/price_model.py`）
商品名を TF-IDF でベクトル化し、Ridge回帰で価格を推定します。学習済みモデルは `app/models/ml/*.joblib` に同梱。

#### 購入確率予測モデル（`app/utils/predictor.py`）
ユーザーの購買履歴から「カテゴリ嗜好ベクトル」と「平均購入価格」を算出し、対象商品の
**(ユーザー埋め込み, 価格差, カテゴリ埋め込み)** を入力とする MLP で購入確率を出力します。
`/predict_batch` では商品一覧に対して購入見込みを一括スコアリングでき、レコメンド的に利用できます。
学習済みモデルは `app/models/ml/model4.pt`。

## 使用技術
- **言語 / フレームワーク**: Python, FastAPI
- **機械学習**: PyTorch, scikit-learn, NumPy, joblib
- **生成AI**: OpenAI API
- **DB**: MySQL, SQLAlchemy
- **認証**: Firebase Authentication（firebase-admin）
- **ストレージ**: Google Cloud Storage
- **インフラ**: Docker / Docker Compose

## 主なAPIエンドポイント
| メソッド | パス | 説明 |
|---|---|---|
| `GET` / `POST` | `/products` | 商品の一覧取得・出品 |
| `GET` / `PUT` / `DELETE` | `/products/{id}` | 商品の詳細・編集・削除 |
| `POST` | `/auth/login` | ログイン |
| `POST` | `/images` | 画像アップロード（GCS） |
| `POST` | `/price/predict_price` | 価格予測（ML） |
| `POST` | `/predict`, `/predict_batch` | 購入確率予測（ML） |
| `POST` | `/category/predict_category` | カテゴリ推定（AI） |
| `POST` | `/generate_description` | 商品説明文の生成（AI） |

起動後、`http://localhost:8080/docs` で Swagger UI から全エンドポイントを確認できます。

## ディレクトリ構成
```
app/
├── main.py                  # FastAPI エントリポイント・ルーター登録・CORS
├── config.py
├── routes/                  # APIエンドポイント
│   ├── products.py / auth.py / users.py / images.py
│   ├── price_predict.py     # 価格予測 (ML)
│   ├── predict.py           # 購入確率予測 (ML)
│   ├── category_predict.py  # カテゴリ推定 (AI)
│   └── openai_description.py# 説明文生成 (AI)
├── dao/                     # DBアクセス層 (SQLAlchemy)
├── utils/
│   ├── price_model.py       # 価格予測モデル (scikit-learn)
│   ├── predictor.py         # 購入確率予測モデル (PyTorch)
│   ├── openai_client.py     # OpenAI 連携
│   ├── gcs.py               # Google Cloud Storage 連携
│   └── firebase_auth.py     # Firebase トークン検証
└── models/
    ├── models.py / predict.py  # Pydantic スキーマ
    └── ml/                     # 学習済みモデル (.joblib / .pt)
```

## セットアップ
前提: Docker / Docker Compose がインストール済みであること。

```bash
# 1. 環境変数ファイルを用意
cp .env.example .env
#    .env を編集（MySQL のパスワード、OpenAI APIキー、Firebase/GCP の認証情報など）

# 2. 起動
docker compose up --build
#    → API:        http://localhost:8080
#    → Swagger UI: http://localhost:8080/docs
```

> Firebase / Google Cloud を使う機能では、サービスアカウントJSONを用意し、
> `GOOGLE_APPLICATION_CREDENTIALS` にそのパスを指定してください（JSONはリポジトリにコミットしないこと）。

## スクリーンショット
<!-- TODO: アプリの画面キャプチャを docs/screenshots/ に置いて、下のリンクを差し替えてください -->

| 画面 | キャプチャ |
|---|---|
| 出品・価格予測 | <!-- ![価格予測](docs/screenshots/price_predict.png) --> _（スクリーンショットを追加）_ |
| 商品一覧・購入確率 | <!-- ![一覧](docs/screenshots/product_list.png) --> _（スクリーンショットを追加）_ |
| 説明文の自動生成 | <!-- ![説明文生成](docs/screenshots/description.png) --> _（スクリーンショットを追加）_ |

## 開発体制
UTTCハッカソンでの **個人開発**。フロントエンド・バックエンド・機械学習モデルをすべて担当しました。
