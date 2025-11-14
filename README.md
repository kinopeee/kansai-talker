# 関西弁チャットボット 🗣️

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red)](https://streamlit.io/)
[![Anthropic](https://img.shields.io/badge/Anthropic-Claude%203.5%20Sonnet-purple)](https://www.anthropic.com/)

## 概要

Anthropic社のClaude 3.5 Sonnet APIを使用した、関西弁で会話するチャットボットです。
Streamlitで構築されたモダンなWebインターフェースを提供し、会話履歴を保持しながら自然な関西弁での対話が可能です。

## 主な機能

- 🗣️ **関西弁での自然な会話**: Claude 3.5 Sonnetによる高品質な関西弁応答
- 💬 **会話履歴の保持**: セッション中の会話を記憶し、文脈を理解した応答
- 🎨 **モダンなUI**: Streamlitのチャットインターフェース
- 🔄 **会話のクリア**: いつでも会話をリセット可能
- ⚙️ **設定の可視化**: 使用中のモデルやパラメータの確認
- 🧪 **テスト完備**: ユニットテストによる品質保証
- 📦 **モジュール化されたアーキテクチャ**: 保守性と拡張性を考慮した設計

## プロジェクト構造

```
kansai-talker/
├── src/                      # ソースコード
│   ├── __init__.py
│   ├── config.py             # 設定管理
│   ├── api_client.py         # Anthropic APIクライアント
│   ├── session_manager.py    # セッション管理
│   └── ui/                   # UIコンポーネント
│       ├── __init__.py
│       └── components.py
├── tests/                    # テストコード
│   ├── __init__.py
│   ├── test_config.py
│   └── test_api_client.py
├── app.py                    # メインアプリケーション
├── kansai_talker.py         # レガシーファイル（後方互換性用）
├── requirements.txt          # 本番用依存関係
├── requirements-dev.txt      # 開発用依存関係
├── .env.example             # 環境変数の例
├── LICENSE
└── README.md
```

## 動作条件

- **Python**: 3.9以上
- **Anthropic APIキー**: [Anthropic Console](https://console.anthropic.com/)から取得

## インストール方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/kansai-talker.git
cd kansai-talker
```

### 2. 仮想環境の作成（推奨）

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

開発環境の場合:
```bash
pip install -r requirements-dev.txt
```

### 4. 環境変数の設定

`.env.example`をコピーして`.env`を作成し、APIキーを設定します:

```bash
cp .env.example .env
```

`.env`ファイルを編集:
```
ANTHROPIC_API_KEY=your_api_key_here
```

または、直接環境変数を設定:
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

### 5. アプリケーションの起動

```bash
streamlit run app.py
```

ブラウザで自動的に開きます（通常は http://localhost:8501）

## 使い方

1. アプリケーションが起動したら、画面下部の入力欄に質問を入力
2. Enterキーを押すか、送信ボタンをクリック
3. AIが関西弁で回答を返します
4. 会話は継続され、文脈を理解した応答が得られます
5. サイドバーの「会話をクリア」ボタンで会話履歴をリセット可能

## 開発

### テストの実行

```bash
# すべてのテストを実行
pytest

# カバレッジ付きで実行
pytest --cov=src tests/

# 詳細な出力
pytest -v
```

### コード品質チェック

```bash
# フォーマット
black src/ tests/

# リント
flake8 src/ tests/

# 型チェック
mypy src/
```

## 設定のカスタマイズ

`src/config.py`で以下の設定を変更できます:

- `MODEL_NAME`: 使用するClaudeモデル（デフォルト: claude-3-5-sonnet-20241022）
- `MAX_TOKENS`: 最大トークン数（デフォルト: 1000）
- `TEMPERATURE`: 応答のランダム性（デフォルト: 0.7）
- `KANSAI_INSTRUCTION`: システムプロンプト

## トラブルシューティング

### APIキーエラー

```
ANTHROPIC_API_KEYが設定されていません
```

環境変数`ANTHROPIC_API_KEY`が正しく設定されているか確認してください。

### モジュールが見つからないエラー

依存関係を再インストールしてください:
```bash
pip install -r requirements.txt --upgrade
```

### Streamlitが起動しない

ポート8501が使用中の場合、別のポートで起動できます:
```bash
streamlit run app.py --server.port 8502
```

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。

## 謝辞

- [Anthropic](https://www.anthropic.com/)のClaude APIを使用
- [Streamlit](https://streamlit.io/)でUIを構築

## バージョン履歴

### v2.0.0 (2025-01-XX)
- モジュール化されたアーキテクチャへの全面リファクタリング
- チャット履歴機能の追加
- ユニットテストの追加
- 最新のClaude 3.5 Sonnetモデルへの更新
- UIの改善とサイドバーの追加

### v1.0.0 (初回リリース)
- 基本的な関西弁チャットボット機能