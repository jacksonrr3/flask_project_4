from flask import Flask

from config import Config
from models import db, Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()

from views import *

if __name__ == "__main__":
    app.run()


