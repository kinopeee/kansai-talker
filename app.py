"""
関西弁チャットボット - メインアプリケーション

Anthropic Claude APIを使用して、関西弁で会話するチャットボットです。
Streamlitで構築されたWebインターフェースを提供します。
"""

import streamlit as st
from src.config import Config
from src.api_client import KansaiTalkerClient
from src.session_manager import SessionManager
from src.ui.components import (
    render_header,
    render_sidebar,
    render_chat_history,
    render_chat_input,
    show_error,
)


def main() -> None:
    """メインアプリケーション"""

    # ページ設定
    st.set_page_config(
        page_title="関西弁チャットボット",
        page_icon=Config.APP_ICON,
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # セッション初期化
    SessionManager.initialize()

    # ヘッダーとサイドバーを描画
    render_header()
    render_sidebar()

    # 設定の検証
    if not Config.validate():
        show_error(Config.get_error_message())
        st.stop()

    # APIクライアントの初期化
    try:
        client = KansaiTalkerClient()
    except ValueError as e:
        show_error(str(e))
        st.stop()
    except Exception as e:
        show_error(f"初期化エラー: {str(e)}")
        st.stop()

    # チャット履歴を表示
    render_chat_history()

    # ユーザー入力を受け付け
    user_input = render_chat_input()

    if user_input:
        # ユーザーメッセージを追加して表示
        SessionManager.add_message("user", user_input)
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # AIの応答を取得
        with st.chat_message("assistant", avatar="🗣️"):
            with st.spinner("考え中..."):
                try:
                    # 会話履歴を取得（最後のユーザーメッセージは除く）
                    conversation_history = SessionManager.get_conversation_history()[:-1]

                    # API呼び出し
                    response = client.ask(
                        question=user_input,
                        conversation_history=conversation_history,
                    )

                    # 応答を表示
                    st.markdown(response)

                    # アシスタントメッセージをセッションに追加
                    SessionManager.add_message("assistant", response)

                except ValueError as e:
                    error_msg = f"入力エラー: {str(e)}"
                    st.error(error_msg)
                    # エラーメッセージもセッションに記録
                    SessionManager.add_message("assistant", error_msg)

                except Exception as e:
                    error_msg = f"エラーが発生しました: {str(e)}"
                    st.error(error_msg)
                    # エラーメッセージもセッションに記録
                    SessionManager.add_message("assistant", error_msg)


if __name__ == "__main__":
    main()
