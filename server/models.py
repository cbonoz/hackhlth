from app import db
import json
from sqlalchemy.dialects.postgresql import JSON

class Accel(db.Model):
    __tablename__ = 'accel'

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float())
    y = db.Column(db.Float())
    z = db.Column(db.Float())
    timestamp = db.Column(db.Float())

    # def __repr__(self):
    #     return json.dumps(self.__dict__)

    @property
    def serialize(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'timestamp': int(self.timestamp)}

    def __repr__(self):
        return "%s" % {'x': self.x, 'y': self.y, 'z': self.z, 'timestamp': int(self.timestamp)}

class Gyro(db.Model):
    __tablename__ = 'gyro'

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float())
    y = db.Column(db.Float())
    z = db.Column(db.Float())
    timestamp = db.Column(db.Float())

    @property
    def serialize(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'timestamp': int(self.timestamp)}

    def __repr__(self):
        return json.dumps(self.__dict__)

    # def __repr__(self):
    #     return '{"x": %f, "y": %f, "z": %f, "timestamp": %d}' % (self.x, self.y, self.z, int(self.timestamp))
