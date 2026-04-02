# SSDtest プロジェクト - Session 記録インデックス

**プロジェクト開始日**: 2026-04-02  
**技術スタック**: Python / FastAPI / SQLite  
**記録ポリシー**: Session ごとに変更内容・変更ファイル・指示内容を記録

---

## Session 記録一覧

### Session 1: 憲法初期化・日本語化

**日時**: 2026-04-02  
**記録ファイル**: [2026-04-02_constitution-init.md](./2026-04-02_constitution-init.md)

#### 実施内容

- プロジェクト憲法（constitution.md）の日本語化
- FastAPI + SQLite に適合させた 5 つのコア原則の定義
- ガバナンスルール、開発ワークフローの確立
- `./record` ディレクトリ体制の構築

#### 更新ファイル

| ファイル                          | 変更内容                     |
| --------------------------------- | ---------------------------- |
| `.specify/memory/constitution.md` | 日本語化・プロジェクト固有化 |
| `record/`                         | ディレクトリ作成             |

#### 次フェーズ

- テンプレート同期確認
- `docs/development.md` 作成
- 第一次フィーチャー計画

---

## 記録ポリシー

すべての Session について以下を記録します：

### 必須項目

- **実施日時**
- **実施内容**（章立てで整理）
- **変更ファイル一覧**（ファイルパス → 変更タイプ）
- **指示内容**（ユーザー要求の要件）
- **変更の理由・背景**
- **次ステップ**

### ファイル命名規則

```
YYYY-MM-DD_<session-topic>.md
例: 2026-04-02_constitution-init.md
   2026-04-03_spec-feature-auth.md
```

### ファイル保存先

```
./record/
```

---

## 参考リンク

- [プロジェクト憲法](./.specify/memory/constitution.md)
- [spec テンプレート](./.specify/templates/spec-template.md)
- [plan テンプレート](./.specify/templates/plan-template.md)
- [tasks テンプレート](./.specify/templates/tasks-template.md)
