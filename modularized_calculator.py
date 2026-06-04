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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

# 掛け算と割り算の処理
def evaluate_multiplication_division(tokens):

    result_multiplication_division = [] # 足し算と引き算の処理に渡す用のリストを作成

    index = 0
    while index < len(tokens):
        curr_token = tokens[index]

        # 今見ているトークンが*か/の場合
        if curr_token['type'] == 'TIMES' or curr_token['type'] == 'DIVIDED':
            recent_token = result_multiplication_division.pop() # 直前にリストに入れた数字を取り出し、リストから削除する

            index += 1  # 演算子の次のトークンに進む
            next_token = tokens[index]

            if curr_token['type'] == 'TIMES':
                calculated_answer = recent_token['number'] * next_token['number']
            else:
                calculated_answer = recent_token['number'] / next_token['number']

            # 計算結果を新しい数字トークンとしてリストに追加
            result_multiplication_division.append({'type': 'NUMBER', 'number': calculated_answer})

        else:
            # 数字、PLUS、MINUS はそのままリストへ流す
            result_multiplication_division.append(curr_token)

        index += 1

    return result_multiplication_division

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



def test(line):
    tokens = tokenize(line)
    result_multiplication_division = evaluate_multiplication_division(tokens)
    actual_answer = evaluate_addition_subtraction(result_multiplication_division)
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
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    print(tokens)
    result_multiplication_division = evaluate_multiplication_division(tokens)
    print(result_multiplication_division)
    answer = evaluate_addition_subtraction(result_multiplication_division)
    print("answer = %f\n" % answer)
