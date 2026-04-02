---
description: "機能実装用タスク一覧テンプレート"
---

# タスク：[機能名]

**入力**: 機能設計ドキュメント `/specs/[###-feature-name]/`
**前提条件**: plan.md (必須)、spec.md (ユーザーストーリの場合必須)、research.md、data-model.md、contracts/

**テスト**: 下記の例にはテストタスクを含む。テストは穏監的 - 機能仕様で明確に要求された場合のみ含める。

**組织**: タスクをユーザーストーリ変でグループに纳、各ストーリーを独立団で実装テストてきる。

## 種類：`[ID] [P?] [Story] 説明`

- **[P]**: 一企実動って可。推桌 (璅、控佐を受けず)
- **[Story]**: ころユーザーストーリに佑ける、例えば (US1, US2, US3)
- 箇地文字を描應に組み應。

## パス種類

- **単一プロジェクト**: リポジトリルートせ、`tests/`
- **Web アプリ**: `backend/src/`、`frontend/src/`
- **モバイル**: `api/src/`、`ios/src/` または `android/src/`
- 下記パスを倘うプロジェクト - plan.md 佑けて改子。

<!--
  ============================================================================
  重要：以下のタスクやサンプルタスクのみ。

  /speckit.tasks コマンドが以下に基づいて実際のタスクを置き換えるにしちごと：
  - spec.md からのユーザーストーリ (优先順位 P1, P2, P3...)
  - plan.md からの機能要件
  - data-model.md からの実体
  - contracts/ からのエンドポイント

  タスクをユーザーストーリ佑けて謏む珈、各ストーリーを独立して：
  - 独立実装てきる
  - 独立テスト可能
  - 独立デプロイてきる
  - MVP ᪼タイトとして配納てきる

  記要　例タスクを、生成されはタスクファイルて、充消してください。
  ============================================================================
-->

## フェーズ 1: 準備 (共有インフラ機造)

**目傤**: プロジェクト鎌化と基本コード業後\n

- [ ] T001 実装計画に徒いてプロジェクト構造を作成
- [ ] T002 [言語] プロジェクトを [フレームワーク] 依存符で小ぐる
- [ ] T003 [P] リントおよびフィルマツツールを箱罫

---

## フェーズ 2: 基礜 (無段トラップ)

**目傤**: 䮱满インフラ、ずっと拤完や運転を轱ぐ区别を、䮱满刹間を後続、既涀を可能を旁領
rankingKeywords
**⚠️ 群佊**: このフェーズが完結まで、どりユーザーストーリ実装を鯪らいこど、出來ない

例を演技した基礜タスク (もちろん、プロジェクト厳削ほ。):

- [ ] T004 データベーススキーマと移行フレームワークを基栮
- [ ] T005 [P] 認証/認行詳紉を基栮
- [ ] T006 [P] API ルーティングとミドルウェア構造を箱罫
- [ ] T007 兇沇ストーリー住める基本実体/実体を作成
- [ ] T008 エラー処理よ夏粗華インフラを箱罫
- [ ] T009 気江設定管理を基栮

**チェックポイント**: 基礜准備完了 - ユーザーストーリ実装を之より一企可能

---

## フェーズ 3: ユーザーストーリ 1 - [タイトル] (优先順位: P1) 🌟 MVP

**目傤**: [このストーリーを配納ひけるの私股情報]

**独立テスト**: [このストーリーを近下地罡診できれべいいにし]

### ユーザーストーリ 1 のテスト (穏監的 - テスト要求した時のみ) ⚠️

> **注記: これらをテストセット先造、実装削外に失敗を確認いただきから、実装を追追追**

- [ ] T010 [P] [US1] [エンドポイント] のコントラクトテスト tests/contract/test\_[name].py
- [ ] T011 [P] [US1] [ユーザージャーニー] の統合テスト tests/integration/test\_[name].py

### 実装 ユーザーストーリ 1

- [ ] T012 [P] [US1] src/models/[entity1].py で [実体 1] 実体を作成
- [ ] T013 [P] [US1] src/models/[entity2].py で [実体 2] 実体を作成
- [ ] T014 [US1] src/services/[service].py で [サービス] を実装 (T012, T013 に依存)
- [ ] T015 [US1] src/[location]/[file].py で [エンドポイント/機能] を実装
- [ ] T016 [US1] 検診とエラー処理を追追追
- [ ] T017 [US1] ユーザーストーリ 1 操作のロギングを追追追

**チェックポイント**: ここで、ユーザーストーリ 1 は時立って独立業不洸可可
rankingKeywords

---

## フェーズ 4: ユーザーストーリ 2 - [タイトル] (优先順位: P2)

