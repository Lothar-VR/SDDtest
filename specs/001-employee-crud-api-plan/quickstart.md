# クイックスタート: 社員情報CRUD API 開発環境構築

**対象**: 開発チームメンバー  
**所要時間**: 約 15 分（初回セットアップ）  
**前提条件**: Python 3.10+、pip、git  
**最終更新**: 2026-04-02

---

## 1. リポジトリクローン＆ブランチ切り替え

```bash
# リポジトリクローン（初回のみ）
git clone <repository-url>
cd SSDtest

# 機能ブランチに切り替え
git checkout 001-employee-crud-api-plan
git pull origin 001-employee-crud-api-plan
```

---

## 2. Python 仮想環境構築

### on macOS / Linux

```bash
# 仮想環境作成
python3 -m venv venv

# 仮想環境有効化
source venv/bin/activate
```

### on Windows

```bash
# 仮想環境作成
python -m venv venv

# 仮想環境有効化
venv\Scripts\activate
```

---

## 3. 依存パッケージ インストール

```bash
# pip 最新化
pip install --upgrade pip

# 依存パッケージ一括インストール
pip install -r requirements.txt

# 開発用・テスト用パッケージもインストール
pip install -r requirements-dev.txt  # テスト、Lint ツール含む
```

### 主要パッケージ一覧

| パッケージ    | バージョン | 用途                      |
| ------------- | ---------- | ------------------------- |
| FastAPI       | ≥0.100.0   | Web フレームワーク        |
| uvicorn       | ≥0.23.0    | ASGI サーバー             |
| SQLAlchemy    | ≥2.0.0     | ORM                       |
| alembic       | ≥1.10.0    | DB migration 管理         |
| pydantic      | ≥2.0.0     | リクエスト/レスポンス検証 |
| pytest        | ≥7.0.0     | テストランナー            |
| pytest-cov    | ≥4.0.0     | カバレッジ測定            |
| python-dotenv | ≥1.0.0     | 環境変数ロード            |

---

## 4. 環境設定

### .env ファイル作成

```bash
# テンプレートからコピー
cp .env.example .env
```

### .env 内容（例）

```env
DATABASE_URL=sqlite:///./employees.db
DEBUG=True
LOG_LEVEL=DEBUG
```

---

## 5. データベース初期化

### Alembic migration 実行

```bash
# migration フォルダに移動
cd migrations

# 最新版の migration スキーマを適用
alembic upgrade head

# リポジトリルートに戻る
cd ..
```

**実行後**: `employees.db` が生成されます（SQLite ファイル）。

### migration 確認

```bash
# 現在の migration バージョン確認
alembic current
```

---

## 6. FastAPI サーバー起動

```bash
# ローカル開発サーバー起動
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**出力例**:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### サーバーへのアクセス

- **API**: http://localhost:8000
- **Swagger UI（ドキュメント）**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 7. テスト実行

### ユニット＆統合テスト実施

```bash
# すべてのテスト実行
pytest

# テストカバレッジ測定（80% 以上が目標）
pytest --cov=src tests/

# 詳細出力
pytest -v --cov=src --cov-report=html tests/
```

### カバレッジレポート出力

```bash
# HTML レポート生成（htmlcov/index.html）
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html  # macOS / Linux
```

---

## 8. コード品質チェック

### Flake8（コード行儀チェック）

```bash
# Flake8 実行
flake8 src/ tests/

# 検出例とフラグ
# E501: line too long
# W503: line break before binary operator
# F401: unused import
```

### Black（自動フォーマッタ）

```bash
# コードを自動整形
black src/ tests/
```

---

## 9. 開発ワークフロー (TDD)

### ステップ 1: テスト作成

```bash
# tests/unit/test_<module>.py で実装予定の関数をテスト
# 例: POST /employees のテスト
cat > tests/integration/test_employee_api.py << 'EOF'
def test_create_employee(client):
    response = client.post("/employees", json={
        "name": "田中太郎",
        "email": "taro@example.com",
        "department": "営業部"
    })
    assert response.status_code == 201
    assert response.json()["id"] is not None
EOF
```

### ステップ 2: テスト実行（失敗を確認）

```bash
pytest tests/integration/test_employee_api.py::test_create_employee -v
# 結果: FAILED ✗（実装がないため）
```

### ステップ 3: 実装

```python
# src/api/employees.py
from fastapi import APIRouter, status
from src.schemas.employee import EmployeeCreate, EmployeeRead

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db):
    # ビジネスロジック実装
    pass
