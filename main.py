from config import Config
from app import app, db


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host=Config.FLASK_APP_HOST,
            debug=Config.FLASK_DEBUG)
