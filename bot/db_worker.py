from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Путь к базе данных SQLite находится по адресу .\bot_administration\db.sqlite3
db_path = r'..\bot_administration\db.sqlite3'

# Создаем engine с использованием SQLite и указываем путь к базе данных
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# Создаем базовый класс для определения модели
Base = declarative_base()

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()


# Определяем модель данных бота с настройками (пока что только состояния юзера)
class BotUserSettings(Base):
    __tablename__ = 'botuser_settings'
    tg_id = Column(Integer, primary_key=True)
    user_state = Column(String)

    # Пишет текущий стейт (название текущего подменю) юзера тг бота в таблицу
    @classmethod
    async def write_botuser_state(cls, tg_id, user_state):
        # Создаем таблицу в базе данных, если ее нет
        Base.metadata.create_all(engine, checkfirst=True)
        new_settings = BotUserSettings(tg_id=tg_id, user_state=user_state)
        cls.session.add(new_settings)
        cls.session.commit()


# Определяем модель данных django с токенами
class LoginBotUser(Base):
    __tablename__ = 'login_botuser'
    id = Column(Integer, primary_key=True)
    domain = Column(String)
    auth_type = Column(String)
    application_token = Column(String)
    refresh_token = Column(String)
    tg_id = Column(Integer)


# Пишет текущий стейт (название текущего подменю) юзера тг бота в таблицу
async def is_botuser_logged_in(tg_id):
    # Чтение значения поля из таблицы
    user = session.query(LoginBotUser).filter_by(tg_id=tg_id).first()
    if user:
        print(f"User found: TG ID: {user.tg_id}, Auth type: {user.auth_type}")
    else:
        print("User not found")
    return True

# Закрываем сессию
session.close()
