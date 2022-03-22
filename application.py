from flask import Flask, redirect, url_for, render_template, request
from flask_restful import Resource, Api, reqparse
import json
import sqlite3
import os
from flask_chat import *
from flask_device import *
import datetime

application = Flask(__name__)
api = Api(application)

@application.route("/")
def home():
	return render_template("index.html")



api.add_resource(Records, '/chat') 
api.add_resource(Storage, '/create')  # '/users' is our entry point for Users
api.add_resource(Users, '/users')  # and '/locations' is our entry point for Locations
api.add_resource(Devices, '/devices')
api.add_resource(Measurements, '/measurements')
api.add_resource(Assignments, '/assignments')

if __name__ == '__main__':
	application.run(debug=True)