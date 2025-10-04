from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from schemas.task import TaskStatus

from datetime import datetime

from database.db_setup import Base

class TaskDB(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(String, default=TaskStatus.PENDING)
    due_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))

    owner = relationship("UserDB", back_populates="tasks")
    category = relationship("CategoryDB", back_populates="tasks")
