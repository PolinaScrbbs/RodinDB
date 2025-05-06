from datetime import timedelta

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    CheckConstraint,
    Enum,
    Date,
    Table,
    DateTime,
    Interval,
)

from utils import get_start_date, get_end_date
from .applications import Base, BaseEnum


training_plan_clients = Table(
    "training_plan_clients",
    Base.metadata,
    Column(
        "training_plan_id", Integer, ForeignKey("training_plans.id", ondelete="CASCADE")
    ),
    Column("client_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
)


class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)
    descriptions = Column(String(150), default=None)
    start_date = Column(Date, default=get_start_date, nullable=False)
    end_date = Column(Date, default=get_end_date)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class ExerciseType(BaseEnum):
    SQUATS = "Приседания"
    PUSH_UPS = "Отжимания"
    RUNNING = "Бег"


class TrainingPlanExercise(Base):
    __tablename__ = "training_plan_exercises"

    training_plan_id = Column(
        Integer, ForeignKey("training_plans.id", ondelete="CASCADE"), primary_key=True
    )

    type = Column(Enum(ExerciseType), nullable=False)
    approaches_number = Column(Integer, nullable=False, default=2)
    repetitions_number = Column(Integer, nullable=False, default=20)
    start_datetime = Column(DateTime, nullable=False)
    rest_between_approaches = Column(
        Interval, nullable=False, default=timedelta(minutes=1)
    )

    __table_args__ = (
        CheckConstraint("approaches_number > 0", name="check_approaches_positive"),
        CheckConstraint("repetitions_number > 0", name="check_repetitions_positive"),
        CheckConstraint(
            "rest_between_approaches > interval '0'", name="check_rest_positive"
        ),
    )
