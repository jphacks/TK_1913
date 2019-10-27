from datetime import datetime
from database import db

class Bow(db.Model):
    __tablename__ = "bows"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(127), nullable=False)
    macaddress = db.Column(db.String(31))
    path = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

