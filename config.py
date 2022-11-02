import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    try:
        SECRET_KEY = os.environ.get("SECRET_KEY")
    except:
        SECRET_KEY ="9eee204f49f041e7977d9fcaf4643f04" 
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'Webeee_datas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "static/img/posts"