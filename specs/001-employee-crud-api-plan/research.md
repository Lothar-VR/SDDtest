# 技術調査: 社員情報CRUD API

**作成日**: 2026-04-02  
**ステータス**: 完了  
**対象**: FastAPI + SQLite による RESTful CRUD API の技術スタック検証

## 調査結果

### AR-001: FastAPI フレームワーク選定

**決定**: FastAPI 0.100.0 以上を採用

**根拠**:

- 自動的な OpenAPI/Swagger ドキュメント生成（憲法 I. API-ファースト設計に準拠）
- Pydantic による自動的なリクエスト/レスポンス検証（憲法 V. セキュリティ準拠）
- 非同期対応で高速（平均応答 200ms 目標を満たす容易性）
- Python エコシステムの充実（型チェック、テストツール連携）

**代替案検討**:

- Django REST Framework: 過度に機能豊富（本要件には不必要）
- Flask: 最小限だが、自動検証・ドキュメント機能が弱い

**結論**: FastAPI は要件と憲法の両立に最適。

---

### AR-002: ORM・データベースマッピング

**決定**: SQLAlchemy 2.0 + Alembic を採用

**根拠**:

- SQLAlchemy ORM で SQL インジェクション対策が容易（憲法 V. セキュリティ）
- Alembic で migration 管理（憲法 III. DB 設計の一貫性）
- 型ヒント対応で IDE 補完が良好
- SQLite → PostgreSQL への移行が容易（production 対応）

**制約**: 本バージョンは SQLite のみ。production では Alembic マイグレーション実行必須。

**結論**: SQLAlchemy + Alembic は企業レベルの堅牢性を確保。

---

### AR-003: テスト戦略

**決定**: pytest + pytest-cov を採用、テストカバレッジ 80% 以上維持

**根拠**:

- pytest は TDD ワークフローに最適（憲法 II.）
- pytest-cov で覆率測定・自動チェック機能
- fixture による テストデータ管理と再利用性
- 並列テスト実行で開発速度向上

**テスト構成**:

- **ユニットテスト**: models, schemas, services 層（各関数単位）
- **統合テスト**: API エンドポイント全体（DB + API 双方のシミュレーション）
- **E2E テスト**: 本API サーバー起動後の実機テスト（将来実装予定）

**結論**: pytest による三層テスト構築は憲法 II. TDD 準拠に必須。

---

### AR-004: 入力検証・スキーマ管理

**決定**: Pydantic v2 を採用

**根拠**:

- FastAPI との標準統合（自動検証＆ドキュメント生成）
- 複雑な検証ルールを宣言的に記述可能
- エラーメッセージの自動ローカライズ対応
- 型安全性の確保

**実装予定**:

- `schemas/employee.py` で EmployeeCreate, EmployeeRead, EmployeeUpdate を定義
- 必須フィールド検証：name, email, department（最小値・最大値は実装フェーズで検討）
- email フォーマット検証（Pydantic 組み込み）

**結論**: Pydantic は憲法 V. セキュリティ要求に最適合。

---

### AR-005: ログ・可観測性実装

**決定**: Python 標準 logging + 構造化ログライブラリ（python-json-logger または structlog）を検討

**根拠**:

- 憲法 IV. ログと可観測性に準拠
- 本フェーズでは基本的なログレベル（DEBUG, INFO, WARNING, ERROR）の実装
- JSON 形式ログで ELK/CloudWatch との連携を想定

**実装予定**:

- main.py で logging 設定
- 重要処理（CREATE/UPDATE/DELETE）は INFO レベルで記録
- エラーは ERROR レベルでスタックトレース含有
- トレース ID（uuid4）で複数リクエスト追跡対応

**結論**: 基本ログ実装は Phase 1 で完全統合。詳細設計は Phase 1 中に実施。

---

### AR-006: 認証・認可

**決定**: 本バージョンは認証機能未実装。内部 LAN 環境での使用を想定

**理由**:

- 仕様書（前提条件・制限事項）に明記：認証は本バージョンで未実装
- ユーザーは HR 部門の非技術者（社内アクセス前提）
- 将来バージョンで JWT または API キー追加予定

**結論**: 認証機能は Phase 2 以降で実装。本フェーズでは不要。

---

### AR-007: パフォーマンス最適化

**決定**: インデックス戦略を事前設計。キャッシング・ページングは将来機能

**根拠**:

- 目標：平均応答 200ms 以下、同時接続 100 ユーザー対応
- SQLite の単一テーブル（Employees）へのクエリは十分高速
- インデックス：email（UNIQUE）を必須、id（主キー）は自動インデックス
- ページング機能は要件外（データ量が増えれば Phase 2 で実装）

**結論**: L ホスペーアップインデックス設計は migration v001 で実装。ページングは将来機能。

---

## 未完了・検討中の項目

- [ ] ログライブラリの最終選定（structlog vs python-json-logger）：Phase 1 デザインレビューで決定
- [ ] CORS ポリシー：フロントエンド統合時に明記予定
- [ ] Rate Limiting：将来機能（本バージョン未実装）

## 次ステップ

1. **Phase 1 Design**: data-model.md で Employee エンティティ確定
2. **API Contracts**: OpenAPI スキーマ（contracts/ ）で インターフェース冷凍
3. **Quickstart**: 開発環境セットアップガイド作成

---

**作成者**: speckit.plan  
**レビュー**: 保留中 → Phase 1 以降で技術レビュー実施予定
