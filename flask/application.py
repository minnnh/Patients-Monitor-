from flask import Flask, redirect, url_for, render_template, request
from flask_restful import Resource, Api, reqparse
import json
import sqlite3
import os
import sys

sys.path.insert(0, '../device_module')
from device_module import Device

application = Flask(__name__)
api = Api(application)

os.system('python ../device_module/table.py')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#db = os.path.join(BASE_DIR, '../device_module/table.db')
db = os.path.join(BASE_DIR, 'table.db')

col_users = ['User_id', 'Name', 'Date_of_Birth', 'Roles', 'Gender']
col_devices = ['Device_id', 'MAC', 'Date_of_Purchase', 'User_id', 'Fir_ver']
col_measurements = ['User_id', 'Weight', 'Height', 'Temperature', 'Systolic_Pressure', 'Diastolic_Pressure', 'Pulse', 'Oximeter', 'Glucometer']
col_assignments = ['Device_id', 'User_id', 'Assigner_id', 'Date_Assigned']
col_storage = ['Premission', 'User_id', 'Device_id', 'Roles']

def insert_data(table, new_data):
	data = tuple(list(new_data[table].values()))

	conn = sqlite3.connect(db) # table.db
	cur = conn.cursor()

	if(table == "Users"):
		sql_statement = 'INSERT INTO Users VALUES (?, ?, ?, ?, ?)'
		cur.executemany(sql_statement, [data])

	elif(table == "Devices"):
		sql_statement = 'INSERT INTO Devices VALUES (?, ?, ?, ?, ?)'
		cur.executemany(sql_statement, [data])

	elif(table == "Measurements"):
		sql_statement = 'INSERT INTO Measurements VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
		cur.executemany(sql_statement, [data])

	elif(table == "Assignments"):
		sql_statement = 'INSERT INTO Assignments VALUES (?, ?, ?, ?)'
		cur.executemany(sql_statement, [data])

	else:
		print("there is something wrong, please check your information")

	conn.commit()
	conn.close

def get_data(table, col):
	con = sqlite3.connect(db)
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	num = 1
	data = {}

	for row in cur.execute(f'SELECT * FROM {table}'):
		dic = {}
		for i in range(len(row)):
			dic[col[i]] = row[i]				
		data[f'number {num} user'] = dic
		num += 1

	con.commit()
	con.close
	return data

class Storage(Resource):
	def get(self):
		#get_data("Storage")
		return get_data("Storage", col_storage)
		# return col_storage
	def post(self):
		parser = reqparse.RequestParser()  # initialize

		for col in col_storage[1:]:
			parser.add_argument(col,required=True)

		args = parser.parse_args()  # parse arguments to dictionary

		new_data = {"Storage":{'User_id': int(args['User_id']),
					'Device_id': int(args['Device_id']),
					'Roles': args['Roles']}}
		new_json = json.dumps(new_data)

		with open('new_json.json', 'w') as outfile:
			json.dump(new_json, outfile)

		p = Device('new_json.json')
		#p.importdb("table.db")
		p.importdb(db)
		p.user_id = int(args['User_id'])
		p.device_id = int(args['Device_id'])
		p.role = args['Roles']
		#p.get_device(0)

		p.check_user_id()
		p.check_device_id()
		p.check_role()
		if ((p.check_user_id() and p.check_device_id() and p.check_role())!=True):
			return "There is something wrong in your infomation, please check it."
		
		conn = sqlite3.connect(db) # table.db
		cur = conn.cursor()
		cur.execute(f'INSERT INTO Storage VALUES ((SELECT MAX(Premission) + 1 FROM Storage),{p.user_id}, {p.device_id}, "{p.role}")')

		conn.commit()
		conn.close

		return new_data
		#return redirect(url_for("users"))

class Users(Resource):
	def get(self):
		return get_data("Users", col_users)

	def post(self):
		parser = reqparse.RequestParser()  # initialize
		for col in col_users:
			parser.add_argument(col,required=True)

		args = parser.parse_args()  # parse arguments to dictionary

		new_data = {"Users":{'User_id': int(args['User_id']),
					'Name': args['Name'],
					'Date_of_Birth': args['Date_of_Birth'],
					'Roles': args['Roles'],
					'Gender': args['Gender']}}

		insert_data("Users", new_data)

		return new_data

class Devices(Resource):
	def get(self):
		return get_data("Devices", col_devices)

	def post(self):
		parser = reqparse.RequestParser()  # initialize
		for col in col_devices:
			parser.add_argument(col,required=True)

		args = parser.parse_args()  # parse arguments to dictionary	

		new_data = {"Devices":{'Device_id': int(args['Device_id']),
					'MAC': args['MAC'],
					'Date_of_Purchase': args['Date_of_Purchase'],
					'User_id': int(args['User_id']),
					'Fir_ver': args['Fir_ver']}}

		insert_data("Devices", new_data)

		return new_data

class Measurements(Resource):
	def get(self):
		return get_data("Measurements", col_measurements)

	def post(self):
		parser = reqparse.RequestParser()  # initialize
		for col in col_measurements:
			parser.add_argument(col,required=True)

		args = parser.parse_args()  # parse arguments to dictionary	

		new_data = {"Measurements":{'User_id': int(args['User_id']),
					'Weight': float(args['Weight']),
					'Height': float(args['Height']),
					'Temperature': float(args['Temperature']),
					'Systolic_Pressure': float(args['Systolic_Pressure']),
					'Diastolic_Pressure': float(args['Diastolic_Pressure']),
					'Pulse': float(args['Pulse']),
					'Oximeter': float(args['Oximeter']),
					'Glucometer': float(args['Glucometer'])}}

		insert_data("Measurements", new_data)

		return new_data

class Assignments(Resource):
	def get(self):
		return get_data("Assignments", col_assignments)

	def post(self):
		parser = reqparse.RequestParser()  # initialize
		for col in col_assignments:
			parser.add_argument(col,required=True)

		args = parser.parse_args()  # parse arguments to dictionary	

		new_data = {"Assignments":{'Device_id': int(args['Device_id']),
					'User_id': int(args['User_id']),
					'Assigner_id': int(args['Assigner_id']),
					'Date_Assigned': args['Date_Assigned'],
					}}

		insert_data("Assignments", new_data)
		return new_data
    
api.add_resource(Storage, '/create')  # '/users' is our entry point for Users
api.add_resource(Users, '/users')  # and '/locations' is our entry point for Locations
api.add_resource(Devices, '/devices')
api.add_resource(Measurements, '/measurements')
api.add_resource(Assignments, '/assignments')

if __name__ == '__main__':
	#p = Device()
	application.run(debug=True)  # run our Flask app