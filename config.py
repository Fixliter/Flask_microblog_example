import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Параметры SMTP для рассылки оповещений по электронной почте
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['anton_krayushkin@mail.ru']

    # для настройки количества постов на странице в рамках пагинации
    POSTS_PER_PAGE_INDEX = 10
    POSTS_PER_PAGE_EXPLORE = 15
    POSTS_PER_PAGE_PROFILE = 10

    # управления языками сайта
    LANGUAGES = ['en', 'ru']
