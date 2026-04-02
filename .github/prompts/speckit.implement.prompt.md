---
agent: speckit.implement
---

# Constitution.md 準拠確認

このモード完了時に、以下を確認してください：

**必須チェックリスト**:

- [ ] `.specify/memory/constitution.md` の全ルール準拠を確認
- [ ] 特に以下の原則が守られていることを確認：
  - I. API-ファースト設計（OpenAPI ドキュメント作成）
  - II. テスト駆動開発（テストカバレッジ 80% 以上）
  - III. データベース設計一貫性（migration スクリプト管理）
  - IV. ログと可観測性（構造化ログ実装）
  - V. セキュリティ・入力検証（Pydantic 検証、SQL パラメータ化）
- [ ] 該当する内容について Session ごとに `./record/YYYY-MM-DD_<topic>-implement.md` を作成

詳細は [constitution.md](.specify/memory/constitution.md) を参照
