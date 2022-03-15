import sqlite3
import os
import logging
import datetime
import json

# dbfile = os.path.join('device_module/', 'table.db')
if os.path.exists('chat_table.db'):
    os.remove('chat_table.db')

class Chat():
	def __init__(self):
		logging.basicConfig(format='%(levelname)s - %(message)s')
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.INFO)

	def check(self, user_id, connect_id):
		if (isinstance(user_id, int) and isinstance(connect_id, int)):
			if (user_id != connect_id):
				return True


	def create_tables(self, user_id, connect_id):
		conn = sqlite3.connect('chat_table.db')
		cur = conn.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

		a = [x[0] for x in cur.fetchall()]
		if (f'User_{user_id}_Records' not in a):
			cur.execute(f'CREATE TABLE User_{user_id}_Records (Record_Num INTEGER PRIMARY KEY AUTOINCREMENT, From_id INTEGER, To_id INTEGER, Message_Type TEXT, Content TEXT, Time TEXT)')
		if (f'User_{connect_id}_Records' not in a):
		 	cur.execute(f'CREATE TABLE User_{connect_id}_Records (Record_Num INTEGER PRIMARY KEY AUTOINCREMENT, From_id INTEGER, To_id INTEGER, Message_Type TEXT, Content TEXT, Time TEXT)')
		
		id_list = [user_id, connect_id]
		id_list.sort()
		self.tt = f"User{id_list[0]}_User{id_list[1]}"

		if (self.tt not in a):
			cur.execute(f'CREATE TABLE {self.tt} (Record_Times INTEGER PRIMARY KEY AUTOINCREMENT, From_id INTEGER, To_id INTEGER, Message_Type TEXT, Content TEXT, Time TEXT)')
		#cur.execute(f'CREATE TABLE {user_id}(Connect_to INTEGER PRIMARY KEY, Message_Type TEXT, Content TEXT)')

		conn.commit()
		conn.close

	def store_data(self, user_id, connect_id, message_type, content):
		conn = sqlite3.connect('chat_table.db')
		cur = conn.cursor()

		time = str(datetime.datetime.now())

		cur.execute(f'INSERT INTO User_{user_id}_Records VALUES ((SELECT MAX(Record_Num) + 1 FROM User_{user_id}_Records),{user_id}, {connect_id}, "{message_type}", "{content}", "{time}")')
		cur.execute(f'INSERT INTO User_{connect_id}_Records VALUES ((SELECT MAX(Record_Num) + 1 FROM User_{connect_id}_Records),{connect_id}, {user_id}, "{message_type}", "{content}", "{time}")')
		cur.execute(f'INSERT INTO {self.tt} VALUES ((SELECT MAX(Record_Times) + 1 FROM {self.tt}),{user_id}, {connect_id}, "{message_type}", "{content}", "{time}")')


		# for row in cur.execute(f'SELECT * FROM User_{user_id}_Records'):
		# 	print(row)
		# print("test\n")

		conn.commit()
		conn.close

	def control(self, jsfile):
		f = open(jsfile) # data.json
		data = json.loads(f.read())

		for key in data.keys():
			user_id = int(data[key]["User_id"])
			connect_id = int(data[key]["Connect_id"])
			message_type = data[key]["Message_Type"]
			content = data[key]["Content"]
			if(self.check(user_id, connect_id)):

				self.create_tables(user_id, connect_id)
				self.store_data(user_id, connect_id, message_type, content)
			else:
				print('there is something wrong')
if __name__ == '__main__':
	p = Chat()
	p.control("dt.json")

