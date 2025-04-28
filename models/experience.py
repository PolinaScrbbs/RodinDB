from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
)

from .result import Base


class TrainerExperience(Base):
    __tablename__ = "trainer_experiences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String(1024), nullable=False)
