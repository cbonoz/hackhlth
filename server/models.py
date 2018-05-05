from app import db
from sqlalchemy.dialects.postgresql import JSON

class Accel(db.Model):
    __tablename__ = 'accel'

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float())
    y = db.Column(db.Float())
    z = db.Column(db.Float())
    timestamp = db.Column(db.Float())

    def __repr__(self):
        return 'Accel<id {}>'.format(self.id)

class Gyro(db.Model):
    __tablename__ = 'gyro'

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float())
    y = db.Column(db.Float())
    z = db.Column(db.Float())
    timestamp = db.Column(db.Float())

    def __repr__(self):
        return 'Gyro<id {}>'.format(self.id)