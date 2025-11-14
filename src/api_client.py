"""
Anthropic API クライアントモジュール

Anthropic APIとの通信を担当し、関西弁での応答を生成します。
"""

from typing import List, Dict, Optional
from anthropic import Anthropic
from .config import Config


class KansaiTalkerClient:
    """関西弁チャットボットのAPIクライアント"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ):
        """
        KansaiTalkerClientの初期化

        Args:
            api_key: Anthropic APIキー（省略時はConfig.ANTHROPIC_API_KEYを使用）
            model: 使用するモデル名（省略時はConfig.MODEL_NAMEを使用）
            max_tokens: 最大トークン数（省略時はConfig.MAX_TOKENSを使用）
            temperature: 温度パラメータ（省略時はConfig.TEMPERATUREを使用）
        """
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        self.model = model or Config.MODEL_NAME
        self.max_tokens = max_tokens or Config.MAX_TOKENS
        self.temperature = temperature or Config.TEMPERATURE

        if not self.api_key:
            raise ValueError("APIキーが設定されていません")

        self.client = Anthropic(api_key=self.api_key)

    def ask(
        self,
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        質問に対して関西弁で回答を生成

        Args:
            question: ユーザーからの質問
            conversation_history: 会話履歴（オプション）
                形式: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

        Returns:
            str: AIの回答

        Raises:
            ValueError: 質問が空の場合
            Exception: API呼び出しエラー
        """
        if not question or not question.strip():
            raise ValueError("質問を入力してください")

        # メッセージリストの構築
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": question})

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=Config.KANSAI_INSTRUCTION,
                messages=messages,
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"API呼び出しエラー: {str(e)}")

    def ask_streaming(
        self,
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ):
        """
        ストリーミングで回答を生成（将来の拡張用）

        Args:
            question: ユーザーからの質問
            conversation_history: 会話履歴（オプション）

        Yields:
            str: AIの回答の一部

        Raises:
            ValueError: 質問が空の場合
            Exception: API呼び出しエラー
        """
        if not question or not question.strip():
            raise ValueError("質問を入力してください")

        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": question})

        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=Config.KANSAI_INSTRUCTION,
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise Exception(f"API呼び出しエラー: {str(e)}")
