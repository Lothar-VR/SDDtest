# データモデル設計: 社員情報CRUD API

**作成日**: 2026-04-02  
**バージョン**: 1.0  
**ステータス**: 確定  
**対応仕様**: [spec.md](../001-employee-crud-api/spec.md#重要な実体)

## ER 図

```
┌─────────────────────────────────┐
│         Employees               │
├─────────────────────────────────┤
│ PK  id: INTEGER (auto)          │
│ UK  email: VARCHAR(255)         │
│ --- name: VARCHAR(255)          │
│ --- department: VARCHAR(100)    │
│ --- is_deleted: BOOLEAN         │
│ --- created_at: TIMESTAMP       │
│ --- updated_at: TIMESTAMP       │
└─────────────────────────────────┘
```

**制約**:

- `id`: 主キー、自動採番、正の整数
- `email`: 一意制約（UNIQUE）、削除済みを除外（is_deleted = false のみ）
- `name`, `department`: NOT NULL
- `is_deleted`: NOT NULL、デフォルト False（論理削除用）
- `created_at`, `updated_at`: タイムスタンプ、自動設定

---

## エンティティ定義

### Employee（社員情報）

#### 属性

| 属性         | 型           | 制約                                | 説明           |
| ------------ | ------------ | ----------------------------------- | -------------- |
| `id`         | INTEGER      | PK, AUTO_INCREMENT                  | 社員識別子     |
| `name`       | VARCHAR(255) | NOT NULL                            | 社員名         |
| `email`      | VARCHAR(255) | NOT NULL, UNIQUE（削除済み除外）    | メールアドレス |
| `department` | VARCHAR(100) | NOT NULL                            | 部門・チーム   |
| `is_deleted` | BOOLEAN      | NOT NULL, DEFAULT FALSE             | 論理削除フラグ |
| `created_at` | TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 登録日時       |
| `updated_at` | TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 更新日時       |

#### バリデーション規則

```python
# name
- 必須（最小 1 文字）
- 最大 255 文字
- 先頭・末尾の空白は許可（業務判断で担当者が削除）

# email
- 必須
- RFC 5322 形式（Pydantic EmailStr で検証）
- 最大 255 文字
- 小文件で保存、検索時は大文字小文字区別なし

# department
- 必須（最小 1 文字）
- 最大 100 文字
- テキスト入力（ドロップダウンリストは将来機能）

# is_deleted
- デフォルト: False
- 削除時のみ True（ハードデリート禁止、論理削除必須）
```

#### ステート遷移

```
┌──────────┐
│  Active  │ ← 初期状態 (is_deleted = false)
└────┬─────┘
     │
     │ DELETE /employees/{id}
     ↓
┌──────────┐
│ Deleted  │ ← 最終状態 (is_deleted = true)
└──────────┘
※ 復元機能なし（実装予定なし）
```

---

## SQLite スキーマ

### 初期マイグレーション (v001)

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    department VARCHAR(100) NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- email の UNIQUE 制約は削除済みを除外
-- SQLite での部分インデックス：
CREATE UNIQUE INDEX idx_email_not_deleted
ON employees(email)
WHERE is_deleted = 0;

-- クエリ高速化用インデックス
CREATE INDEX idx_created_at ON employees(created_at);
CREATE INDEX idx_is_deleted ON employees(is_deleted);
```

### インデックス戦略

| インデックス    | 理由                 | 削除フィルター |
| --------------- | -------------------- | -------------- |
| PRIMARY（id）   | 自動 (PK)            | N/A            |
| UNIQUE（email） | 重複チェック用       | is_deleted = 0 |
| idx_created_at  | ソート・フィルター用 | なし           |
| idx_is_deleted  | GET 時フィルター用   | 必須           |

---

## Pydantic スキーマ

### リクエスト/レスポンスモデル

```python
# リクエスト: 新規登録
class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=100)

# リクエスト: 更新（全項目）
class EmployeeUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=100)

# リクエスト: 部分更新
class EmployeePatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=1, max_length=100)

# レスポンス: 単体
class EmployeeRead(BaseModel):
    id: int
    name: str
    email: str
    department: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# レスポンス: リスト
class EmployeeList(BaseModel):
    items: List[EmployeeRead]
    total: int
```

---

## 関連規則・制約

### 一意性制約

- **email**: is_deleted = false の社員のみ一意。削除済みと同じ email で新規登録可能。

### 削除戦略

- **論理削除（ソフトデリート）**: DB から物理削除せず、is_deleted = true に設定
- **GET エンドポイント**: 削除済み社員は返却しない（WHERE is_deleted = false）
- **復元機能**: 本バージョンで未実装

### パフォーマンス

- **クエリ時間目標**: 平均 200ms 以下
- **同時接続**: 100 ユーザー対応可能（SQLite + Alembic で対応）
- **ページング**: 将来機能（本バージョン未実装）

---

## マイグレーション計画

### v001: 初期テーブル作成

```
DOWN: DROP TABLE employees;
UP:   CREATE TABLE employees (...)
      CREATE UNIQUE INDEX idx_email_not_deleted ...
      CREATE INDEX idx_created_at, idx_is_deleted ...
```

### 将来版（参考）

- v002: ページング/検索機能テーブル追加（予定なし）
- v003: 監査ログテーブル追加（予定なし）

---

## 設計決定ログ

| 決定           | 理由                 | 代替案（検討済み）              |
| -------------- | -------------------- | ------------------------------- |
| 論理削除採用   | 監査・復元対応の準備 | 物理削除：回復不可能            |
| email 一意制約 | ユーザー重複防止     | なし（要件必須）                |
| SQLite 採用    | 開発・テスト機速性   | PostgreSQL：production 移行可能 |
| Alembic管理    | migration 自動化     | 手動 SQL：エラーリスク高い      |

---

## 次ステップ

1. **Contract 検証**: contracts/ の OpenAPI スキーマで API インターフェース確定
2. **Quickstart 作成**: 開発環境セットアップガイド
3. **実装フェーズ**: TDD サイクル開始（models.py → services.py → api.py）

---

**データモデル検証**: ✓ 憲法 III. DB 設計準拠確認  
**セキュリティ確認**: ✓ 憲法 V. SQL インジェクション対策（パラメータ化）
