from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from api.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=True)
    reminders = relationship("Reminder", back_populates="user")


class Reminder(Base):
    __tablename__ = "reminders"

    reminder_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    message = Column(Text, nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    snooze_duration = Column(JSON, nullable=True)

    user = relationship("User", back_populates="reminders")
