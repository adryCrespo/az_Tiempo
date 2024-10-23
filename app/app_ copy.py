from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
# from config import Config
from http import HTTPStatus
from sqlalchemy import text
import json

def create_app(db):
        app = Flask(__name__)
        # app.config.from_object("config.Config")

        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@flask-db/users'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        db.init_app(app)

        migrate = Migrate(app=app,db=db)
        return app

app = Flask(__name__)
        # app.config.from_object("config.Config")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@flask-db:3306/users'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db.init_app(app)
db = SQLAlchemy(app)

# migrate = Migrate(app=app,db=db)
# app = create_app(db)

@app.route('/') 
def home(): 
    return 'This is the home page' 

@app.route('/hello') 
def hello():
     return 'Hello'

@app.route('/v1/users/<user_id>', methods=['GET'])
def get_user_details(user_id):
    try:
        sql = text('SELECT * FROM users WHERE id=:id_num')
        with db.engine.begin() as conn:
            result = conn.execute(sql, id_num=user_id).fetchone()
        # result = db.engine.execute(sql, id_num=user_id).fetchone()
        return json.dumps({"name": result.name, "surname": result.surname, "identity_number": result.identity_number,}), HTTPStatus.OK
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND