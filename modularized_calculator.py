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
    result_multiplication_division = []
    calculated_answer = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    finished_check_index = 0
    is_multiplicating_dividing = False
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'TIMES':
                if not is_multiplicating_dividing:
                    calculated_answer =  tokens[index-2]['number']
                    is_multiplicating_dividing = True
                calculated_answer *= tokens[index]['number']
                result_multiplication_division += tokens[finished_check_index:index-2]
                finished_check_index = index-2
            elif tokens[index - 1]['type'] == 'DIVIDED':
                if not is_multiplicating_dividing:
                    calculated_answer =  tokens[index-2]['number']
                    is_multiplicating_dividing = True
                calculated_answer /=  tokens[index]['number']
                result_multiplication_division += tokens[finished_check_index:index-2]
                finished_check_index = index-2
            elif tokens[index - 1]['type'] == 'PLUS' or tokens[index - 1]['type'] == 'MINUS':
                if is_multiplicating_dividing:
                    is_multiplicating_dividing = False
                    finished_check_index = index-1
                    calculated_token =  {'type':'NUMBER','number':calculated_answer}
                    result_multiplication_division.append(calculated_token)
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    if is_multiplicating_dividing:
        calculated_token =  {'type':'NUMBER','number':calculated_answer}
        result_multiplication_division.append(calculated_token)
    else:
        result_multiplication_division += tokens[finished_check_index:]
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
