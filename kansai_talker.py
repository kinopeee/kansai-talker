"""
Anthropic Claude 3.5 Sonnet APIを使用して関西弁で回答するStreamlitアプリ
"""

import os
import streamlit as st
import requests
import anthropic

DEBUG = True

# Anthropic APIキーを環境変数またはStreamlit secretsから取得
def get_api_key():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    source = "環境変数"
    
    if not api_key and hasattr(st, 'secrets') and 'ANTHROPIC_API_KEY' in st.secrets:
        api_key = st.secrets['ANTHROPIC_API_KEY']
        source = "Streamlit secrets"
    
    if not api_key and 'api_key' in st.session_state:
        api_key = st.session_state.api_key
        source = "セッション状態"
    
    if api_key:
        st.session_state.api_key = api_key
    
    return api_key, source

API_KEY = os.getenv("ANTHROPIC_API_KEY")
api_key_source = "環境変数"

if not API_KEY and hasattr(st, 'secrets') and 'ANTHROPIC_API_KEY' in st.secrets:
    API_KEY = st.secrets['ANTHROPIC_API_KEY']
    api_key_source = "Streamlit secrets"
    
if not API_KEY:
    API_KEY = st.text_input("APIキーを入力してください", type="password")
    if API_KEY:
        api_key_source = "ユーザー入力"

if DEBUG:
    st.sidebar.write("デバッグ情報:")
    
    st.sidebar.write("環境変数:")
    for env_var in os.environ:
        if env_var == "ANTHROPIC_API_KEY":
            st.sidebar.write(f"{env_var}: [設定されています]")
        else:
            st.sidebar.write(f"{env_var}: {os.environ[env_var][:10]}...")
    
    # Streamlit secretsの情報を表示
    if hasattr(st, 'secrets'):
        st.sidebar.write("Streamlit secrets:")
        for key in st.secrets:
            if key == "ANTHROPIC_API_KEY":
                if st.secrets[key]:
                    st.sidebar.write(f"{key}: [設定されています]")
                else:
                    st.sidebar.write(f"{key}: [空]")
            else:
                st.sidebar.write(f"{key}: {str(st.secrets[key])[:10]}...")

# APIキーが設定されているか確認
if API_KEY:
    st.sidebar.success(f"APIキーが{api_key_source}から設定されています")
    if len(API_KEY) > 5:
        st.sidebar.write(f"APIキーの先頭: {API_KEY[:5]}...")
    if DEBUG:
        st.sidebar.write(f"APIキーの長さ: {len(API_KEY)}")
        st.sidebar.write(f"APIキーの文字種: {'英数字のみ' if API_KEY.isalnum() else '特殊文字を含む'}")
else:
    st.sidebar.error("APIキーが設定されていません")

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
    # 関西弁で答えるように指示を追加
    kansai_instruction = "これからの質問には全て関西弁で答えてください。できるだけ自然な関西弁を使ってください。"
    
    try:
        api_key = API_KEY
        source = api_key_source
            
        if not api_key:
            return "APIキーが設定されていません。環境変数ANTHROPIC_API_KEYを設定してください。"
        
        if DEBUG:
            st.sidebar.write(f"API呼び出し時のAPIキー: {api_key[:5]}... (from {source})")
            
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 300,
            "temperature": 0.7,
            "system": kansai_instruction,
            "messages": [
                {
                    "role": "user", 
                    "content": question
                }
            ]
        }
        
        # APIを呼び出して回答を生成
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            # 生成された回答のテキストを返す
            return response.json()["content"][0]["text"]
        else:
            # APIエラーの場合はエラーメッセージを返す
            return f"APIエラー: ステータスコード {response.status_code}, レスポンス: {response.text}"
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
