from sqlalchemy import Integer, String, ForeignKey, Identity
from sqlalchemy.orm import relationship, mapped_column, Mapped

from database.db_setup import Base

class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)

    tasks = relationship("TaskDB", back_populates="owner", cascade="all, delete")
    categories = relationship("CategoryDB", back_populates="user", cascade="all, delete")




