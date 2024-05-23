# Пример реализации микроблога на базе микрофреймворка Flask

За основу взята теория из  учебника по Flask от Мигеля Гринберга.

<p align="center">
<image src="/images/MicrBlg.jpg" alt="Welcome to microblog">
</p>

В планах было в учебных целях пописать что-то на Flask для "прочувствования" фреймворка и веб-программирования
<br>Ну что-то получилось =)<br>


**Ссылка на микроблог**: https://fixliter.pythonanywhere.com/

___

# 🔥 <span style="color: yellow">Features</span>

- базовый сайт с несколькими страницами и простой навигацией
- при первом открытии любой страницы сайта реализован запрос войти/авторизоваться или зарегистрироваться с последующим перенаправлением на вход
- сохранение данных зарегистрированных пользователей в БД (Sqlite)
- задумано, что будет страница главная(index) с отображением постов, страница входа (с формой Login), страница регистрации (с формой Register), страница профиля с возможностью редактирования (форма EditProfile), страница "About"
- при запросе иных адресов страниц будет отображение "Страница не найдена"
- в проект добавлена миграция БД, которая позволяет быстро актуализировать структуру БД по последним или выбранным изменениям
- дизайн с применением Bootsrtap
- на сайте реализовано три языка: Испанский, Русский(местами "специфичный перевод"), Английский(по умолчанию) для статичного текста, динамических полей в том числе и результатов работы функйи времени
- простой функционал подписок, счетчик подписок, подписавшихся
- генерация аватара
- размещение постов с пагинацией
- проверка пароля, восстановление пароля
- страница с ссылками на некоторые источники и инструменты, использовавшиеся для сайта


**Адреса**:

 - `'/index'`и `'/'` - главная страница
 - `"/about"` - информация о сайте, например правила поведения и размещения постов
 - `'/login'` - страница авторизации пользователя
 - `/logout` - выход из учетной записи(профиля).
 - `/register` - страница регистрации нового пользователя.
 - `/user/<username>` - страница профиля с отображением информации о пользователе и его постов.
 - `/edit_profile` - страница редактирования информации профиля (имя, о себе).
 - `/explore` - что-то вроде ленты всех постов



<p align="center">
<image src="/images/MicrBlg_2.jpg" alt="Welcome to microblog">
</p>

___

# 🛠️ <span style="color:red">Requirements</span>

- Python 3.11+
- SQLlite
alembic==1.13.1
Babel==2.15.0
blinker==1.8.0
click==8.1.7
colorama==0.4.6
dnspython==2.6.1
email_validator==2.1.1
Flask==3.0.3
Flask-Login==0.6.3
Flask-Mail==0.9.1
Flask-Migrate==4.0.7
Flask-Moment==1.0.5
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
greenlet==3.0.3
idna==3.7
itsdangerous==2.2.0
Jinja2==3.1.3
Mako==1.3.3
MarkupSafe==2.1.5
numpy==1.26.4
packaging==24.0
PyJWT==2.8.0
python-dotenv==1.0.1
SQLAlchemy==2.0.29
typing_extensions==4.11.0
Werkzeug==3.0.2
WTForms==3.1.2

___
# 🏗️ <span style="color:blue">Installation</span>

## Local

- Clone or download the repository.

    ```
    git clone git@github.com: https://github.com/Fixliter/Flask_microblog_example
    ```

- [Create virtual environment and activate it](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) and [install dependencies](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-requirements-files).

    ```
    $ flask run --port 5001 --debug - для отладки, при запуске в прод убрать
    $ python -m venv env (если желание работать через виртуальную среду)
    $ source env/bin/activate (если желание работать через виртуальную среду)
    $ pip install --upgrade pip && pip install -r requirements.txt
    $ flask db init (для активации работы с миграциями БД)
    $ flask db migrate (создает схему миграции)
    $ flask db upgrade (актуализирует БД по последней схеме миграции)
    $ flask db downgrade - для отката версии назад
    $ flaskdb downgrade base и затем $ flaskdb upgrade - для "реинкорнации" (чистая база) структуры базы данных к последней схеме миграции
    $ pybabel extract -F babel.cfg -k _l -o messages.pot .    - генерация общего шаблона для мультиязыков расширения .pot
    $ pybabel init -i messages.pot -d app/translations -l ru - создание директории и файла для компиляции перевода языка расширения .po
    $ pybabel compile -d app/translations    - компилировать трансляции для языков в файлы  расширения .mo
  Update translation with CLI:
    $ pybabel extract -F babel.cfg -k _l -o messages.pot .
    $ pybabel update -i messages.pot -d app/translations
    $ pybabel compile -d app/translations
    ```



