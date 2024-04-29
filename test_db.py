from app import app, db
from app.models import User, Post
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash

# Чтобы Flask и его расширения имели доступ к приложению Flask без необходимости передавать app в качестве аргумента
# в каждую функцию, создаем и передаем контекст приложения
app.app_context().push()


# @app.shell_context_processor
# def make_shell_context():
#     return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}


# Создаем тестовые записи Users
u = User(username='Konstantin', email='kostyan@example.com')
u.set_password('cat')
db.session.add(u)
db.session.commit()

u2 = User(username='Fedor', email='fefed@example.com')
u2.set_password('dog')
db.session.add(u2)
db.session.commit()

u3 = User(username='Susan', email='susan@example.com')
u3.set_password('mypass')
db.session.add(u3)
db.session.commit()

# Проверяем запись и получение данных разными способами
query = sa.select(User)
users = db.session.scalars(query).all()
print(users)

users = db.session.scalars(query)
for u in users:
    print(u.id, u.username)

u_ = db.session.get(User, 1)
print(u_)

# Создаем тестовый пост для u_
p = Post(body='my first post!', author=u_)
db.session.add(p)
db.session.commit()

u_ = db.session.get(User, 2)
print(u_)

p = Post(body='Wow, Amazing!', author=u_)
db.session.add(p)
db.session.commit()

u_ = db.session.get(User, 3)
print(u_)

p = Post(body="Let's get started", author=u_)
db.session.add(p)
db.session.commit()

# получаем посты для u_
query = u_.posts.select()
posts = db.session.scalars(query).all()
print(posts)

# получаем второго user
u = db.session.get(User, 2)
print(u)

# запрашиваем post второго user
query = u.posts.select()
posts = db.session.scalars(query).all()
print(posts)

# запрашиваем все post с указанием автора и id
query = sa.select(Post)
posts = db.session.scalars(query)
for p in posts:
    print(p.id, p.author.username, p.body)

# запрашиваем всех users по имени в алфавитном порядке
query = sa.select(User).order_by(User.username.desc())
print(db.session.scalars(query).all())

# запрашиваем всех users по имени, начинающиеся с f
query = sa.select(User).where(User.username.like('f%'))
print(db.session.scalars(query).all())

# запрашиваем всех users по имени, начинающиеся с k
query = sa.select(User).where(User.username.like('k%'))
print(db.session.scalars(query).all())


# проверка пароля (НЕДОДЕЛАНО)
u = db.session.get(User, 1)
query = u.password_hash.select()
password_hash = db.session.scalars(query)
print(posts)
