## 宿題3-1

- 掛け算・割り算の処理（evaluate_multiplication_division）　→　足し算・引き算の処理（evaluate_addition_subtraction）　の二段階で処理を行う
- 掛け算・割り算の処理をし終えたリスト（*/の記号が残っていない状態）を、evaluate_addition_subtractionに渡すことで、上記の二段階での処理を実現

### 掛け算・割り算の処理

- 既存のリスト(tokens)を先頭から順番に走査する
- 計算結果を格納する新しいリスト（result_multiplication_division）を用意する
  - このリストは、後続の evaluate_addition_subtraction へ渡すためのもの。

-トークンの種類に応じて、以下の通り処理を行う
 - 通常の数字や演算子（+, -）の場合：
    - そのまま result_multiplication_division に追加する。
 - *, / の場合：
  - 直前に result_multiplication_division へ追加した数字をリストから取り出す（.pop）
  - インデックスを1進めて（index += 1）、演算子の次にあるトークン（next_token）を取得する。
  -「取り出した数字」とnext_token」で掛け算or割り算を行い、その計算結果を result_multiplication_division に格納する。
  - ※あらかじめインデックスを先に進めておくことで、次のループで同じ数字を二重に処理してしまうのを防ぎ、そのさらに次のトークンから処理を再開できる。