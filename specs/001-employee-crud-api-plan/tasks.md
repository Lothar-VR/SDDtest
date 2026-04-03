# タスク: 社員情報CRUD API

**入力**: 機能設計ドキュメント `/specs/001-employee-crud-api-plan/`  
**前提条件**: plan.md (✓)、spec.md (✓)、data-model.md (✓)、research.md (✓)、contracts/ (✓)  
**テスト**: TDD 必須（spec.md より）。各ユーザーストーリーのテストを先行実装  
**組織**: ユーザーストーリごとにグループ化。最後に削除されたデータの一覧エンドポイント対応  
**スコープ**: MVP = US1 + US2（P1 機能）。P2・P3 は後続フェーズ

## 形式: `[ID] [P?] [Story?] 説明`

- **[P]**: 並列実行可能（異なるファイル、依存なし）
- **[Story]**: 所属ユーザーストーリ（US1, US2, US3, US4）
- **ファイルパス**: src/、tests/ はリポジトリルート配下

---

## フェーズ 1: セットアップ (共有インフラ)

**目的**: プロジェクト初期化と基本構造構築

- [x] T001 実装計画に従ってプロジェクト構造を作成 (requirements.txt, src/, tests/, migrations/ ディレクトリ)
- [x] T002 [P] requirements.txt に FastAPI (≥0.100.0)、uvicorn、SQLAlchemy、Alembic、Pydantic、pytest、pytest-cov、python-dotenv を追加
- [x] T003 [P] 仮想環境を作成し、pip install -r requirements.txt でパッケージをインストール
- [x] T004 [P] .env.example テンプレートを作成 (DATABASE_URL, DEBUG, LOG_LEVEL)
- [x] T005 [P] Flake8 と Black を設定用のファイル (.flake8, pyproject.toml) で構成

---

## フェーズ 2: 基盤 (全ストーリーをブロック)

**目的**: すべてのユーザーストーリー実装前に完了する必須インフラ

**⚠️ 重要**: このフェーズ完了まで、ユーザーストーリー実装は開始できません

✅ **フェーズ 2 完了** - ユーザーストーリー実装が開始可能

- [x] T006 src/config.py で DATABASE_URL、DEBUG、LOG_LEVEL を読み込む環境設定を実装
- [x] T007 [P] src/database.py で SQLAlchemy エンジン、セッションメーカー、Base を定義
- [x] T008 [P] src/schemas/employee.py で EmployeeCreate (name, email, department)、EmployeeRead (全フィールド含む)、EmployeeUpdate (全フィールドオプション) の Pydantic スキーマを定義
- [x] T009 src/models/employee.py で SQLAlchemy ORM モデルを定義（id, name, email, department, is_deleted, created_at, updated_at、email 一意制約）
- [x] T010 migrations/alembic.ini と migrations/env.py を設定（SQLite、AutoMap 対応）
- [x] T011 migrations/versions/001_create_employees_table.py で初期マイグレーション (CREATE TABLE employees) を作成
- [x] T012 [P] src/main.py で FastAPI アプリケーションインスタンスを作成、Swagger/OpenAPI ドキュメント有効化
- [x] T013 [P] src/api/employees.py で APIRouter を定義し、main.py に include_router
- [x] T014 src/utils/logging_config.py で構造化ログ設定を実装 (DEBUG, INFO, WARNING, ERROR, CRITICAL レベル)
- [x] T015 [P] src/utils/error_handlers.py で共通エラーハンドリング (400, 404, 409, 500) と統一エラーレスポンス形式を実装

**チェックポイント**: 基盤準備完了 - ユーザーストーリー実装が開始可能

---

## フェーズ 3: ユーザーストーリ 1 - 社員情報を新規登録する (優先順位: P1) 🎯 MVP

**目標**: HR部門が POST /employees で新社員を登録でき、id を含む登録データが 201 Created で返される

**独立テスト**: API 呼び出しのみで完全にテスト可能。既存データ依存なし

### ユーザーストーリ 1 のテスト (TDD 必須)

> **注記**: テストを先行実装し、失敗を確認してから実装を進める

