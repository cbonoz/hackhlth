from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine

DB_USER = os.environ['STIM_DB_USER']
DB_PASS = os.environ['STIM_DB_PASS']
DB_HOST = "localhost"
PORT = '5432'

if not DB_USER:
    DB_USER = "postgres"
if not DB_PASS:
    DB_PASS = "admin"

DB_STRING = "postgres://%s:%s@%s:%s/compose" % (DB_USER, DB_PASS, DB_HOST, PORT)

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Accel, Gyro

@app.route('/')
def hello():
    return "Hello World!"

"""
POST REQUESTS
"""

@app.route('/accel', methods=['POST'])
def parse_accel():
    data = request.data
    print(data)
    return jsonify({data: len(data)})

@app.route('/gyro', methods=['POST'])
def parse_gyro():
    data = request.data
    print(data)
    return jsonify({data: len(data)})

"""
GET REQUESTS
"""

@app.route('/accelerometer')
def get_accel():
    # from query string
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    # TODO: fetch data between startTime and endTime timestamps.
    data = []
    print(data)
    return jsonify({data: len(data)})

@app.route('/gyroscope')
def get_accel():
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    # TODO: fetch data between startTime and endTime timestamps.
    data = []
    print(data)
    return jsonify({data: len(data)})

if __name__ == '__main__':
    app.run()