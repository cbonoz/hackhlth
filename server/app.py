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

DB_STRING = "postgres://%s:%s@%s:%s/compose" % (DB_USER, DB_PASS, DB_HOST, PORT)

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Accel
from models import Gyro
from softheon import Softheon

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
        print(body)
        data = body['data']
        print(data)
        # TODO: save to accel DB.
        db.session.add(data)

        return jsonify({'data': len(data)})
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/gyro', methods=['POST'])
def parse_gyro():
    try:
        body = json.loads(request.data)
        print(body)
        data = body['data']
        print(data)
        # TODO: save to gyro DB.
        db.session.add(data)

        return jsonify({'data': len(data)})
    except Exception as e:
        print(e)
        return jsonify(e)

"""
GET REQUESTS
"""

@app.route('/accel')
def get_accel():

    # from query string
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    # TODO: fetch data between startTime and endTime timestamps.

    data = []
    print(data)
    return jsonify({data: len(data)})

@app.route('/gyro')
def get_gyro():
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    # TODO: fetch data between startTime and endTime timestamps.
    db.session.add(data)
    data = []
    print(data)
    return jsonify({data: len(data)})

@app.route('/accel/all')
def get_accel_all():
    data = Accel.query.all()
    return jsonify({data: data})

@app.route('/gyro/all')
def get_gyro_all():
    data = Gyro.query.all()
    return jsonify({data: data})

@app.route('/stim/all')
def get_stim_all():
    userId = request.args.get('userId')
    response = softheon.get_stim_events({'userId': userId})
    return jsonify({data: data})

if __name__ == '__main__':
    app.run(port=APP_PORT)
    print('App running on port %s' % APP_PORT)