- [ ] T016 [P] [US1] tests/contract/test_employee_create.py で POST /employees のコントラクトテスト実装 (正常系: 201 Created, name/email/department 必須確認, id 自動採番確認)
- [ ] T017 [P] [US1] tests/contract/test_employee_create_errors.py で POST /employees のエラーテスト (400 Bad Request: 必須フィールド欠落, 409 Conflict: 重複メール, 422 Unprocessable Entity: 形式エラー)
- [ ] T018 [P] [US1] tests/integration/test_employee_create_integration.py で POST /employees の統合テスト (DB への実際の書き込み確認、トランザクション)

### ユーザーストーリ 1 の実装

- [ ] T019 [US1] src/services/employee_service.py で EmployeeService クラスを実装、create_employee(name, email, department) メソッドを定義 (一意制約チェック、自動タイムスタンプ設定)
- [ ] T020 [US1] tests/unit/test_employee_service_create.py で create_employee のユニットテスト実装 (正常系、一意エラー処理)
- [ ] T021 [US1] src/api/employees.py で POST /employees エンドポイント実装 (EmployeeCreate スキーマ受け取り、EmployeeService.create_employee 呼び出し、201 Created + EmployeeRead レスポンス)
- [ ] T022 [US1] src/api/employees.py の POST /employees エンドポイントに入力検証エラー処理を追加 (400, 409 ステータスコード、error_handlers 使用)
- [ ] T023 [US1] src/api/employees.py の POST /employees エンドポイントにログを追加 (INFO: 登録成功、ERROR: 一意エラー/DB エラー)

**チェックポイント**: ユーザーストーリ 1 が独立して完全に機能・テスト可能

---

## フェーズ 4: ユーザーストーリ 2 - 社員一覧と個別情報を取得する (優先順位: P1) 🎯 MVP

**目標**: HR部門が GET /employees で全社員一覧 (is_deleted=false のみ) と GET /employees/{id} で特定社員を取得できる

**独立テスト**: テストデータセットアップで完全に独立テスト可能。US1 実装完了後に実行

### ユーザーストーリ 2 のテスト (TDD 必須)

- [ ] T024 [P] [US2] tests/contract/test_employee_list.py で GET /employees のコントラクトテスト (正常系: 200 OK, 社員配列返却, is_deleted=false フィルタリング確認)
- [ ] T025 [P] [US2] tests/contract/test_employee_get.py で GET /employees/{id} のコントラクトテスト (正常系: 200 OK, 単一社員返却、404 Not Found: 存在しない id)
- [ ] T026 [P] [US2] tests/integration/test_employee_list_integration.py で GET /employees の統合テスト (複数社員の一覧、is_deleted=true は除外、created_at 順序確認)
- [ ] T027 [P] [US2] tests/integration/test_employee_get_integration.py で GET /employees/{id} の統合テスト (特定社員取得、削除済み社員は 404)

### ユーザーストーリ 2 の実装

- [ ] T028 [P] [US2] src/services/employee_service.py に get_all_employees() メソッドを追加 (is_deleted=false フィルタリング、全件返却)
- [ ] T029 [P] [US2] src/services/employee_service.py に get_employee_by_id(id: int) メソッドを追加 (id で検索、is_deleted=false、None 時は呼び元で 404 処理)
- [ ] T030 [P] [US2] tests/unit/test_employee_service_get.py で get_all_employees、get_employee_by_id のユニットテスト実装
- [ ] T031 [US2] src/api/employees.py で GET /employees エンドポイント実装 (EmployeeService.get_all_employees 呼び出し、{items: [...], total: N} レスポンス形式, 200 OK)
- [ ] T032 [US2] src/api/employees.py で GET /employees/{id} エンドポイント実装 (EmployeeService.get_employee_by_id 呼び出し、404 or 200 OK + EmployeeRead)
- [ ] T033 [US2] src/api/employees.py の GET エンドポイントにエラー処理を追加 (500 Internal Server Error: DB 接続失敗)
- [ ] T034 [US2] src/api/employees.py の GET エンドポイントにログを追加 (INFO: 取得成功、ERROR: DB エラー)

**チェックポイント**: ユーザーストーリ 1 と 2 が両方とも独立して完全に機能

---

## フェーズ 5: ユーザーストーリ 3 - 社員情報を更新する (優先順位: P2)

**目標**: HR部門が PUT /employees/{id} (全更新) 、PATCH /employees/{id} (部分更新) で社員情報を変更できる

