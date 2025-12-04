import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_description_text(name: str, user_hint: str = None):
    system_prompt = (
        "あなたはフリマアプリの出品者をサポートするマーケティング担当者です。"
        "購入者の興味を引きつけ、信頼感を与える魅力的で簡潔な紹介文を作成してください。"
        "文章は丁寧で自然な日本語にしてください。"
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
