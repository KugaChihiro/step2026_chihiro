## 宿題3-3

- より内側かつ左側の()の処理を優先的に行う

### 掛け算・割り算の処理

- evaluate（全体）
　- Q. tokensに()が含まれている？

    -> Yes : evaluate_parentheses（()の処理）
      - 最も内側かつ左側にある()の範囲を確定
      - （）内の範囲において、evaluate_4_arithmetic_operations（四則演算）を実行
        - evaluate_multiplication_division　（掛け算・割り算）を実行
        - evaluate_addition_subtraction　（足し算・引き算）を実行
      - 四則演算の答えをもとに、tokensを更新 ※ ((1+2)*2+1)*2 -->  (3*2+1)*2
      - もう一度evaluateを実行。（**再帰**）

    -> No : tokensについてevaluate_4_arithmetic_operations（四則演算）を実行
        - evaluate_multiplication_division　（掛け算・割り算）を実行
        - evaluate_addition_subtraction　（足し算・引き算）を実