#encoding: utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'e_commerceweb'
USERNAME = 'root'
PASSWORD = '123'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,
DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOADED_IMAGES_DEST = os.path.join(basedir, '/images/')

