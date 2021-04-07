from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(filename='port_scanner.log', encoding='utf-8', level=logging.DEBUG)



app = Flask(__name__)
app.config['SECRET_KEY'] = '661a42c52c6b5583a9d4a10c65a9c968'
# using sql-lite for testing and postgres-sql in production -- sqlalchemy supports this seamlessly
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scanner.db'
# create the db instance
db = SQLAlchemy(app)


# to avoid circular import error
from flaskscanner import routes


db.create_all()
logging.debug("CREATED DATABASE: scanner.db")