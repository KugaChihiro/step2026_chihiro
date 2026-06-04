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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
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
                    new_token = {'type':'NUMBER','number': answer} # 四則演算の結果をtokenとして追加。不要な箇所は削除。
                    del tokens[new_index:index+1]
                    tokens.insert(new_index,new_token)
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
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    evaluate(tokens)
