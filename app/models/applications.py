from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    CheckConstraint,
    Enum,
    DateTime,
    func,
)

from app.database import BaseEnum
from .experience import Base


class ApplicationStatus(BaseEnum):
    SENT = "Отправлен"
    ADOPTED = "Принят"
    REJECTED = "Отклонён"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    status = Column(
        Enum(ApplicationStatus), default=ApplicationStatus.SENT, nullable=False
    )
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sending_reason = Column(String(120), nullable=False)
    refusal_reason = Column(String(120), default=None)
    created_at = Column(DateTime, default=func.current_time(), nullable=False)

    __table_args__ = (
        CheckConstraint("client_id != trainer_id", name="check_client_not_trainer"),
    )
