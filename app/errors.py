from flask import render_template
from app import app, db


#  Кастомный хэндлер для ошибки 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


#  Кастомный хэндлер для ошибки 500
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
