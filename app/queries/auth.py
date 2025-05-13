import bcrypt
from sqlalchemy import select
from ..models import User
from quart_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from datetime import datetime


async def registration(
    session, fullname, phone_number, password, date_of_birth, gender
):
    try:
        result = await session.execute(
            select(User).where(User.phone_number == phone_number)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            return None, "Пользователь с таким номером уже существует"

        parts = fullname.strip().split()
        if len(parts) < 2:
            return None, "Введите имя и фамилию"
        name, surname = parts[0], parts[1]
        patronymic = parts[2] if len(parts) > 2 else None

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User(
            phone_number=phone_number,
            hashed_password=hashed_password,
            name=name,
            surname=surname,
            patronymic=patronymic,
            gender=gender,
            date_of_birth=datetime.strptime(date_of_birth, "%Y-%m-%d").date(),
        )

        session.add(user)
        await session.commit()

        access_token = create_access_token(identity=user.id)
        return access_token, None

    except IntegrityError:
        await session.rollback()
        return None, "Ошибка: возможно, пользователь уже существует"
    except Exception as e:
        await session.rollback()
        return None, str(e)


async def login(session, phone_number: str, password: str):
    result = await session.execute(
        select(User).where(User.phone_number == phone_number)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return None, "Неверный номер телефона или пароль"

    if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        return None, "Неверный номер телефона или пароль"

    token = create_access_token(identity=user.id)
    return token, None
