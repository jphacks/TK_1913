from flask_sqlalchemy import SQLAlchemy
from flask_migreate import Migrate

db = SQLAlchemy()
def init_db(app):
    db, init_app(app)
    Migrate(app, db)
