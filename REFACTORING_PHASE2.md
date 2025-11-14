# リファクタリング計画 Phase 2

## 概要

Phase 1（v2.0.0）で基本的なモジュール化とアーキテクチャの改善が完了しました。
Phase 2では、ユーザー体験の向上と高度な機能の追加を目指します。

## 現状の評価

### ✅ 完了している項目（Phase 1）
- モジュール化されたアーキテクチャ
- 設定管理の一元化
- セッション管理（メモリ内）
- ユニットテストの基盤
- チャットUI
- エラーハンドリング
- 型ヒントとDocstring

### 🎯 Phase 2の目標

1. **ユーザー体験の向上**
   - リアルタイムなストリーミング応答
   - 会話履歴の永続化
   - レスポンスタイムの最適化

2. **機能の拡張**
   - 複数の会話モード（関西弁以外も）
   - 会話のエクスポート/インポート
   - API使用量の可視化

3. **保守性とスケーラビリティ**
   - ロギング機能の追加
   - パフォーマンスモニタリング
   - エラートラッキング

---

## 📋 Phase 2 リファクタリングタスク

### 🚀 優先度: 高

#### 1. ストリーミング応答機能の実装

**目的**: ユーザー体験の向上（応答の待ち時間削減）

**実装内容**:
```python
# src/api_client.py に既にask_streaming()のスケルトンあり
# 完全に実装して、UIと統合する

# app.py での使用例:
with st.chat_message("assistant", avatar="🗣️"):
    message_placeholder = st.empty()
    full_response = ""
    
    for chunk in client.ask_streaming(user_input, conversation_history):
        full_response += chunk
        message_placeholder.markdown(full_response + "▌")
    
    message_placeholder.markdown(full_response)
```

**影響範囲**:
- `src/api_client.py`: `ask_streaming()`メソッドの完成
- `app.py`: ストリーミングモードの追加
- `src/ui/components.py`: ストリーミング表示用の新しいコンポーネント
- テストの追加

**見積もり**: 4-6時間

---

#### 2. 会話履歴の永続化

**目的**: セッション間での会話履歴の保持

**実装内容**:
```python
# 新規ファイル: src/storage.py

from typing import List, Dict, Optional
import json
from datetime import datetime
from pathlib import Path

class ConversationStorage:
    """会話履歴の永続化を管理"""
    
    def __init__(self, storage_dir: str = ".conversations"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def save_conversation(
        self, 
        conversation_id: str, 
        messages: List[Dict[str, str]],
        metadata: Optional[Dict] = None
    ) -> None:
        """会話を保存"""
        pass
    
    def load_conversation(self, conversation_id: str) -> List[Dict[str, str]]:
        """会話を読み込み"""
        pass
    
    def list_conversations(self) -> List[Dict]:
        """保存されている会話のリストを取得"""
        pass
    
    def delete_conversation(self, conversation_id: str) -> None:
        """会話を削除"""
        pass
    
    def export_to_json(self, conversation_id: str, output_path: str) -> None:
        """会話をJSONにエクスポート"""
        pass
    
    def export_to_markdown(self, conversation_id: str, output_path: str) -> None:
        """会話をMarkdownにエクスポート"""
        pass
```

**UI統合**:
- サイドバーに「会話を保存」ボタン
- 「保存された会話」のリスト表示
- 会話の読み込み機能
- エクスポート機能（JSON/Markdown）

**影響範囲**:
- `src/storage.py`: 新規作成
- `src/session_manager.py`: ストレージ連携
- `src/ui/components.py`: 保存/読み込みUI
- `tests/test_storage.py`: 新規作成

**見積もり**: 6-8時間

---

#### 3. ロギング機能の追加

**目的**: デバッグとモニタリングの改善

**実装内容**:
```python
# 新規ファイル: src/logger.py

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class AppLogger:
    """アプリケーションロガー"""
    
    @staticmethod
    def setup_logger(
        name: str = "kansai_talker",
        log_dir: str = "logs",
        level: int = logging.INFO
    ) -> logging.Logger:
        """ロガーのセットアップ"""
        log_dir_path = Path(log_dir)
        log_dir_path.mkdir(exist_ok=True)
        
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # ファイルハンドラ（ローテーション付き）
        file_handler = RotatingFileHandler(
            log_dir_path / "app.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        
        # コンソールハンドラ
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
```

**ロギング対象**:
- API呼び出し（リクエスト/レスポンス時間）
- エラー発生時の詳細情報
- セッション開始/終了
- ユーザーアクション

**影響範囲**:
- `src/logger.py`: 新規作成
- `src/api_client.py`: ログ追加
- `src/session_manager.py`: ログ追加
- `app.py`: ログ追加

