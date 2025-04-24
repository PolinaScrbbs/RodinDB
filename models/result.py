from sqlalchemy import (
    Column,
    Integer,
    String,
    func,
    DateTime,
    ForeignKey,
)

from database import Base


class CourseResult(Base):
    __tablename__ = "course_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    completed_at = Column(DateTime, default=func.now(), nullable=False)
    score = Column(Integer, nullable=False)


class TaskResult(Base):
    __tablename__ = "task_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("course_tasks.id"), nullable=False)
    completed_at = Column(DateTime, default=func.now(), nullable=False)
    is_correct = Column(Integer, nullable=False)
    answer_text = Column(String(255), nullable=True)
