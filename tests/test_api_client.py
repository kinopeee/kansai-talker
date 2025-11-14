"""
APIクライアントのテスト
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.api_client import KansaiTalkerClient


class TestKansaiTalkerClient:
    """KansaiTalkerClient クラスのテスト"""

    def test_init_with_api_key(self):
        """APIキーを指定して初期化できるかテスト"""
        client = KansaiTalkerClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.model == "claude-3-5-sonnet-20241022"
        assert client.max_tokens == 1000
        assert client.temperature == 0.7

    def test_init_without_api_key(self, monkeypatch):
        """APIキーがない場合にエラーが発生するかテスト"""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ValueError, match="APIキーが設定されていません"):
            KansaiTalkerClient()

    def test_init_with_custom_parameters(self):
        """カスタムパラメータで初期化できるかテスト"""
        client = KansaiTalkerClient(
            api_key="test_key",
            model="claude-3-opus-20240229",
            max_tokens=500,
            temperature=0.5,
        )
        assert client.model == "claude-3-opus-20240229"
        assert client.max_tokens == 500
        assert client.temperature == 0.5

    def test_ask_with_empty_question(self):
        """空の質問でエラーが発生するかテスト"""
        client = KansaiTalkerClient(api_key="test_key")
        with pytest.raises(ValueError, match="質問を入力してください"):
            client.ask("")

    def test_ask_with_whitespace_question(self):
        """空白のみの質問でエラーが発生するかテスト"""
        client = KansaiTalkerClient(api_key="test_key")
        with pytest.raises(ValueError, match="質問を入力してください"):
            client.ask("   ")

    @patch("src.api_client.Anthropic")
    def test_ask_success(self, mock_anthropic):
        """正常に質問できるかテスト"""
        # モックの設定
        mock_response = Mock()
        mock_response.content = [Mock(text="せやな、それはええ質問やで！")]
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        # テスト実行
        client = KansaiTalkerClient(api_key="test_key")
        response = client.ask("こんにちは")

        # 検証
        assert response == "せやな、それはええ質問やで！"
        mock_client.messages.create.assert_called_once()

    @patch("src.api_client.Anthropic")
    def test_ask_with_conversation_history(self, mock_anthropic):
        """会話履歴を含めて質問できるかテスト"""
        # モックの設定
        mock_response = Mock()
        mock_response.content = [Mock(text="そうやで！")]
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        # テスト実行
        client = KansaiTalkerClient(api_key="test_key")
        history = [
            {"role": "user", "content": "こんにちは"},
            {"role": "assistant", "content": "ほな、どないしたん？"},
        ]
        response = client.ask("元気？", conversation_history=history)

        # 検証
        assert response == "そうやで！"
        call_args = mock_client.messages.create.call_args
        messages = call_args.kwargs["messages"]
        assert len(messages) == 3
        assert messages[0]["content"] == "こんにちは"
        assert messages[1]["content"] == "ほな、どないしたん？"
        assert messages[2]["content"] == "元気？"

    @patch("src.api_client.Anthropic")
    def test_ask_api_error(self, mock_anthropic):
        """API呼び出しエラーが適切に処理されるかテスト"""
        # モックの設定
        mock_client = Mock()
        mock_client.messages.create.side_effect = Exception("API Error")
        mock_anthropic.return_value = mock_client

        # テスト実行
        client = KansaiTalkerClient(api_key="test_key")
        with pytest.raises(Exception, match="API呼び出しエラー"):
            client.ask("こんにちは")