**見積もり**: 3-4時間

---

### 🎨 優先度: 中

#### 4. 複数のシステムプロンプトプリセット

**目的**: 様々な会話スタイルへの対応

**実装内容**:
```python
# src/config.py の拡張

class PromptPresets:
    """システムプロンプトのプリセット"""
    
    KANSAI = (
        "これからの質問には全て関西弁で答えてください。"
        "できるだけ自然な関西弁を使ってください。"
        "「〜や」「〜やで」「〜やねん」「せやな」「ほんま」などの"
        "関西弁特有の表現を使って、親しみやすく答えてください。"
    )
    
    HAKATA = (
        "これからの質問には全て博多弁で答えてください。"
        "「〜ばい」「〜たい」「〜と？」「〜やけん」などの"
        "博多弁特有の表現を使ってください。"
    )
    
    STANDARD = (
        "丁寧で分かりやすい標準語で答えてください。"
    )
    
    FRIENDLY = (
        "友達に話すようなカジュアルな口調で答えてください。"
    )
    
    PROFESSIONAL = (
        "ビジネスシーンにふさわしい、"
        "丁寧で専門的な口調で答えてください。"
    )
    
    @classmethod
    def get_all_presets(cls) -> Dict[str, str]:
        """全プリセットを取得"""
        return {
            "関西弁": cls.KANSAI,
            "博多弁": cls.HAKATA,
            "標準語": cls.STANDARD,
            "カジュアル": cls.FRIENDLY,
            "ビジネス": cls.PROFESSIONAL,
        }
```

**UI統合**:
- サイドバーにプリセット選択ドロップダウン
- 選択したプリセットの適用
- カスタムプロンプトの入力機能

**影響範囲**:
- `src/config.py`: プリセットクラスの追加
- `src/ui/components.py`: プリセット選択UI
- `src/session_manager.py`: 選択されたプリセットの管理

**見積もり**: 3-4時間

---

#### 5. API使用量のトラッキング

**目的**: コスト管理とモニタリング

**実装内容**:
```python
# 新規ファイル: src/usage_tracker.py

from typing import Dict, List
from datetime import datetime
import json
from pathlib import Path

class UsageTracker:
    """API使用量のトラッキング"""
    
    def __init__(self, storage_path: str = ".usage_stats.json"):
        self.storage_path = Path(storage_path)
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """統計データを読み込み"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"sessions": [], "total_tokens": 0}
    
    def _save_stats(self) -> None:
        """統計データを保存"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def track_request(
        self, 
        input_tokens: int, 
        output_tokens: int,
        model: str,
        duration: float
    ) -> None:
        """APIリクエストを記録"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "model": model,
            "duration_seconds": duration,
        }
        
        if "sessions" not in self.stats:
            self.stats["sessions"] = []
        
        self.stats["sessions"].append(entry)
        self.stats["total_tokens"] = self.stats.get("total_tokens", 0) + entry["total_tokens"]
        self._save_stats()
    
    def get_total_usage(self) -> Dict:
        """合計使用量を取得"""
        return {
            "total_requests": len(self.stats.get("sessions", [])),
            "total_tokens": self.stats.get("total_tokens", 0),
        }
    
    def get_usage_by_date(self) -> Dict[str, int]:
        """日付別の使用量を取得"""
        usage_by_date = {}
        for session in self.stats.get("sessions", []):
            date = session["timestamp"].split("T")[0]
            usage_by_date[date] = usage_by_date.get(date, 0) + session["total_tokens"]
        return usage_by_date
```

**UI統合**:
- サイドバーに使用量統計の表示
- 日別/月別の使用量グラフ
- コスト概算の表示

**影響範囲**:
- `src/usage_tracker.py`: 新規作成
- `src/api_client.py`: トラッキングの統合
- `src/ui/components.py`: 統計表示UI
- `tests/test_usage_tracker.py`: 新規作成

**見積もり**: 4-5時間

---

#### 6. モデル切り替え機能

**目的**: 用途に応じたモデルの選択

**実装内容**:
```python
# src/config.py の拡張

class ModelConfig:
    """利用可能なモデルの定義"""
    
    MODELS = {
        "claude-3-5-sonnet-20241022": {
            "name": "Claude 3.5 Sonnet (最新)",
            "description": "最も高性能なモデル",
            "max_tokens": 8192,
        },
        "claude-3-5-haiku-20241022": {
            "name": "Claude 3.5 Haiku",
            "description": "高速で経済的",
            "max_tokens": 8192,
        },
        "claude-3-opus-20240229": {
            "name": "Claude 3 Opus",
            "description": "最高品質（高コスト）",
            "max_tokens": 4096,
        },
    }
    
    @classmethod
    def get_model_options(cls) -> List[str]:
        """選択可能なモデルのリストを取得"""
        return list(cls.MODELS.keys())
    
    @classmethod
    def get_model_info(cls, model_name: str) -> Dict:
        """モデルの情報を取得"""
        return cls.MODELS.get(model_name, {})
```

