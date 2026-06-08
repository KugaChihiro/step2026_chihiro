#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_times(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def read_divided(line, index):
    token = {'type': 'DIVIDED'}
    return token, index + 1

def read_left_parentheses(line, index):
    token = {'type': 'L_PARENTHESES'}
    return token, index + 1

def read_right_parentheses(line, index):
    token = {'type': 'R_PARENTHESES'}
    return token, index + 1

def read_word(line, index):
    start = index
    # アルファベットが続く限り、indexを進める
    while index < len(line) and line[index].isalpha():
        index += 1

    # 切り出した単語（例: "abs", "int", "round"）
    word = line[start:index]

    # 単語の種類に応じてトークンを作る
    if word == 'abs':
        token = {'type': 'ABS'}
    elif word == 'int':
        token = {'type': 'INT'}
    elif word == 'round':
        token = {'type': 'ROUND'}
    else:
        print(f"Unknown function or word: {word}")
        exit(1)

    return token, index

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_divided(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parentheses(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parentheses(line, index)
        elif line[index].isalpha():
            (token, index) = read_word(line, index)
        else:
            # スペースなどを無視するための安全弁
            index += 1
            continue
        tokens.append(token)
    return tokens

# 掛け算と割り算の処理
def evaluate_multiplication_division(tokens):
    index = 0
    while index < len(tokens):
        # 今見ているトークンが*か/の場合
        if tokens[index]['type'] == 'TIMES' or tokens[index]['type'] == 'DIVIDED':
            if tokens[index]['type']  == 'TIMES':
                answer = tokens[index-1]['number'] * tokens[index+1]['number']
            else:
                answer = tokens[index-1]['number'] / tokens[index+1]['number']

            # 計算結果を新しい数字トークンとしてリストに追加
            del tokens[index-1:index+2]
            new_token = {'type':'NUMBER','number':answer}
            tokens.insert(index-1,new_token)
        else:
            index += 1
    return tokens

# 足し算と引き算の処理
def evaluate_addition_subtraction(tokens):
    answer = 0
    index = 1
    tokens.insert(0, {'type': 'PLUS'})
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            elif tokens[index - 1]['type'] == 'TIMES' or tokens[index - 1]['type'] == 'DIVIDED':
                print('Multiplication and division cannot be processed in the second step.')
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

# （）の処理を行う
# 1. 現時点で一番内側かつ左側にある()で囲まれた範囲を特定する
# 2. 1の範囲内で四則演算を実行
# 3. 四則演算の結果をもとに、tokensを更新 : ((1+2)*2+1)*2 -->  (3*2+1)*2

def evaluate_parentheses(tokens):
    index = 0
    while index < len(tokens):  # tokensのリストを先頭から走査。一番初めに見つかった")"について考える。
        if (tokens[index]['type'] == 'R_PARENTHESES'):
            new_index = index
            while 0 <= new_index < len(tokens): # ")"が一番初めにindexから、反対方向にさかのぼり、"("を探す。
                if tokens[new_index]['type'] == "L_PARENTHESES":
                    answer = evaluate_4_arithmetic_operations(tokens[new_index+1:index]) # ()のセットが見つかった場合、その（）内で四則演算を行う。

                    # 削除を開始する位置（関数の有無で変える）を管理する変数
                    start_delete_index = new_index

                    # カッコの1つ前に関数（ABS, INT, ROUND）があるかチェック
                    if new_index > 0 and tokens[new_index-1]['type'] in ('ABS', 'INT', 'ROUND'):
                        func_type = tokens[new_index-1]['type']
                        start_delete_index = new_index - 1  # 関数ごと削除するためにインデックスを1つ前にずらす

                        if func_type == "ABS":
                            if answer < 0:
                                answer = -answer
                        elif func_type == "INT":
                            answer = answer // 1        # 1で割った商（整数部）
                        elif func_type == "ROUND":
                            integer_answer = answer // 1
                            fractional_answer = answer % 1      # 1で割った余り（小数部）
                            if fractional_answer >= 0.5:
                                integer_answer += 1
                            answer = integer_answer

                    new_token = {'type':'NUMBER','number': answer}

                    # 関数トークンやカッコをまとめて綺麗に削除して置き換え
                    del tokens[start_delete_index:index+1]
                    tokens.insert(start_delete_index, new_token)
                    return tokens
                new_index -= 1
        index += 1

# 四則演算を行う
# 掛け算・割り算→足し算・引き算
def evaluate_4_arithmetic_operations(tokens):
    tokens = evaluate_multiplication_division(tokens)
    answer = evaluate_addition_subtraction(tokens)
    return answer

# カッコが1つでも残っていれば、カッコ内を計算（evaluate_parentheses）して、最初からやり直す（再帰）
# カッコがすべて消えたら、通常の四則演算を行って最終結果を返す
def evaluate(tokens):
    if any(token.get('type') == 'L_PARENTHESES' for token in tokens):
        tokens = evaluate_parentheses(tokens)
        return evaluate(tokens)
    else:
        answer = evaluate_4_arithmetic_operations(tokens)
        return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))



# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("2-1")
    test("1-2")
    test("2*2")
    test("2/2")
    test("2*2*2")
    test("2*2-2")
    test("2-2*2")
    test("8-2*2-2")
    test("0.1+0.2")
    test("0.1+1")
    test("1+0.1")
    test("1.0+2.1-3")
    test("(1+2)")
    test("(1+2*3)")
    test("((1+2)*3)")
    test("(1+2)*(1+3)")
    test("abs(1-3)")
    test("int(1.5+2.1)")
    test("round(1.6)")
    test("12 + abs(int(round(1.55) + abs(int(2.3 + 4))))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    print(evaluate(tokens))