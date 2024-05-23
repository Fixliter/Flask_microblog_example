# -*- coding: utf-8 -*-
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db, cli
from app.models import User, Post


# создаем контекст оболочки, который добавляет экземпляр базы данных и модели в сеанс оболочки:
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

# app = Flask(__name__)
#
# if __name__ == "__main__":
#     app.run(debug=True)
