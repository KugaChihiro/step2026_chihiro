def anagram01(x,y):
	sorted_dictionary = {("".join(sorted(i))) : i for i in x}
	new_dictionary = dict(sorted(sorted_dictionary.items()))

	new_input = "".join(sorted(y))
	new_dictionary_keys = list(new_dictionary.keys())
	high = len(new_dictionary_keys)-1
	low = 0
	while low <= high:
		mid = (high+low)//2
		if new_dictionary_keys[mid] == new_input:
			return new_dictionary[new_dictionary_keys[mid]]
		elif new_dictionary_keys[mid] > new_input:
			high = mid-1
		else:
			low = mid+1


#　make_sorted()を呼び出して、辞書と入力の両方をソートする
with open("words.txt","r") as dictionary_file:
  dictionary_list = [i.rstrip() for i in dictionary_file.readlines()]

with open("test01.txt","r") as input_file:
  input_list = [i.rstrip() for i in input_file.readlines()]

for i in range(len(input_list)):
	print(anagram01(dictionary_list,input_list[i]))

