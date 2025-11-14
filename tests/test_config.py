"""
設定管理のテスト
"""

import os
import pytest
from src.config import Config


class TestConfig:
    """Config クラスのテスト"""

    def test_default_values(self):
        """デフォルト値が正しく設定されているかテスト"""
        assert Config.MODEL_NAME == "claude-3-5-sonnet-20241022"
        assert Config.MAX_TOKENS == 1000
        assert Config.TEMPERATURE == 0.7
        assert Config.APP_TITLE == "関西弁チャットボット 🗣️"
        assert Config.APP_ICON == "💬"

    def test_kansai_instruction_exists(self):
        """関西弁の指示文が存在するかテスト"""
        assert Config.KANSAI_INSTRUCTION
        assert "関西弁" in Config.KANSAI_INSTRUCTION

    def test_validate_with_api_key(self, monkeypatch):
        """APIキーが設定されている場合の検証テスト"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_api_key")
        # Configを再読み込み
        monkeypatch.setattr(Config, "ANTHROPIC_API_KEY", "test_api_key")
        assert Config.validate() is True

    def test_validate_without_api_key(self, monkeypatch):
        """APIキーが設定されていない場合の検証テスト"""
        monkeypatch.setattr(Config, "ANTHROPIC_API_KEY", None)
        assert Config.validate() is False

    def test_validate_with_empty_api_key(self, monkeypatch):
        """APIキーが空文字の場合の検証テスト"""
        monkeypatch.setattr(Config, "ANTHROPIC_API_KEY", "")
        assert Config.validate() is False

    def test_get_error_message(self, monkeypatch):
        """エラーメッセージが適切に返されるかテスト"""
        monkeypatch.setattr(Config, "ANTHROPIC_API_KEY", None)
        error_msg = Config.get_error_message()
        assert "ANTHROPIC_API_KEY" in error_msg
        assert "設定されていません" in error_msg
