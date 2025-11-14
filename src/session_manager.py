"""
セッション管理モジュール

Streamlitのセッション状態を管理し、チャット履歴を保持します。
"""

from typing import List, Dict
import streamlit as st


class SessionManager:
    """チャットセッションの状態管理クラス"""

    # セッション状態のキー
    MESSAGES_KEY = "messages"
    INITIALIZED_KEY = "initialized"

    @staticmethod
    def initialize() -> None:
        """
        セッション状態を初期化

        初回アクセス時にチャット履歴を空のリストで初期化します。
        """
        if SessionManager.INITIALIZED_KEY not in st.session_state:
            st.session_state[SessionManager.INITIALIZED_KEY] = True
            st.session_state[SessionManager.MESSAGES_KEY] = []

    @staticmethod
    def get_messages() -> List[Dict[str, str]]:
        """
        チャット履歴を取得

        Returns:
            List[Dict[str, str]]: チャット履歴
                形式: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        """
        SessionManager.initialize()
        return st.session_state[SessionManager.MESSAGES_KEY]

    @staticmethod
    def add_message(role: str, content: str) -> None:
        """
        メッセージをチャット履歴に追加

        Args:
            role: メッセージの送信者（"user" または "assistant"）
            content: メッセージ内容
        """
        SessionManager.initialize()
        st.session_state[SessionManager.MESSAGES_KEY].append(
            {"role": role, "content": content}
        )

    @staticmethod
    def clear_messages() -> None:
        """チャット履歴をクリア"""
        st.session_state[SessionManager.MESSAGES_KEY] = []

    @staticmethod
    def get_conversation_history() -> List[Dict[str, str]]:
        """
        API呼び出し用の会話履歴を取得

        Returns:
            List[Dict[str, str]]: API用の会話履歴
        """
        return SessionManager.get_messages()

    @staticmethod
    def has_messages() -> bool:
        """
        メッセージが存在するかチェック

        Returns:
            bool: メッセージが1つ以上存在する場合True
        """
        return len(SessionManager.get_messages()) > 0
