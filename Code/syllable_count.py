import syllables
from fuzzywuzzy import fuzz
import pyodbc 

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:pshycomms.database.windows.net' 
database = 'psychComms_db' 
username = 'pshycomms' 
password = 'ZrdjUMR3heDj' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


def spell_check(query_text, user_text):

	query_split = query_text.split()
	user_split = user_text.split()
	
	q_syllable_cnt = 0
	u_syllable_cnt = 0

	# word score
	w_score = fuzz.partial_ratio(query_text, user_text)

	# Syllable score
	for i in range(0,len(query_split)):
		q_syllable_cnt += syllables.estimate(query_split[i])
		try:
			u_syllable_cnt += syllables.estimate(user_split[i])
		except:
			break
		
	syllable_score = (u_syllable_cnt/q_syllable_cnt) * 100
	# print(q_len,q_syllable_cnt)
	# print(u_len,u_syllable_cnt)

	## 30-40-30 % slpit of word- score

	# thirty_1 = round(0.3*len(query_split))
	# fourty = round(0.4*len(query_split))
	# sent_1 = query_split[0:thirty_1]
	# sent_2 = query_split[thirty_1:fourty+thirty_1]
	# sent_3 = query_split[fourty+thirty_1:]

	# sqlite3 table saving rerord
	# s = User_Score(word_score=word_score,syllable_score=syllable_score) 
	# s.save()
	# print(thirty_1,fourty,sent_1,sent_2,sent_3)
	return(w_score)



pr = ['All must go','Hold my cup']
set_1 = ['Move the hammer',
		 'Can you sense it',
		 'Boxes are full',
		 'They now like sweets'
		]

set_2 = ['Raining dogs and cats',
		 'Carrots and apples',
		 'Old people are wise',
		 'The weather has changed',
		 'Ten tons of old junk'
		]

set_3 = ['Vision is a great sense to have',
		 'The book was a very good read',
		 'Computers can be annoying',
		 'Time is shifting beneath our feet',
		 'The first time is always a thrill',
		]

set_4 = ['Monitor them, for fear of a mutiny',
		 'We piled into our van for the evening',
		 'Stormy times shifted beyond normality',
		 'Though believing her, they pressed the rocker switch',
		 'As they approached, the tiny kitten ran off',
		]

set_5 = ['And I wonder if she dreamed like the other animals',
		 'A bottle fund was arranged to light up more hearts and minds ',
		 'Holding my newspaper tight to my chest in total awe ',
		 'Then all fell silent across the newly formed republic',
		 'The joke went down really well on the couple’s first date',
		]
set_pool = [pr,set_1,set_2,set_3,set_4,set_5]

def move_forward(age,set_no, query_no):
	next_set = set_no+1
	if set_no == 0 and age > 8:
		next_set = set_no+2
		next_query = 0
	elif set_no == 1:
		next_query = query_no + 1
	elif set_no == 5:
		next_set = 'none'
		next_query = 'none'
	elif query_no < 2:
		next_query = 0
	elif query_no >= 2:
		next_query = query_no - 1
	print(set_no,query_no)
	return(next_set,next_query)

def move_back(set_no, query_no):
	next_set = set_no - 1
	if set_no == 2:
		next_query = query_no
		if next_set == 1 and next_query == 4:
			next_set = 'none'
			next_query = 'none'
	elif set_no == 1 or query_no == 4:
		next_set = 'none'
		next_query = 'none'
	elif query_no == 0:
		next_query = 2
	elif query_no > 0:
		next_query = query_no +2
		if next_query > 4:
			next_set = 'none'
			next_query = 'none'

	print(set_no,query_no,next_set,next_query)
	return(next_set,next_query)



def logic_flow(user_id,age,user_text,co_ordinate):
	if user_text == '' and co_ordinate == '':
		set_no = 0
		query_no = 0
		return({'co_ordinate':(set_no,query_no),'next_text': set_pool[set_no][query_no]})
	set_no = int(co_ordinate[0])
	query_no = int(co_ordinate[2])
	actual_text = set_pool[set_no][query_no]
	print(actual_text)
	if spell_check(actual_text,user_text) < 80:
		set_no,query_no = move_back(set_no,query_no)
		print(set_no,query_no)
		if set_no == 'none' and query_no == 'none':
			return('END')
		# print((set_no,query_no), set_pool[set_no][query_no])
	else:
		set_no,query_no = move_forward(int(age),set_no,query_no)
		# print((set_no,query_no), set_pool[set_no][query_no])
		if set_no == 'none' and query_no == 'none':
			return('END')
	return({'co_ordinate':(set_no,query_no),'next_text': set_pool[set_no][query_no]})


# logic_flow()


	
	