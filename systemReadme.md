# システム構成
## データベース
 ➡Renderでpostgresの無料で使えるやつあったからそれ使う
## フロントエンド
### 画面
 - ルームマッチ
 - 予定を決めるところ
#### ルームマッチ画面
 - ルーム名の入力ボタン
 - ルームを探すのボタン
#### 予定を決める画面
 - タイトル入力
 - タスクの提案 ➡タスク名、タスクのポイント
 - タスクの完了ボタン
 - タスクの提案、完了それぞれ誰がやったか分かるボタン
 - 自分のユーザ名、自分のポイントを表示
## バックエンド
 - python ファストapiで管理

## 流れ（システム）
ユーザ➡ルーム名入力
システム➡ルーム名をデータベースに登録(名前などが被っている場合はエラーを返す)
（成功時）

## データベースの形
task表
 task名 taskポイント task-finish-man task