from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #, MigrateCommand
# from flask_script import Manager
import sys
sys.path.append("..")


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@flask-db/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# handler = Manager(app)
# handler.add_command('db', MigrateCommand)
migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    identity_number = db.Column(db.Integer())

