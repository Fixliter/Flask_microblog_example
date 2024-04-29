from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post

password_hashed = generate_password_hash('foobar')
print(password_hashed)
print(check_password_hash(password_hashed, 'foobar'))
print(check_password_hash(password_hashed, 'barfoo'))

u = User(username='Susan', email='susan@example.com')
u.set_password('mypassword')
print(u.check_password('anotherpassword'))
print(u.check_password('mypassword'))


