from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.orm import sessionmaker, declarative_base
import asyncio

# Путь к базе данных SQLite находится по адресу .\bot_administration\db.sqlite3
db_path = '../bot_administration/db.sqlite3'

# Создаем engine с использованием SQLite и указываем путь к базе данных
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# Создаем базовый класс для определения модели
Base = declarative_base()


# Определяем модель данных бота с настройками (пока что только состояния юзера)
class BotUserSettings(Base):
    __tablename__ = 'botuser_settings'
    tg_id = Column(Integer, primary_key=True)
    user_state = Column(String)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Пишет текущий стейт (название текущего подменю) юзера тг бота в таблицу
    @classmethod
    async def write_botuser_state(cls, tg_id, user_state):
        # Создаем таблицу в базе данных, если ее нет
        Base.metadata.create_all(engine, checkfirst=True)
        # Пишем
        user_to_update = cls.session.query(BotUserSettings).filter_by(tg_id=tg_id).first()
        if user_to_update:
            user_to_update.user_state = user_state
            cls.session.commit()
        else:
            new_settings = BotUserSettings(tg_id=tg_id, user_state=user_state)
            cls.session.add(new_settings)
            cls.session.commit()
        # Закрываем сессию
        cls.session.close()

    @classmethod
    async def read_botuser_state(cls, tg_id):
        # Чтение значения поля из таблицы
        user = cls.session.query(BotUserSettings).filter_by(tg_id=tg_id).first()
        # Закрываем сессию
        cls.session.close()
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
    auth_token = Column(String)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Проверка на то, что пользователь залогинился в тайге
    @classmethod
    async def is_botuser_logged_in(cls, tg_id):
        # Чтение значения поля из таблицы
        user = cls.session.query(LoginBotUser).filter_by(tg_id=tg_id).first()
        cls.session.close()
        if user:
            print(f"User found: TG ID: {user.tg_id}, Auth type: {user.auth_type}")
            return True
        else:
            print("User not found")
            return False

    # Метод обновления токенов. Ищет по старому токену, заменяет на новые
    @classmethod
    async def update_tokens(cls, old_refresh_token, new_refresh_token, auth_token):
        user = cls.session.query(LoginBotUser).filter_by(refresh_token=old_refresh_token).first()
        user.refresh_token = new_refresh_token
        user.auth_token = auth_token
        cls.session.commit()
        cls.session.close()

    # получает auth_token по tg_id
    @classmethod
    async def get_auth_token(cls, tg_id):
        user = cls.session.query(LoginBotUser).filter_by(tg_id=tg_id).first()
        cls.session.close()
        return user.auth_token

    # получает refresh_token по tg_id
    @classmethod
    async def get_refresh_token(cls, tg_id):
        user = cls.session.query(LoginBotUser).filter_by(tg_id=tg_id).first()
        cls.session.close()
        return user.refresh_token


# async def main():
#     await LoginBotUser.update_tokens(
#         "new_refresh2",
#         "new_refresh2",
#         "auth"
#     )
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()
