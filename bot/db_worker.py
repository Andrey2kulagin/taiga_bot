from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import asyncio

# Путь к базе данных SQLite находится по адресу .\bot_administration\db.sqlite3
db_path = r'..\bot_administration\db.sqlite3'

# Создаем engine с использованием SQLite и указываем путь к базе данных
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# Создаем базовый класс для определения модели
Base = declarative_base()


# Определяем модель данных бота с настройками (пока что только состояния юзера)
class BotUserSettings(Base):
    __tablename__ = 'botuser_settings'
    tg_id = Column(Integer, primary_key=True)
    user_state = Column(String)

    # Пишет текущий стейт (название текущего подменю) юзера тг бота в таблицу
    @classmethod
    async def write_botuser_state(cls, tg_id, user_state):
        # Создаем сессию
        # TODO: убрать дубликат кода
        Session = sessionmaker(bind=engine)
        session = Session()
        # Создаем таблицу в базе данных, если ее нет
        Base.metadata.create_all(engine, checkfirst=True)
        # Пишем
        user_to_update = session.query(BotUserSettings).filter_by(tg_id=tg_id).first()
        if user_to_update:
            user_to_update.user_state = user_state
            session.commit()
        else:
            new_settings = BotUserSettings(tg_id=tg_id, user_state=user_state)
            session.add(new_settings)
            session.commit()
        # Закрываем сессию
        session.close()

    @classmethod
    async def read_botuser_state(cls, tg_id):
        # Создаем сессию
        # TODO: убрать дубликат кода
        Session = sessionmaker(bind=engine)
        session = Session()
        # Чтение значения поля из таблицы
        user = session.query(BotUserSettings).filter_by(tg_id=tg_id).first()
        # Закрываем сессию
        session.close()
        return user.user_state


# Определяем модель данных django с токенами
class LoginBotUser(Base):
    __tablename__ = 'login_botuser'
    id = Column(Integer, primary_key=True)
    domain = Column(String)
    auth_type = Column(String)
    application_token = Column(String)
    refresh_token = Column(String)
    tg_id = Column(Integer)

    # Проверка на то, что пользователь залогинился в тайге
    @classmethod
    async def is_botuser_logged_in(cls, tg_id):
        # Создаем сессию
        # TODO: убрать дубликат кода
        Session = sessionmaker(bind=engine)
        session = Session()
        # Чтение значения поля из таблицы
        user = session.query(LoginBotUser).filter_by(tg_id=tg_id).first()
        session.close()
        if user:
            print(f"User found: TG ID: {user.tg_id}, Auth type: {user.auth_type}")
            return True
        else:
            print("User not found")
            return False
        # Закрываем сессию

