import syllables

text = input()
text_split = text.split()
w_len = len(text_split)
cnt = 0
for word in text_split:
	cnt += syllables.estimate(word)

print((cnt,w_len))