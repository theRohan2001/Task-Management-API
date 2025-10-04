from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.db_setup import Base

class CategoryDB(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    user = relationship("UserDB", back_populates="categories")
    tasks = relationship("TaskDB", back_populates="category", cascade="all, delete")