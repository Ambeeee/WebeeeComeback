from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.secret_key = "6414" #prima o poi la tolgo
app.config.from_object(Config)


#DATABASE
db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch = True)
    else:
        migrate.init_app(app, db)





from blog import models, routes
