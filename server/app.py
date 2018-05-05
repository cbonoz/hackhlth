from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
import json

DB_USER = os.environ['STIM_DB_USER']
DB_PASS = os.environ['STIM_DB_PASS']

softheon_client = os.environ['SOFTHEON_CLIENT_ID']
softheon_secret = os.environ['SOFTHEON_CLIENT_SECRET']
DB_HOST = "localhost"
PORT = '5432'
APP_PORT = 3000

DB_STRING = "postgres://%s:%s@%s:%s/stim" % (DB_USER, DB_PASS, DB_HOST, PORT)
# print(DB_STRING)

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

from softheon import Softheon

db.create_all()

scopes = "enterpriseapi" #openid
print('softheon info', softheon_client, softheon_secret)

softheon = Softheon(softheon_client, softheon_secret, scopes)

@app.route('/')
def hello():
    return "Hello World!"

"""
POST REQUESTS
"""

@app.route('/accel', methods=['POST'])
def parse_accel():
    try:
        body = json.loads(request.data)
        data = body['data']
        print(data)
        data = list(map(lambda val: Accel(x=val['x'], y=val['y'], z=val['z'], timestamp=val['timestamp']), data))
        db.session.add_all(data)
        db.session.commit()

        return jsonify({'inserted': len(data)})
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/gyro', methods=['POST'])
def parse_gyro():
    try:
        body = json.loads(request.data)
        data = body['data']
        data = list(map(lambda val: Gyro(x=val['x'], y=val['y'], z=val['z'], timestamp=val['timestamp']), data))
        print(data)
        db.session.add_all(data)
        db.session.commit()

        return jsonify({'inserted': len(data)})
    except Exception as e:
        print(e)
        return jsonify(e)

"""
GET REQUESTS
"""

@app.route('/accel')
def get_accel():
    try:
        # from query string
        start_time = request.args.get('startTime')
        end_time = request.args.get('endTime')
        data = db.session.query(Accel).filter(
            (Accel.timestamp >= start_time) & (Accel.timestamp <= end_time)
        )
        records = [i.serialize for i in data]
        return jsonify(data = records)
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/gyro')
def get_gyro():
    try:
        # from query string
        start_time = request.args.get('startTime')
        end_time = request.args.get('endTime')
        data = db.session.query(Gyro).filter(
            (Gyro.timestamp >= start_time) & (Gyro.timestamp <= end_time)
        )
        records = [i.serialize for i in data]
        return jsonify(data = records)
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/accel/all')
def get_accel_all():
    try:
        data = Accel.query.all()
        records = [i.serialize for i in data]
        return jsonify(data = records)
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/gyro/all')
def get_gyro_all():
    try:
        data = Gyro.query.all()
        records = [i.serialize for i in data]
        return jsonify(data = records)
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/stim/all')
def get_stim_all():
    try:
        userId = request.args.get('userId')
        response = softheon.get_stim_events({'userId': userId})
        data = response.text
        print(data)
        records = [i.serialize for i in data]
        return jsonify(data = records)
    except Exception as e:
        print(e)
        return jsonify(e)

if __name__ == '__main__':
    app.run(port=APP_PORT)
    print('App running on port %s' % APP_PORT)