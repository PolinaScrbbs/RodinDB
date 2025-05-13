from sqlalchemy import (
    Column,
    Integer,
    String,
    CHAR,
    Date,
    func,
    Enum,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import object_session, validates, relationship

from app.database import Base, BaseEnum


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
    trainer_id = Column(Integer, ForeignKey("users.id"), default=None)
    date_of_birth = Column(Date, server_default=func.current_date(), nullable=False)
    is_regular_client = Column(Boolean, default=False, nullable=False)
    avatar_url = Column(String(40), default="media/default.png")
    creation_at = Column(DateTime, default=func.now(), nullable=False)

    @validates("trainer_id")
    def validate_trainer_id(self, trainer_id):
        if trainer_id is not None:
            session = object_session(self)
            trainer = session.query(User).filter_by(id=trainer_id).first()
            if not trainer:
                raise ValueError(f"Тренер с id={trainer_id} не найден.")
            if trainer.role != Role.TRAINER:
                raise ValueError(
                    f"Пользователь с id={trainer_id} не является тренером."
                )
        return trainer_id

    trainer = relationship("User", remote_side=[id], backref="clients")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(256), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
