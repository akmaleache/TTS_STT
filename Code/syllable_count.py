import syllables
from fuzzywuzzy import fuzz
import pyodbc 
import item_pool as pool
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
success_word = 100
success_syllable = 100
server = 'tcp:pshycomms.database.windows.net' 
database = 'psychComms_db' 
username = 'pshycomms' 
password = 'ZrdjUMR3heDj' 


def spell_check(query_text, user_text):

	query_split = query_text.split()
	user_split = user_text.split()
	
	q_syllable_cnt = 0
	u_syllable_cnt = 0

	# word score
	total_word = len(query_split)
	w_score = fuzz.ratio(query_text, user_text)

	# Syllable score
	for i in range(0,len(query_split)):
		q_syllable_cnt += syllables.estimate(query_split[i])
	for i in range(0,len(query_split)):
		try:
			u_syllable_cnt += syllables.estimate(user_split[i])
		except:
			break
		
	syllable_score = round((u_syllable_cnt/q_syllable_cnt) * 100)
	# print(q_len,q_syllable_cnt)
	# print(u_len,u_syllable_cnt)

	## 30-40-30 % slpit of word- score

	# thirty_1 = round(0.3*len(query_split))
	# fourty = round(0.4*len(query_split))
	# sent_1 = query_split[0:thirty_1]
	# sent_2 = query_split[thirty_1:fourty+thirty_1]
	# sent_3 = query_split[fourty+thirty_1:]

	# print(thirty_1,fourty,sent_1,sent_2,sent_3)
	return(total_word,w_score,q_syllable_cnt,syllable_score)


def move_forward(age,set_no, query_no):
	next_set = set_no+1
	if set_no == 0 and age > 0:
		next_set = set_no+2
		next_query = 0
	elif set_no == 1:
		next_query = query_no + 1
	elif set_no == 12:
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
	elif set_no == 0:
		if query_no == 0:
			next_set = 0
			next_query = 1
		else:
			next_set = 'none'
			next_query = 'none'
	elif set_no == 1:
		if query_no < 3:
			next_set = 1
			next_query = query_no+1
		else:
			next_set = 'none'
			next_query = 'none'
	elif set_no > 2 and query_no > 3:
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

def get_cursor():
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	return(cursor,cnxn)

def add_new_user(user):
	cursor,cnxn = get_cursor()
	cursor.execute("INSERT INTO User_table VALUES (?);",user)
	cnxn.commit()
	cnxn.close()

def insert_user_score(user,question,tot_word,success_word,w_score,tot_syllable,success_syllable,syllable_score,final_out):
	cursor,cnxn = get_cursor()
	cursor.execute("INSERT INTO Score_Table VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)",(user,question,tot_word,success_word,w_score,tot_syllable,success_syllable,syllable_score,final_out))
	cnxn.commit()
	cnxn.close()

qus_no = {0:'A',1:'B',2:'C',3:'D',4:'E'}

def logic_flow(user_id,age,user_text,co_ordinate):
	if user_text == '' and co_ordinate == '':
		set_no = 0
		query_no = 0
		# sql create table
		add_new_user(user_id)
		return({'co_ordinate':(set_no,query_no),'next_text': pool.set_pool[set_no][query_no]})

	set_no = int(co_ordinate[0])
	query_no = int(co_ordinate[2])
	actual_text = pool.set_pool[set_no][query_no]
	print(actual_text)
	tot_word,w_score,tot_syllable,syllable_score =spell_check(actual_text.lower(),user_text.lower())
	print(w_score)
	if w_score < 100:
		final_out  = 'Fail'
		insert_user_score(user_id,str(set_no)+qus_no[query_no],tot_word,success_word,w_score,tot_syllable,success_syllable,syllable_score,final_out)
		set_no,query_no = move_back(set_no,query_no)
		print(set_no,query_no)
		if set_no == 'none' and query_no == 'none':
			return('END')
	else:
		final_out = 'Pass'
		insert_user_score(user_id,str(set_no)+qus_no[query_no],tot_word,success_word,w_score,tot_syllable,success_syllable,syllable_score,final_out)
		set_no,query_no = move_forward(int(age),set_no,query_no)
		if set_no == 'none' and query_no == 'none':
			return('END')
	return({'co_ordinate':(set_no,query_no),'next_text': pool.set_pool[set_no][query_no]})




	
	