<p align="center">
<image src="/images/MicrBlg_3.jpg" alt="Welcome to microblog"></a>
</p>  

# 🏃  <span style="color:deeppink">Start</span>

1. **$ flask run**: при успешной установке


___
# 💻 <span style="color:green">Structure</span>

1. **Головной файл microblog.py.**
2. **app** Пакет с необходимым набором компонентов для структуризации и наполнения страниц
2. **__init__** Для пакета app добавлен __init__ с импортом основных библиотек и регистрации/подключения классов этих библиотек в приложение
4. **templates.** содержит html шаблоны для страниц, применен base.html с основными блоками, в остальных шаблонах добавляется/расширяется контент к base
5. **static.** CSS и JS компоненты в основном для стилевых задач 
6. **forms.** Прописаны формы, применяющиеся на сайте 
7. **models.** Описаны модели базы данных, хэширование и проверка паролей. 
8. **routes** Описаны обработчики endpoints, рендер
9. **.flaskenv** Регистрация приложения в переменной окружения flask: FLASK_APP=microblog.py. Позволяет запускать приложение командой flask run без присваивания переменной окружения при каждом сеансе терминала
10. **сonfig** Задается SECRET_KEY и SQLALCHEMY_DATABASE_URI
10. **test_avatar** Просто для ручного теста получения аватара
10. **test_db** Просто для ручного теста некоторых запросов в БД
10. **test_hash_password** Просто тестирование функционала хэширования пароля
10. **microblog** В основном для создания контекст оболочки, который добавляет экземпляр базы данных и модели в сеанс оболочки, а также импорт некоторых модулей и библиотек, например CLI для возможности использовать сокращенные команды терминала
10. **messages.pot** Общий шаблон для последующего создания файлов конфигурации перевода для конкретного языка
10. **babel.cfg** Конфигуратор с пометками в каких файлах искать метки перевода на другой язык
10. **app.db** База данных SQlite
10. **logs** Логи
10. **tests** Тесты на базу Unittest для некоторого функционала
10. **errors** Придание ошибкам единого стиля сайта через хэндлеры и применение шаблонов
10. **email** Функционал отправки писемва случае оповещения администратора об ошибках на сервере и отправка письма для сброса пароля. Но не работает, так как не настроен бесплатный SMTP
10. **cli** Command-Line Enhancements для использования сокращенных настроенных команд терминала
10. **translations** Директория с поддиректориями для каждого языка, содержащие два файла: файл шаблона-конфигурации перевода .po и скомпилированный из него файл .mo, использующийся веб-сайтом
 

    

# Данные

**Структура DB:**
<p align="center">
<image src="/images/Post_db.jpg" alt="Welcome to microblog">
</p>
```

```db
// Table - User 
// Model:
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')
}
```
```db
// Table - Post 
// Model:
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')
}
```

***
# 🙇 <span style="color:purple">To_do and to_improve</span>

- **try/Except**: Структуру хотелось бы сделать с try/Except блоками по кодам ошибок для большей отслеживаемости и надежности
- **async**: Добавить асинхрон
- **types**: Добавить аннотацию типов для более прозрачной и удобной работы
- **comments**: Добавить функционал добавления комментариев к постам
- **likes**: Добавить функционал добавления лайков к постам
- **media**: Добавить функционал использования медиа в постах(фото, картинки, видео, аудио)
- **test**: Добавить больше автотестов на содержательную часть
- **attract**: Добавить больше привлекательности дизайну



<p align="center">
<image src="/images/close_laptop.jpg" alt="Welcome to microblog">
</p>