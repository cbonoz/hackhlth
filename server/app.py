from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_pushjack import FlaskAPNS
from sqlalchemy.dialects.postgresql import JSON

from predict import Predict
from notification import NotificationService, DEV_CERT_FILE, KEY_FILE, PROD_CERT_FILE

from colorama import Fore, Back, Style
from colorama import init

init()

config = {
    'APNS_CERTIFICATE': DEV_CERT_FILE
}

import os
import json
import time

DB_USER = os.environ['STIM_DB_USER']
DB_PASS = os.environ['STIM_DB_PASS']

DB_HOST = "localhost"
PORT = '5432'
APP_PORT = 9001

DB_STRING = "postgres://%s:%s@%s:%s/stim" % (DB_USER, DB_PASS, DB_HOST, PORT)
print('db', DB_STRING)

app = Flask(__name__)
app.config.update(config)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

apns_client = FlaskAPNS()
apns_client.init_app(app)

CORS(app)

db = SQLAlchemy(app)


class Accel(db.Model):
    __tablename__ = 'accel'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String())
    x = db.Column(db.Float())
    y = db.Column(db.Float())
    z = db.Column(db.Float())
    timestamp = db.Column(db.Float())

    @property
    def serialize(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'userId': self.userId, 'timestamp': int(self.timestamp)}

    def __repr__(self):
        return "%s" % {'x': self.x, 'y': self.y, 'z': self.z, 'userId': self.userId, 'timestamp': int(self.timestamp)}


class Gyro(db.Model):
    __tablename__ = 'gyro'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String())
    x = db.Column(db.Float())
    y = db.Column(db.Float())
    z = db.Column(db.Float())
    timestamp = db.Column(db.Float())

    @property
    def serialize(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'userId': self.userId, 'timestamp': int(self.timestamp)}

    def __repr__(self):
        return "%s" % {'x': self.x, 'y': self.y, 'z': self.z, 'userId': self.userId, 'timestamp': int(self.timestamp)}


class StimEvent(db.Model):
    __tablename__ = 'stimevent'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String())
    timestamp = db.Column(db.Float())

    @property
    def serialize(self):
        return {'userId': self.userId, 'timestamp': int(self.timestamp)}

    def __repr__(self):
        obj = {'userId': self.userId, 'timestamp': int(self.timestamp)}
        return "%s" % obj


db.create_all()
predict = Predict()
ns = NotificationService()


@app.route('/hello')
def hello():
    return "Hello World!"


"""
POST REQUESTS
"""


@app.route('/predict', methods=['POST'])
def parse_data():
    try:
        # body = json.loads(request.data)
        body = request.get_json()
        # print('request predict', body)

        accel = body['accel']
        gyro = body['gyro']
        insert = False
        # try:
        #     insert = body['insert']
        # except KeyError as e:
        #     insert = False

        userId = '1'
        try:
            userId = body['userId']
        except KeyError as e:
            userId = '1'

        type = None
        try:
            type = body['type']
            # there is a type declared
            fd = open('./ml/data/accel_data_%s.txt' % type, 'a')
            text = '\n'.join(list(map(lambda val: "%s %s %s %s" % (val['x'], val['y'], val['z'], val['timestamp']), accel))) + "\n"
            fd.write(text)
            fd.close()

            fd = open('./ml/data/gyro_data_%s.txt' % type, 'a')
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
        # print('running prediction on test_data shape', test_data.shape)
        print("\n%s\n" % test_data[['accel-std-x', 'accel-std-y', 'accel-std-z']])
        prediction = predict.predict_stim(userId, test_data)
        print('new_stim', new_stim)
        if prediction and new_stim:  # if we just had an upward spike
            # We had a stimming event detection, record to softheon using the current time of detection.
            detection_time = int(time.time())
            stim_event = StimEvent(userId=userId, timestamp=detection_time)
            print("Stim event created: %s" % stim_event)
            # Broadcast the stim event.
            with app.app_context():
                # Send to single device.
                res = apns_client.send(ns.get_token(userId), "Stimming detected for ID(%s)." % userId)
                print('apns', res.__dict__)
            ns.send_notification(userId, "Detected Stim Event: %d" % detection_time)

        return jsonify({'inserted': inserted, 'prediction': prediction})
    except Exception as e:
        print(e)
        return jsonify(e)


@app.route('/accel', methods=['POST'])
def parse_accel():
    try:
        body = request.get_json()
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
        body = request.get_json()
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
        accel_std = 0
        if userId in predict.last_prediction:
            last_pred = predict.last_prediction[userId]
            val = last_pred['pred'] + 0
            accel_std = last_pred['accel-std']
        status_json = {'status': val, 'accel-std': accel_std}
        print(status_json)
        return jsonify(status_json)
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
        return jsonify({'userId': userId, 'token': token})
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
        return jsonify(data=records)
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
        return jsonify(data=records)
    except Exception as e:
        print(e)
        return jsonify(e)


@app.route('/accel/all')
def get_accel_all():
    try:
        data = Accel.query.all()
        records = [i.serialize for i in data]
        return jsonify(data=records)
    except Exception as e:
        print(e)
        return jsonify(e)


@app.route('/gyro/all')
def get_gyro_all():
    try:
        data = Gyro.query.all()
        records = [i.serialize for i in data]
        return jsonify(data=records)
    except Exception as e:
        print(e)
        return jsonify(e)


@app.route('/stim/all')
def get_stim_all():
    try:
        userId = request.args.get('userId')
        if userId:
            data = StimEvent.query.filter_by(userId=userId).all()
        else:
            data = StimEvent.query.all()
        records = [i.serialize for i in data]
        # print('userId', userId, records)
        return jsonify(data=records)
    except Exception as e:
        print(e)
        return jsonify(e)


if __name__ == '__main__':
    app.run(port=APP_PORT)
    print('App running on port %s' % APP_PORT)
