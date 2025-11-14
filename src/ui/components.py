"""
UIコンポーネントモジュール

Streamlitを使用したUIコンポーネントを提供します。
"""

import streamlit as st
from typing import Optional
from ..config import Config
from ..session_manager import SessionManager


def render_header() -> None:
    """アプリケーションのヘッダーを描画"""
    st.title(Config.APP_TITLE)
    st.markdown(
        """
        関西弁で何でも答える気さくなAIチャットボットやで！
        気軽に質問してな〜 💬
        """
    )


def render_sidebar() -> None:
    """サイドバーを描画（設定やヘルプ情報）"""
    with st.sidebar:
        st.header("📝 使い方")
        st.markdown(
            """
            1. 下の入力欄に質問を入力
            2. 「送信」ボタンをクリック
            3. 関西弁で回答が返ってきます！

            会話履歴は保持されるので、
            続けて質問できますよ〜
            """
        )

        st.divider()

        # 会話をクリアするボタン
        if st.button("🗑️ 会話をクリア", use_container_width=True):
            SessionManager.clear_messages()
            st.rerun()

        st.divider()

        st.header("⚙️ 設定")
        st.markdown(f"**モデル:** {Config.MODEL_NAME}")
        st.markdown(f"**最大トークン:** {Config.MAX_TOKENS}")
        st.markdown(f"**Temperature:** {Config.TEMPERATURE}")


def render_chat_history() -> None:
    """チャット履歴を描画"""
    messages = SessionManager.get_messages()

    for message in messages:
        role = message["role"]
        content = message["content"]

        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
        else:  # assistant
            with st.chat_message("assistant", avatar="🗣️"):
                st.markdown(content)


def render_chat_input() -> Optional[str]:
    """
    チャット入力欄を描画

    Returns:
        Optional[str]: 入力された質問（入力がない場合はNone）
    """
    return st.chat_input("質問を入力してください...")


def show_error(message: str) -> None:
    """
    エラーメッセージを表示

    Args:
        message: 表示するエラーメッセージ
    """
    st.error(f"❌ {message}")


def show_warning(message: str) -> None:
    """
    警告メッセージを表示

    Args:
        message: 表示する警告メッセージ
    """
    st.warning(f"⚠️ {message}")


def show_info(message: str) -> None:
    """
    情報メッセージを表示

    Args:
        message: 表示する情報メッセージ
    """
    st.info(f"ℹ️ {message}")


def show_success(message: str) -> None:
    """
    成功メッセージを表示

    Args:
        message: 表示する成功メッセージ
    """
    st.success(f"✅ {message}")
