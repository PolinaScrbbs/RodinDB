from sqlalchemy import Column, Integer, String, CHAR, Date, func, Enum, DateTime, ForeignKey

from database import Base, BaseEnum


class Role(BaseEnum):
    ADMIN = "Администратор"
    TRAINER = "Тренер"
    USER = "Пользователь"


class Gender(BaseEnum):
    MALE = "Мужчина"
    FEMALE = "Женщина"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone_number = Column(CHAR(11), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    patronymic = Column(String(30), default=None)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    gender = Column(Enum(Gender), default=Gender.MALE, nullable=False)
    date_of_birth = Column(Date, server_default=func.current_date(), nullable=False)
    avatar_url = Column(String(40), default="media/default.png")
    creation_at = Column(DateTime, default=func.current_time(), nullable=False)


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(256), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))