import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_description_text(name: str, user_hint: str = None):
    system_prompt = (
        "あなたはフリマアプリの出品者をサポートするマーケティング担当者です。"
        "購入者の興味を引きつけ、信頼感を与える魅力的で簡潔な紹介文を作成してください。"
        "文章は丁寧で自然な日本語にしてください。"
        "商品説明の際には、商品の特徴、状態、名前等商品に関することを、読みやすいように箇条書きを用いて説明してください"
    )

    if user_hint:
        prompt = f"以下の商品について魅力的な紹介文を100文字以内で書いてください。\n商品名: {name}\n補足情報: {user_hint}"
    else:
        prompt = f"以下の商品について魅力的な紹介文を100文字以内で書いてください。\n商品名: {name}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


def predict_category_with_openai(product_name: str):
    """OpenAI API を使って商品名からカテゴリーを推定"""
    system_prompt = (
        "あなたはフリマアプリのカテゴリー分類の専門家です。\n"
        "商品名から最も適切なカテゴリーを1つ選んでください。\n"
        "**「その他」は絶対に使用しないでください。**\n"
        "必ず具体的なカテゴリー名を10文字以内で答えてください。\n\n"
        "【回答例】\n"
        "iPhone 13 Pro → 家電\n"
        "ユニクロ セーター → ファッション\n"
        "ワンピース 漫画 → 本・雑誌\n"
        "Nintendo Switch → ゲーム\n"
        "サッカーボール → スポーツ\n"
        "ソファ 3人掛け → 家具\n"
        "リップ シャネル → コスメ\n"
        "プロテイン → 食品\n"
        "ベビーカー → ベビー用品\n"
        "革靴 ビジネス → 靴\n"
        "腕時計 メンズ → アクセサリー\n"
        "ぬいぐるみ → おもちゃ\n"
        "観葉植物 → インテリア\n\n"
        "**重要：必ず具体的なカテゴリー名を返してください。「その他」「不明」「未分類」などは使用禁止です。**\n"
        "カテゴリー名のみを返してください。説明は不要です。"
    )

    prompt = f"商品名: {product_name}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,  # さらに低くして一貫性を最大化
    )

    category = response.choices[0].message.content.strip()
    
    # 保険：「その他」が返ってきたら「雑貨」に変換
    if category in ["その他", "不明", "未分類", "その他雑貨"]:
        return "雑貨"
    
    return category
