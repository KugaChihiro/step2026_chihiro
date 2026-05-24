def anagram02(true_dictionary,input):

  # 入力値について、各単語ごとに構成文字とその出現回数をまとめたものをdictとして作成
  input_character_list = list(set(input))
  input_disassembled = {cha:input.count(cha) for cha in input_character_list}

  # 比較処理の結果、True（アナグラム成立）と判断されたら場合のみ、その成立したアナグラムをanswerとして設定（デフォルトはNone）
  answer = None
  for word in list(true_dictionary.keys()):
    if compare(true_dictionary[word],input_disassembled):
      answer = word
      break
    else:
        continue

  # 成立したアナグラムが格納されたlistを、answer.txtに出力
  # もしアナグラムが1つも見つからなかった問題は、空行(改行だけ)を出力する
  with open("answer.txt","a") as answer_txt:
    if answer == None:
      answer_txt.write("\n")
    else:
      answer_txt.write(answer + "\n")

# 辞書を作成する関数
def create_dicitonary():

  # 辞書のファイルを開いて、listとして保持
  dictionary_list = file_open("words.txt")

  true_dictionary = {}

  # 辞書内における各単語に対するスコアの計算を行い、スコアの高い単語順にソートした状態にする
  with_score_dict = {word:calculate_score(word) for word in dictionary_list}
  sorted_list = sorted(with_score_dict, key=with_score_dict.get, reverse=True)

  # 辞書について、もともとの単語をkey、各単語ごとに構成文字とその出現回数をまとめたもの(dict形式)をvalueとして、true_dictionaryに順次格納
  for word in sorted_list:
    dictionary_character_list = list(set(word))
    true_dictionary_disassembled = {cha:word.count(cha) for cha in dictionary_character_list}
    true_dictionary[word] = true_dictionary_disassembled
  return true_dictionary

# 前処理完了後の入力値と、前処理完了後の辞書（各単語ごとに構成文字とその出現回数をまとめたもの）のlistに含まれる一単語を比較する
# 比較の結果、辞書の中の一単語が必要とする構成文字を入力値が保持していたら、bool値を返す関数
def compare(true_dictionary_disassembled,true_input):
    for key in list(true_dictionary_disassembled.keys()):
       if true_input.get(key, 0) >= true_dictionary_disassembled.get(key, 0):
          bool = True
          continue
       else:
          bool = False
          break
    return bool

# ファイルを開いて、listとして保持するための関数
def file_open(file_name):
  with open(file_name,"r") as file:
    file_list = [i.rstrip() for i in file.readlines()]
  return file_list

# スコアの計算
def calculate_score(word):
    SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score


# 辞書の初期値をリセット

true_dictionary = {}

# 入力値として定めた複数の文字列（リスト）から、1語ずつ取り出して処理を実行
for input in file_open("small.txt"):
  if not true_dictionary:
     true_dictionary = create_dicitonary()
  anagram02(true_dictionary,input)