**独立テスト**: 更新対象の社員がテストデータとして存在する場合、独立してテスト可能

### ユーザーストーリ 3 のテスト (TDD 必須)

- [ ] T035 [P] [US3] tests/contract/test_employee_update_put.py で PUT /employees/{id} のコントラクトテスト (正常系: 200 OK, name/email/department 全更新、404 Not Found)
- [ ] T036 [P] [US3] tests/contract/test_employee_update_patch.py で PATCH /employees/{id} のコントラクトテスト (正常系: 200 OK, 指定フィールドのみ更新、404, 409 Conflict: 重複メール)
- [ ] T037 [P] [US3] tests/integration/test_employee_update_put_integration.py で PUT /employees/{id} の統合テスト (DB への更新確認、updated_at タイムスタンプ更新確認、Last-Write-Wins パターン)
- [ ] T038 [P] [US3] tests/integration/test_employee_update_patch_integration.py で PATCH /employees/{id} の統合テスト (部分更新、指定されないフィールドは変更なし)

### ユーザーストーリ 3 の実装

- [ ] T039 [P] [US3] src/schemas/employee.py に EmployeeUpdateFull と EmployeeUpdatePartial スキーマを定義 (EmployeeUpdateFull: name/email/department 必須、EmployeeUpdatePartial: 全フィールドオプション)
- [ ] T040 [P] [US3] src/services/employee_service.py に update_employee(id: int, email_changed: bool, \*\*kwargs) メソッドを追加 (全更新、一意制約チェック、updated_at 自動更新)
- [ ] T041 [P] [US3] src/services/employee_service.py に patch_employee(id: int, \*\*kwargs) メソッドを追加 (部分更新、指定フィールドのみ)
- [ ] T042 [P] [US3] tests/unit/test_employee_service_update.py で update_employee、patch_employee のユニットテスト実装
- [ ] T043 [US3] src/api/employees.py で PUT /employees/{id} エンドポイント実装 (EmployeeUpdateFull スキーマ受け取り、EmployeeService.update_employee 呼び出し、200 OK + EmployeeRead)
- [ ] T044 [US3] src/api/employees.py で PATCH /employees/{id} エンドポイント実装 (EmployeeUpdatePartial スキーマ受け取り、EmployeeService.patch_employee 呼び出し、200 OK + EmployeeRead)
- [ ] T045 [US3] src/api/employees.py の PUT/PATCH エンドポイントにエラー処理を追加 (400, 404, 409 ステータスコード)
- [ ] T046 [US3] src/api/employees.py の PUT/PATCH エンドポイントにログを追加 (INFO: 更新成功、ERROR: エラー)

**チェックポイント**: ユーザーストーリ 1・2・3 が すべて独立して完全に機能

---

## フェーズ 6: ユーザーストーリ 4 - 社員情報を削除する (優先順位: P3)

**目標**: HR部門が DELETE /employees/{id} で退職社員を論理削除（is_deleted=true）できる。削除済み社員は一覧・個別取得から除外

**独立テスト**: 削除対象の社員がテストデータとして存在する場合、独立してテスト可能

### ユーザーストーリ 4 のテスト (TDD 必須)

- [ ] T047 [P] [US4] tests/contract/test_employee_delete.py で DELETE /employees/{id} のコントラクトテスト (正常系: 204 No Content、404 Not Found)
- [ ] T048 [P] [US4] tests/contract/test_employee_delete_verify.py で DELETE 後の GET による削除確認テスト (削除後、GET /employees/{id} で 404、GET /employees で除外)
- [ ] T049 [P] [US4] tests/integration/test_employee_delete_integration.py で DELETE /employees/{id} の統合テスト (DB の is_deleted=true 確認、論理削除実装確認)

### ユーザーストーリ 4 の実装

- [ ] T050 [US4] src/services/employee_service.py に delete_employee(id: int) メソッドを追加 (is_deleted=true に設定、updated_at 自動更新、404 時は例外)
- [ ] T051 [US4] tests/unit/test_employee_service_delete.py で delete_employee のユニットテスト実装
- [ ] T052 [US4] src/api/employees.py で DELETE /employees/{id} エンドポイント実装 (EmployeeService.delete_employee 呼び出し、204 No Content または 404 Not Found)
- [ ] T053 [US4] src/api/employees.py の DELETE エンドポイントにエラー処理を追加 (404, 500 ステータスコード)
- [ ] T054 [US4] src/api/employees.py の DELETE エンドポイントにログを追加 (INFO: 削除成功、ERROR: エラー)

