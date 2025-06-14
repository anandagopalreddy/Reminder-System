from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None

class ReminderCreate(BaseModel):
    user_id: int
    message: str
    reminder_time: Optional[datetime] = None
    weeks: Optional[int] = 0
    days: Optional[int] = 0
    hours: Optional[int] = 0
    minutes: Optional[int] = 0

class SnoozeInput(BaseModel):
    reminder_id: int
    weeks: Optional[int] = 0
    days: Optional[int] = 0
    hours: Optional[int] = 0
    minutes: Optional[int] = 0
class ReminderUpdate(BaseModel):
    reminder_id: int
    weeks: Optional[int] = 0
    days: Optional[int] = 0
    hours: Optional[int] = 0
    minutes: Optional[int] = 0
