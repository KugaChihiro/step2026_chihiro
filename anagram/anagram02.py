def anagram02(x,y):
  true_dictionary = []

  for i in range(len(x)):
    dictionary_word_list = sorted(list(set(x[i])))
    true_dictionary.append({i:y.count(i) for i in dictionary_word_list})

  input_word_list = list(set(y))
  true_input = {i:y.count(i) for i in input_word_list}

# 【わからないところ】true_inputにある文字が、必要個数分true_dictionary[i]にもあるか確かめたい
  true_input.keys()
  for i in range(len(true_dictionary)):
    true_dictionary[i]

with open("words.txt","r") as dictionary_file:
  dictionary_list = [i.rstrip() for i in dictionary_file.readlines()]

with open("small.txt","r") as input_file:
  input_list = [i.rstrip() for i in input_file.readlines()]

for i in range(len(input_list)):
	print(anagram02(dictionary_list,input_list[i]))