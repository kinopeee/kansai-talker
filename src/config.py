"""
設定管理モジュール

アプリケーションの設定を一元管理します。
環境変数からの設定読み込みと、デフォルト値の管理を行います。
"""

import os
from typing import Optional


class Config:
    """アプリケーション設定クラス"""

    # Anthropic API設定
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    # モデル設定
    MODEL_NAME: str = "claude-3-5-sonnet-20241022"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7

    # システムプロンプト
    KANSAI_INSTRUCTION: str = (
        "これからの質問には全て関西弁で答えてください。"
        "できるだけ自然な関西弁を使ってください。"
        "「〜や」「〜やで」「〜やねん」「せやな」「ほんま」などの関西弁特有の表現を使って、"
        "親しみやすく答えてください。"
    )

    # UI設定
    APP_TITLE: str = "関西弁チャットボット 🗣️"
    APP_ICON: str = "💬"

    @classmethod
    def validate(cls) -> bool:
        """
        設定の妥当性を検証

        Returns:
            bool: 設定が有効な場合True、そうでない場合False
        """
        return cls.ANTHROPIC_API_KEY is not None and len(cls.ANTHROPIC_API_KEY) > 0

    @classmethod
    def get_error_message(cls) -> str:
        """
        設定エラー時のメッセージを取得

        Returns:
            str: エラーメッセージ
        """
        if not cls.ANTHROPIC_API_KEY:
            return (
                "ANTHROPIC_API_KEYが設定されていません。\n"
                "環境変数にAPIキーを設定してください。\n\n"
                "例: export ANTHROPIC_API_KEY='your_api_key_here'"
            )
        return "設定エラーが発生しました。"
