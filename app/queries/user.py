from sqlalchemy import select
from ..models import User


async def get_user_by_id(session, user_id: int):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
