from sqlalchemy import (
    Column,
    Integer,
    String,
    func,
    Enum,
    DateTime,
    ForeignKey,
    Table,
)

from .user import Base, BaseEnum


class CourseType(BaseEnum):
    TRAINING = "Обучение"
    PROFESSIONAL_DEVELOPMENT = "Повышение квалификации"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)
    description = Column(String(120), nullable=False)
    type = Column(Enum(CourseType), default=CourseType.TRAINING, nullable=False)
    creation_at = Column(DateTime, default=func.now(), nullable=False)
    last_update_at = Column(DateTime, default=None)


class CourseTask(Base):
    __tablename__ = "course_tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)
    condition = Column(String(120), unique=True, nullable=False)
    content = Column(String(50), unique=True, nullable=False)
    execution_duration = Column(Integer, default=1, nullable=False)


course_task_association = Table(
    "courses_tasks",
    Base.metadata,
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
    Column("task_id", ForeignKey("course_tasks.id"), primary_key=True),
)
