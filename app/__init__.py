# -*- coding: utf-8 -*-
from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l


def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    # return "ru"
    return "ru"


app = Flask(__name__)  # инициализация самого Flask app
app.config.from_object(Config)  # файл конфигурации подаем для построения соответствущих вещей
db = SQLAlchemy(app)  # для работы с БД
migrate = Migrate(app, db) # для создания схемы миграции базы данных
login = LoginManager(app)  # для логирвоания
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')  # перезапись стандартного сообщения для дальнейшей
# возможности перевести на другой язык
mail = Mail(app)  # Для SMTP рассылок
moment = Moment(app)  # {yyyy}-{mm}-{dd}T{hh}:{mm}:{ss}{tz}
babel = Babel(app, locale_selector=get_locale)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_USERNAME'],
            # fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.INFO)
        app.logger.addHandler(mail_handler)

    #  Создаем директорию log и записываем логи, используя RotatingFileHandler, настроенные на 10КБ объем и 10 файлов бэкапов
    #  Уровень записи логов - ИНФО
    #  Записываем строку с timestamp, уровнем лога, сообщением, файлом и линией источника внимания
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors

# print(app.config['SECRET_KEY'])
