from flask import Flask, redirect, url_for, render_template, request
from flask_restful import Resource, Api, reqparse
import json
import sqlite3
import os
from chat_module import Chat
import datetime

application = Flask(__name__)
api = Api(application)

if os.path.exists('chat_table.db'):
	os.remove('chat_table.db')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(BASE_DIR, 'chat_table.db')

p = Chat()
p.control('dt.json')

col_records = ['Record_Num', 'From_id', 'To_id', 'Message_Type', 'Content', 'Time']
col_connect = ['Record_Times', 'From_id', 'To_id', 'Message_Type', 'Content', 'Time']
co = ['User_id', 'Connect_id', 'Message_Type', 'Content', 'Time']

class Records(Resource):
	def get(self):
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('User_id', required=True)
		args = parser.parser_args()

		user_id = int(args['User_id'])
		table = f'User_{user_id}_Records'

		con = sqlite3.connect(db)
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		data = {}

		for row in cur.execute(f'SELECT * FROM {table}'):
			dic = {}
			for i in range(len(row)):
				dic[col_records[i]] = row[i]				
			data[f'number {user_id} user'] = dic
			#num += 1

		con.commit()
		con.close
		"""

		return p.table_rec

	def post(self):
		parser = reqparse.RequestParser()  # initialize
		for c in co[:-1]:
			parser.add_argument(c,required=True)

		args = parser.parse_args()

		user_id = int(args['User_id'])
		connect_id = int(args['Connect_id'])
		message_type = args['Message_Type']
		content = args['Content']
		#time = str(datetime.datetime.now())


		if(p.check(user_id, connect_id)):
			p.create_tables(user_id, connect_id)
			p.store_data(user_id, connect_id, message_type, content)
			data = {'Records':p.data_rec, 'Connects':p.data_con}
			return data

		else:
			return "things wrong"

api.add_resource(Records, '/chat') 
if __name__ == '__main__':
	application.run(debug=True)

