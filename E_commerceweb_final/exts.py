# encoding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
db = SQLAlchemy()
images = UploadSet('images', IMAGES)