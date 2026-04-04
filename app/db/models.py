from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    role:
    created_at: 
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", 
        back_populates="user",
        cascade="all, delete-orphan"
    )

class ChatMessage(Base):

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id
    role,
    content,
    created_at Mapped[str | None] = mapped_column(String(128), nullable=True)