**UI統合**:
- サイドバーにモデル選択ドロップダウン
- モデル情報の表示
- 選択したモデルでのAPI呼び出し

**影響範囲**:
- `src/config.py`: モデル設定の追加
- `src/ui/components.py`: モデル選択UI
- `src/session_manager.py`: モデル選択の管理
- `app.py`: 動的なモデル切り替え

**見積もり**: 2-3時間

---

### 🔧 優先度: 低（将来の拡張）

#### 7. マルチユーザー対応

**目的**: 複数ユーザーでの利用

**実装内容**:
- ユーザー認証機能
- ユーザー別のセッション管理
- ユーザー別の会話履歴
- 使用量制限

**見積もり**: 12-16時間

---

#### 8. プラグインシステム

**目的**: 機能の拡張性向上

**実装内容**:
- プラグインインターフェースの定義
- プラグインローダー
- サンプルプラグイン（画像生成、検索など）

**見積もり**: 10-12時間

---

#### 9. Web API化

**目的**: 外部からの利用

**実装内容**:
- FastAPIによるREST API
- 認証・認可
- APIドキュメント（OpenAPI）
- レート制限

**見積もり**: 16-20時間

---

## 🗓️ 実装スケジュール案

### Week 1-2: 基盤機能
- [ ] ストリーミング応答機能（優先度: 高）
- [ ] ロギング機能（優先度: 高）
- [ ] API使用量トラッキング（優先度: 中）

### Week 3-4: ユーザー体験向上
- [ ] 会話履歴の永続化（優先度: 高）
- [ ] 複数のシステムプロンプト（優先度: 中）
- [ ] モデル切り替え機能（優先度: 中）

### Week 5+: 高度な機能（必要に応じて）
- [ ] マルチユーザー対応（優先度: 低）
- [ ] プラグインシステム（優先度: 低）
- [ ] Web API化（優先度: 低）

---

## 📊 期待される改善効果

### パフォーマンス
- **ストリーミング応答**: 体感速度が50-70%改善
- **ロギング**: デバッグ時間が40%削減

### ユーザビリティ
- **会話の永続化**: ユーザー満足度が大幅に向上
- **プリセット**: 利用シーンが3-5倍に拡大
- **使用量トラッキング**: コスト意識の向上

### 保守性
- **ロギング**: 問題の早期発見と解決
- **モジュール化の深化**: 機能追加が容易に

---

## 🧪 テスト戦略

各機能について以下のテストを追加:

1. **ユニットテスト**
   - 各クラス・関数の動作検証
   - エッジケースのカバー

2. **統合テスト**
   - モジュール間の連携テスト
   - API呼び出しのモックテスト

3. **E2Eテスト**（将来的に）
   - Streamlit UIの自動テスト
   - シナリオベースのテスト

**目標カバレッジ**: 85%以上

---

## 📚 ドキュメント更新

- [ ] README.mdの更新（新機能の追加）
- [ ] 各モジュールのdocstring充実
- [ ] ユーザーガイドの作成
- [ ] API仕様書（Web API化時）
- [ ] CHANGELOG.mdの作成

---

## 🚨 リスクと対策

### リスク1: ストリーミング実装の複雑さ
**対策**: まずはシンプルな実装から始め、段階的に改善

### リスク2: ストレージ機能のパフォーマンス
**対策**: 大量の会話履歴がある場合の最適化を考慮（インデックス、圧縮）

### リスク3: API使用量の増加
**対策**: キャッシュ機能の検討、レート制限の実装

### リスク4: テストの保守コスト
**対策**: CIパイプラインの構築、テストの自動化

---

## 📈 成功指標（KPI）

- **コードカバレッジ**: 85%以上
- **応答時間**: 平均2秒以内（ストリーミング開始まで）
- **エラー率**: 1%以下
- **ユーザー満足度**: フィードバック収集とスコア化
- **保守性**: 新機能追加の所要時間削減

---

## 🎯 まとめ

Phase 2では、以下の3つの柱を中心に改善を進めます:

1. **ユーザー体験の向上** 
   - ストリーミング、永続化、プリセット

2. **運用性の向上**
   - ロギング、トラッキング、モニタリング

3. **拡張性の確保**
   - モジュール化の深化、プラグイン対応の準備

優先度の高い機能から順次実装し、各マイルストーンでレビューとフィードバックを行います。
