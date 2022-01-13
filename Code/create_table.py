import pyodbc 

server = 'tcp:pshycomms.database.windows.net' 
database = 'psychComms_db' 
username = 'pshycomms' 
password = 'ZrdjUMR3heDj' 

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("CREATE TABLE User_table (User_ID INTEGER NOT NULL PRIMARY KEY);")
cnxn.commit()
cursor.execute("CREATE TABLE Score_Table (User_ID int FOREIGN KEY REFERENCES User_table(User_ID),Question_no TEXT NOT NULL,Total_word  INTEGER NOT NULL,Success_word  INTEGER NOT NULL,Attempt_word  INTEGER NOT NULL,Total_syllable  INTEGER NOT NULL,Success_syllable  INTEGER NOT NULL,Attempt_syllable  INTEGER NOT NULL,Final_out TEXT NOT NULL);")
cnxn.commit()
cnxn.close()