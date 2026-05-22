def anagram02(input):

  # 辞書のファイルを開いて、listとして保持
  dictionary_list = file_open("words.txt")

  true_dictionary = {}

  # 辞書について、もともとの単語をkey、各単語ごとに構成文字とその出現回数をまとめたもの(dict形式)をvalueとして、true_dictionaryに順次格納
  for word in dictionary_list:
    dictionary_character_list = list(set(word))
    true_dictionary_disassembled = {cha:word.count(cha) for cha in dictionary_character_list}
    true_dictionary[word] = true_dictionary_disassembled

  # 入力値について、各単語ごとに構成文字とその出現回数をまとめたものをdictとして作成
  input_character_list = list(set(input))
  input_disassembled = {cha:input.count(cha) for cha in input_character_list}

  answer_list = []

  # 比較処理の結果、True（アナグラム成立）と判断されたら場合のみ、その成立したアナグラムをlistに追加
  for word in list(true_dictionary.keys()):
    if compare(true_dictionary[word],input_disassembled):
       answer_list.append(word)

  # 成立したアナグラムが格納されたlistを、answer.txtに出力
  # 入力値の1単語につき、一行分になるよう、成立したアナグラムはカンマで区切る
  with open("answer.txt","a") as o:
      o.write(" ".join(answer_list) + "\n")


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


# 入力値として定めた複数の文字列（リスト）から、1語ずつ取り出して処理を実行
for input in file_open("small.txt"):
	anagram02(input)