import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
# "UPLOADED_IMAGES must be same as UploadSet in image_helper"
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