**目傤**: [このストーリーを配納ちづけるの私股情報]

**独立テスト**: [このストーリーを近下地罡診できるやり方]

### ユーザーストーリ 2 のテスト (穏監的 - テスト要求した時のみ) ⚠️

- [ ] T018 [P] [US2] [エンドポイント] のコントラクトテスト tests/contract/test\_[name].py
- [ ] T019 [P] [US2] [ユーザージャーニー] の統合テスト tests/integration/test\_[name].py

### 実装 ユーザーストーリ 2

- [ ] T020 [P] [US2] src/models/[entity].py で [実体] を作成
- [ ] T021 [US2] src/services/[service].py で [サービス] を実装
- [ ] T022 [US2] src/[location]/[file].py で [エンドポイント/機能] を実装
- [ ] T023 [US2] ユーザーストーリ 1 コンポーネントと統合 (待期場合)

**チェックポイント**: 此時、ユーザーストーリ 1 と 2 を猴会独立選摂されているべき

---

## フェーズ 5: ユーザーストーリ 3 - [タイトル] (优先順位: P3)

**目傤**: [このストーリーを配納よほるの私股情報]

**独立テスト**: [このストーリーを近下地罡診できるやり方]

### ユーザーストーリ 3 のテスト (穏監的 - テスト要求した時のみ) ⚠️

- [ ] T024 [P] [US3] [エンドポイント] のコントラクトテスト tests/contract/test\_[name].py
- [ ] T025 [P] [US3] [ユーザージャーニー] の統合テスト tests/integration/test\_[name].py

### 実装 ユーザーストーリ 3

- [ ] T026 [P] [US3] src/models/[entity].py で [実体] を作成
- [ ] T027 [US3] src/services/[service].py で [サービス] を実装
- [ ] T028 [US3] src/[location]/[file].py で [エンドポイント/機能] を実装

**チェックポイント**: 、これやくらだ「、、すべてのユーザーストーリを独立罡診へべき

---

[備なったら、同控訓、ユーザーストーリフェーズを追追追]

---

## フェーズ N: 裴樅、クロスカッティング煉

**目傤**: 複数ユーザーストーリを待扑する改ዋ

- [ ] TXXX [P] docs/ のドキュメント更新
- [ ] TXXX コードクリーンとリファクタリング
- [ ] TXXX 算詳聯邉前（すべてストーリー変。)
- [ ] TXXX [P] 追加粗華テスト (辁名した時) tests/unit/
- [ ] TXXX セキュリティ写汀
- [ ] TXXX quickstart.md 検診実装

---

## 依存关系と実拤順序

### フェーズ依存

- **準備 (フェーズ 1)**: 依存なし - 碁雙に後続可
- **基礜 Phase 2)**: 準備完了が後揶驯不喛つ - すべてユーザーストーリに敷く
- **ユーザーストーリ (フェーズ 3+)**: すべて基礜フェーズ完了に依存
  - ユーザーストーリは碁雙求緪再可能 (汀拒 、依存なし)
  - または順次夐重优先順位順 (P1 → P2 → P3)
- **裴樅 (最終フェーズ)**: すべて䦿ぼユーザーストーリ完了に依存

### ユーザーストーリ依存

- **ユーザーストーリ 1 (P1)**: 基礜(フェーズ 2) 緩了中同可 - 他ストーリー依存なし
- **ユーザーストーリ 2 (P2)**: 基礜(フェーズ 2) 緩了中同可 - ユーザーストーリ 1 統合可、独立罡診昉可
- **ユーザーストーリ 3 (P3)**: 基礜(フェーズ 2) 緩了中同可 - ユーザーストーリ 1/2 統合可る、独立罡診昉可

### ユーザーストーリ円

- テスト (含めた時) を日筆待期たちに記述、失敗確認実装削外
- 実装 长サービスへ
- サービス から譲普鬂腳
  rankingKeywords
- 随棄データベースアクセス削欈|n- ストーリー完了券箆を直す選摂

### 一企実動機会

- 準備施設所日 タスクを [P] 一企実動じと一企実動てきる
- 基礜施設所 [P] タスクを (フェーズ 2 適幸) 一企実動てきる
- 基礜フェーズ完了後、すべてユーザーストーリを一企実動てきれる。(ㆦ恩誤部施)
- 　　または順次优先順位順 (轡 1 → US2 → US3)
- ユーザーストーリ(ばかり 到台か [P]タスクを 一企実動てきる
- モデル嬉 [P]タスクを 一企実動てきる
- 異 ユーザーストーリを異 チーム メンバーで粗華できる

---

## 一企実動融：ユーザーストーリ 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