**チェックポイント**: すべてのユーザーストーリが独立して完全に機能・テスト・削除対応

---

## フェーズ 7: ポーランド & クロスカッティング

**目的**: コード品質向上、ドキュメント完成

- [ ] T055 [P] pytest を実行し、全テストが合格することを確認 (tests/unit, tests/contract, tests/integration)
- [ ] T056 pytest-cov で テストカバレッジ測定、80% 以上達成を確認 (coverage report: tests/coverage/)
- [ ] T057 [P] Flake8 で コード品質チェック実施、E501（行長）を除外して合格を確認
- [ ] T058 [P] Black で コード自動フォーマット実施
- [ ] T059 src に conftest.py を作成、pytest fixture (db_session, client など) を集約
- [ ] T060 README.md を作成 (プロジェクト概要、セットアップ手順、API ドキュメント URL)
- [ ] T061 [P] Alembic migration を実行確認 (alembic upgrade head で テーブル作成確認)
- [ ] T062 [P] FastAPI Swagger UI (http://localhost:8000/docs) で全エンドポイント動作確認
- [ ] T063 Postman または curl で 全エンドポイント (POST, GET, GET/{id}, PUT, PATCH, DELETE) の実機動作テスト
- [ ] T064 [P] 環境変数管理 (.env ファイル) と .env.example のドキュメント確認
- [ ] T065 ドキュメント整備 (api-contract.md, 開発ガイド、トラブルシューティング)

---

## タスク統計

- **総タスク数**: 65
- **セットアップ**: 5 タスク
- **基盤**: 10 タスク
- **US1 (登録, P1)**: 8 タスク + テスト 3 = 11 タスク
- **US2 (取得, P1)**: 8 タスク + テスト 4 = 12 タスク
- **US3 (更新, P2)**: 8 タスク + テスト 4 = 12 タスク
- **US4 (削除, P3)**: 5 タスク + テスト 3 = 8 タスク
- **ポーランド**: 11 タスク

---

## 依存グラフ & 実行順序

```
セットアップ (T001-T005)
    ↓
基盤 (T006-T015)
    ├→ US1 テスト (T016-T018)
    │   ├→ US1 実装 (T019-T023)
    │       ├→ US2 テスト (T024-T027)
    │       │   └→ US2 実装 (T028-T034)
    │       ├→ US3 テスト (T035-T038)
    │       │   └→ US3 実装 (T039-T046)
    │       └→ US4 テスト (T047-T049)
    │           └→ US4 実装 (T050-T054)
    └→ ポーランド (T055-T065)
```

---

## 並列実行例

### MVP リリース (US1 + US2)

**計画**: 最小 3-4 日間で配信可能

1. **Day 1**: セットアップ + 基盤 (T001-T015, 並列可)
2. **Day 2**: US1 完全実装 (T016-T023, 並列可のテスト先行)
3. **Day 3**: US2 完全実装 (T024-T034, T031/T032 並列)
4. **Day 4**: ポーランド & テスト確認 (T055-T064)

**チーム分け例**:

- **チーム A**: セットアップ + 基盤 (T001-T015)
- **チーム B**: US1 (T016-T023, T016/T017/T018 並列開始)
- **チーム C**: US2 (T024-T034, T024/T025 並列開始)

---

## 実装戦略: MVP ファースト

**MVP スコープ**: US1 (登録) + US2 (取得) = 最小機能セット

**理由**:

- 基本的な CRUD の 60% をカバー
- 複数チームの並列開発に対応可能
- P1 機能のみで先行リリース

**P2・P3 の追加予定**: US3 (更新) と US4 (削除) は後続スプリントで実装

---

## テストカバレッジ目標

**憲法要件**: 80% 以上

**実現方法**:

- **ユニットテスト**: models、schemas、services の全関数　(目標: 90%)
- **統合テスト**: API エンドポイント通成動作　(目標: 85%)
- **コントラクトテスト**: OpenAPI 仕様との整合　(目標: 100%)

**検証**: `pytest-cov` で `coverage report` 実行、自動チェック
