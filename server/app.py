from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_pushjack import FlaskAPNS

from softheon import Softheon
from predict import Predict
from notification import NotificationService, DEV_CERT_FILE, KEY_FILE, PROD_CERT_FILE
from models import *

from colorama import Fore, Back, Style
from colorama import init
init()

config = {
    'APNS_CERTIFICATE': PROD_CERT_FILE
}

import os
import json
import time

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
app.config.update(config)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


apns_client = FlaskAPNS()
apns_client.init_app(app)

CORS(app)

db = SQLAlchemy(app)

db.create_all()

predict = Predict()
ns = NotificationService()
softheon = Softheon(softheon_client, softheon_secret)


@app.route('/')
def hello():
    return "Hello World!"

"""
POST REQUESTS
"""

@app.route('/predict', methods=['POST'])
def parse_data():
    try:
        body = json.loads(request.data)

        accel = body['accel']
        gyro = body['gyro']
        insert = False
        try:
            insert = body['insert']
        except KeyError as e:
            insert = False

        userId = '1'
        try:
            userId = body['userId']
        except KeyError as e:
            userId = '1'

        type = None
        try:
            type = body['type']
            # there is a type declared
            fd = open('./ml/data/accel_data_%s.txt' % type,'a')
            text = '\n'.join(list(map(lambda val: "%s %s %s %s" % (val['x'], val['y'], val['z'], val['timestamp']), accel))) + "\n"
            fd.write(text)
            fd.close()

            fd = open('./ml/data/gyro_data_%s.txt' % type,'a')
            text = '\n'.join(list(map(lambda val: "%s %s %s %s" % (val['x'], val['y'], val['z'], val['timestamp']), gyro))) + "\n"
            fd.write(text)
            fd.close()

        except KeyError as e:
            print('no type declared - not training, in live mode.')
            type = None

        print('insert', insert, 'userId', userId, 'accel', len(accel), 'gyro', len(gyro), 'type', type)

        # See if the data should be inserted as well.
        if insert:
            accel_data = list(map(lambda val: Accel(x=val['x'], y=val['y'], z=val['z'], userId=val['userId'], timestamp=val['timestamp']), accel))
            db.session.add_all(accel_data)
            db.session.commit()

            gyro_data = list(map(lambda val: Gyro(x=val['x'], y=val['y'], z=val['z'], userId=val['userId'], timestamp=val['timestamp']), gyro))
            db.session.add_all(gyro_data)
            db.session.commit()
            inserted = len(accel) + len(gyro)
        else:
            inserted = 0

        test_data = predict.process_data(accel, gyro)
        new_stim = predict.is_new_stim(userId)
        prediction = predict.predict_stim(userId, test_data)
        print('new_stim', new_stim)
        if prediction and new_stim: # if we just had an upward spike
            # We had a stimming event detection, record to softheon using the current time of detection.
            detection_time = int(time.time())
            try:
                softheon.send_stim_event(userId, detection_time)
            except Exception as e:
                # Auth token likely expired, but try again.
                softheon.get_auth_token()
                response = softheon.send_stim_event(userId, detection_time)
            print("Entry created in softheon DB")

            with app.app_context():
                # Send to single device.
                res = apns_client.send(ns.get_token(userId), "Stimming detected for %s" % userId)
                print('apns', res.__dict__)
            # ns.send_notification(userId, "Detected Stim Event: %d" % detection_time)

        return jsonify({'inserted': inserted, 'prediction': prediction})
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/accel', methods=['POST'])
def parse_accel():
    try:
        body = json.loads(request.data)
        data = body['data']
        print(data)
        data = list(map(lambda val: Accel(x=val['x'], y=val['y'], z=val['z'], userId=val['userId'], timestamp=val['timestamp']), data))
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
        data = list(map(lambda val: Gyro(x=val['x'], y=val['y'], z=val['z'], userId=val['userId'], timestamp=val['timestamp']), data))
        db.session.add_all(data)
        db.session.commit()

        return jsonify({'inserted': len(data)})
    except Exception as e:
        print(e)
        return jsonify(e)

"""
GET REQUESTS
"""

@app.route('/status')
def get_status():
    try:
        # from query string
        userId = request.args.get('userId')
        val = 0
        if userId in predict.last_prediction:
            val = predict.last_prediction[userId] + 0
        return jsonify({'status':val})
    except Exception as e:
        print(e)
        return jsonify(e)

@app.route('/register')
def get_register():
    try:
        # from query string
        userId = request.args.get('userId')
        token = request.args.get('token')
        ns.register_token(userId, token)
        return jsonify({'userId':userId, 'token': token})
    except Exception as e:
        print(e)
        return jsonify(e)

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
        token = softheon.get_auth_token()
        response = softheon.get_stim_events()
        data = response.text
        # records = [i.serialize for i in data]
        print("fetched %d stimming records" % len(data))
        return jsonify(data = data)
    except Exception as e:
        print(e)
        return jsonify(e)

if __name__ == '__main__':
    app.run(port=APP_PORT)
    print('softheon info', softheon_client, softheon_secret)
    print('App running on port %s' % APP_PORT)