# API Contract: 社員情報 CRUD API

**バージョン**: 1.0  
**作成日**: 2026-04-02  
**ステータス**: 確定  
**フォーマット**: OpenAPI 3.0.3

## 概要

社員情報管理 REST API のインターフェース契約。 FastAPI による自動ドキュメント생成に対応。

## ベース URL

- **開発**: `http://localhost:8000`
- **本番**: `http://api.example.com`

## エンドポイント

### 1. 社員一覧取得

**端点**: `GET /employees`

**説明**: 登録されている全社員情報を取得（論理削除済みを除く）

**パラメータ**: なし

**レスポンス** (200 OK):

```json
{
  "items": [
    {
      "id": 1,
      "name": "田中太郎",
      "email": "taro@example.com",
      "department": "営業部",
      "is_deleted": false,
      "created_at": "2026-04-02T10:30:00Z",
      "updated_at": "2026-04-02T10:30:00Z"
    }
  ],
  "total": 1
}
```

**エラーレスポンス** (500 Internal Server Error):

```json
{
  "detail": "データベース接続エラー",
  "status_code": 500
}
```

---

### 2. 社員情報新規登録

**端点**: `POST /employees`

**説明**: 新しい社員情報を登録

**リクエストボディ**:

```json
{
  "name": "田中太郎",
  "email": "taro@example.com",
  "department": "営業部"
}
```

**リクエスト検証**:

- `name`: 必須、1-255 文字
- `email`: 必須、有効なメールアドレス形式、一意（削除済み除外）
- `department`: 必須、1-100 文字

**レスポンス** (201 Created):

```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "taro@example.com",
  "department": "営業部",
  "is_deleted": false,
  "created_at": "2026-04-02T10:30:00Z",
  "updated_at": "2026-04-02T10:30:00Z"
}
```

**エラーレスポンス** (400 Bad Request):

```json
{
  "detail": [
    {
      "field": "email",
      "message": "invalid email format"
    }
  ],
  "status_code": 400
}
```

**エラーレスポンス** (409 Conflict):

```json
{
  "detail": "このメールアドレスは既に登録されています",
  "status_code": 409
}
```

---

### 3. 社員情報取得（単体）

**端点**: `GET /employees/{id}`

**説明**: 指定した ID の社員情報を取得

**パスパラメータ**:

- `id` (integer, required): 社員ID

**レスポンス** (200 OK):

```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "taro@example.com",
  "department": "営業部",
  "is_deleted": false,
  "created_at": "2026-04-02T10:30:00Z",
  "updated_at": "2026-04-02T10:30:00Z"
}
```

**エラーレスポンス** (404 Not Found):

```json
{
  "detail": "社員が見つかりません",
  "status_code": 404
}
```

---

### 4. 社員情報更新（全項目）

**端点**: `PUT /employees/{id}`

**説明**: 指定した ID の社員情報をすべて置き換える（全項目必須）

**パスパラメータ**:

- `id` (integer, required): 社員ID

**リクエストボディ**:

```json
{
  "name": "田中太郎",
  "email": "taro@example.com",
  "department": "営業部"
}
```

**リクエスト検証**: POST と同一

**レスポンス** (200 OK):

```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "taro@example.com",
  "department": "営業部",
  "is_deleted": false,
  "created_at": "2026-04-02T10:30:00Z",
  "updated_at": "2026-04-02T10:35:00Z"
}
```

**エラーレスポンス** (404 Not Found, 400 Bad Request, 409 Conflict): DELETE と同一

---

### 5. 社員情報更新（部分）

**端点**: `PATCH /employees/{id}`

**説明**: 指定した ID の社員情報の一部を更新（変更フィールドのみ指定）

**パスパラメータ**:

- `id` (integer, required): 社員ID

**リクエストボディ** (例：名前のみ変更):

```json
{
  "name": "田中次郎"
}
```

**リクエスト検証**: 指定されたフィールドのみ検証。未指定はスキップ。

**レスポンス** (200 OK):

```json
{
  "id": 1,
  "name": "田中次郎",
  "email": "taro@example.com",
  "department": "営業部",
  "is_deleted": false,
  "created_at": "2026-04-02T10:30:00Z",
  "updated_at": "2026-04-02T10:40:00Z"
}
```

---

### 6. 社員情報削除（論理削除）

**端点**: `DELETE /employees/{id}`

**説明**: 指定した ID の社員情報を削除（DB から完全削除せず、is_deleted フラグを true に設定）

**パスパラメータ**:

- `id` (integer, required): 社員ID

**レスポンス** (204 No Content): 本文なし

**エラーレスポンス** (404 Not Found):

```json
{
  "detail": "社員が見つかりません",
  "status_code": 404
}
```

---

## HTTP ステータスコード一覧

| コード | 説明                                   | エンドポイント                  |
| ------ | -------------------------------------- | ------------------------------- |
| 200    | OK - リクエスト成功                    | GET（単体）、PUT、PATCH         |
| 201    | Created - リソース作成成功             | POST                            |
| 204    | No Content - 削除成功                  | DELETE                          |
| 400    | Bad Request - 検証エラー               | POST、PUT、PATCH                |
| 404    | Not Found - リソース不存在             | GET（単体）、PUT、PATCH、DELETE |
| 409    | Conflict - メールアドレス重複          | POST、PUT、PATCH                |
| 500    | Internal Server Error - サーバーエラー | すべて                          |

---

## エラーハンドリング

### 標準エラー応答形式

```json
{
  "detail": "エラーメッセージ",
  "status_code": 400
}
```

### 検証エラー詳細

```json
{
  "detail": [
    {
      "field": "フィールド名",
      "message": "エラーメッセージ"
    }
  ],
  "status_code": 400
}
```

---

## ビジネスルール

### メールアドレス一意性

- 各メールアドレスは全体で一意（削除済み社員を除く）
- 削除済み社員のメールは新規登録で再利用可能

### 論理削除

- DELETE エンドポイントで `is_deleted = true` に設定
- GET エンドポイントは削除済みを自動フィルタリング（where is_deleted = false）
- 復元機能なし

### 並行更新時の挙動

- Last-Write-Wins パターン（競合チェックなし）
- 複数リクエストが同時に同じリソースを更新→最後の書き込みが優先

---

## 対応フォーマット

- **Content-Type**: `application/json`
- **Character Encoding**: UTF-8
- **Timestamp Format**: ISO 8601 (RFC 3339): `2026-04-02T10:30:00Z`

---

## 次ステップ

1. **Swagger UI**: FastAPI による自動ドキュメント (`/docs`)
2. **実装検証**: contracts/ のスキーマで実装テスト
3. **クライアント統合**: フロントエンド連携テスト

---

**契約検証**: ✓ 憲法 I. API-ファースト設計準拠確認  
**セキュリティ確認**: ✓ 入力検証・エラー情報開示レベル確認（内部詳細は非開示）