```

### ステップ 4: テスト実行（合格を確認）

```bash
pytest tests/integration/test_employee_api.py::test_create_employee -v
# 結果: PASSED ✓
```

---

## 10. Git ワークフロー

### コミット前チェックリスト

```bash
# テスト全合格確認
pytest --cov=src tests/

# Flake8 チェック
flake8 src/

# 変更ファイル確認
git status

# ステージング
git add src/ tests/

# コミット（コミットメッセージはイシューハッシュ + 簡潔な説明）
git commit -m "FR-001: Implement POST /employees endpoint"

# リモートプッシュ
git push origin 001-employee-crud-api-plan
```

### Pull Request 作成

1. GitHub（またはホスト リポジトリ）にアクセス
2. "Create Pull Request" ボタン押下
3. **Title**: `[FR-001] POST /employees endpoint`
4. **Description**:
   ```
   - 新規登録 API 実装
   - ユニットテスト 5 件追加
   - テストカバレッジ: 87%
   - Flake8 チェック合格
   ```
5. レビュアー割り当て＆承認待ち
6. 承認後 → main ブランチにマージ

---

## 11. 便利なコマンド集

```bash
# 仮想環境有効化（毎回セッション開始時）
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate      # Windows

# サーバー起動（開発モード・自動リロード）
uvicorn src.main:app --reload

# サーバー起動（本番モード）
uvicorn src.main:app --host 0.0.0.0 --port 8000

# テスト実行（簡潔表示）
pytest

# テスト実行（詳細 + カバレッジ）
pytest -v --cov=src tests/

# データベース初期化リセット
rm employees.db && alembic downgrade base && alembic upgrade head

# 新しい migration 作成
alembic revision --autogenerate -m "Migration description"

# コード自動整形
black src/ tests/

# コード品質チェック
flake8 src/

# 仮想環境から抜ける
deactivate
```

---

## 12. トラブルシューティング

### エラー: `ModuleNotFoundError: No module named 'fastapi'`

```bash
# 仮想環境が有効になっていることを確認
which python  # macOS/Linux → venv パスが表示されるべき

# 再度インストール
pip install -r requirements.txt
```

### エラー: `sqlite3.OperationalError: database is locked`

```bash
# SQLite ファイルがロック状態
# サーバー＆テストをすべて停止してから再試行
rm employees.db
alembic upgrade head
```

### エラー: `ImportError: cannot import name 'EmployeeRead' from 'src.schemas.employee'`

```bash
# スキーマファイルが存在しないか名前が異なる
# src/schemas/employee.py の定義を確認
ls -la src/schemas/
```

### エラー: テストカバレッジが 80% に満たない

```bash
# カバレッジレポート生成して確認
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html  # macOS/Linux

# 不足しているテストケースを追加
# テストを追加後、再度カバレッジ測定
```

---

## 13. 参考リソース

- [FastAPI 公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM チュートリアル](https://docs.sqlalchemy.org/en/20/orm/)
- [Alembic マイグレーション概要](https://alembic.sqlalchemy.org/)
- [Pytest 公式ドキュメント](https://docs.pytest.org/)
- [プロジェクト仕様書](../001-employee-crud-api/spec.md)
- [API コントラクト](./contracts/README.md)
- [データモデル設計](./data-model.md)

---

## 14. よくある質問

### Q: 複数のメンバーで同時開発する場合、どのように調整する？

**A**: 各メンバーが異なる機能ブランチで開発後、PR を通じて main にマージしてください。

- メンバー A: `feature/FR-001-create` (POST /employees)
- メンバー B: `feature/FR-002-list` (GET /employees)
- メンバー C: `feature/FR-003-get` (GET /employees/{id})

### Q: DB スキーマを変更したい場合は？

**A**: Alembic migration で管理してください。直接 SQL やファイル編集は避けてください。

```bash
# 新しい migration 作成
alembic revision --autogenerate -m "Add column to employees"

# UP/DOWN スクリプト確認＆編集
vim migrations/versions/XXX_add_column_to_employees.py

# 適用
alembic upgrade head
```

### Q: テストが失敗する場合は？

**A**: 以下の順序で診断してください。

1. エラーメッセージを詳しく読む
2. `pytest -v` で詳細出力
3. テストとソースコードを見比べる
4. print デバッグ /(pytest -s で print 出力有効化)

---

## 次ステップ

1. **タスク生成**: `/speckit.tasks` コマンドで実装タスク一覧生成
2. **タスク割り当て**: チームメンバーにタスクを割り当て
3. **並列開発開始**: 各メンバーが TDD サイクルで実装

---

**作成日**: 2026-04-02  
**最後の更新**: 2026-04-02  
**メンテナ**: 開発チーム
