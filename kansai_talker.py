"""
Anthropic Claude 3.5 Sonnet APIを使用して関西弁で回答するStreamlitアプリ
"""

import os
import streamlit as st
from anthropic import Anthropic

# Anthropic APIキーを環境変数から取得
API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Streamlitアプリのタイトルを設定
st.title('Anthropic Claude 3.5 Sonnet API 関西弁で答えるアプリ')

# ユーザーからの質問を入力フィールドで受け取る
question = st.text_input('質問を入力してください')

def ask_anthropic(question: str) -> str:
    """
    Anthropic APIを使用して質問に対する回答を取得する関数

    Args:
        question (str): ユーザーからの質問

    Returns:
        str: AIの回答または発生したエラーメッセージ
    """
    # Anthropicクライアントを初期化
    client = Anthropic(api_key=API_KEY)
    
    # 関西弁で答えるように指示を追加
    kansai_instruction = "これからの質問には全て関西弁で答えてください。できるだけ自然な関西弁を使ってください。"
    
    try:
        # APIを呼び出して回答を生成
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            temperature=0.7,
            system=kansai_instruction,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        # 生成された回答のテキストを返す
        return response.content[0].text
    except Exception as e:
        # エラーが発生した場合はエラーメッセージを返す
        return f"エラー: {str(e)}"

# ボタンを作成し、クリックされたらAIに質問を送る
if st.button('AIに質問する'):
    if API_KEY is None:
        # APIキーが設定されていない場合はエラーメッセージを表示
        st.error('APIキーが設定されていません')
    else:
        # AIに質問を送信し、回答を取得
        response = ask_anthropic(question)
        # 回答を表示
        st.write("AIの回答:")
        st.write(response)