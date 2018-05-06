from app import db
import json
from sqlalchemy.dialects.postgresql import JSON

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
        return {'x': self.x, 'y': self.y, 'z': self.z, 'userId':self.userId, 'timestamp': int(self.timestamp)}

    def __repr__(self):
        return "%s" % {'x': self.x, 'y': self.y, 'z': self.z, 'userId':self.userId, 'timestamp': int(self.timestamp)}

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
        return {'x': self.x, 'y': self.y, 'z': self.z, 'userId':self.userId, 'timestamp': int(self.timestamp)}

    def __repr__(self):
        return "%s" % {'x': self.x, 'y': self.y, 'z': self.z, 'userId':self.userId, 'timestamp': int(self.timestamp)}
