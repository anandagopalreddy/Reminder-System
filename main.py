from fastapi import FastAPI, HTTPException,Body
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional
import logging
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.models import User,Reminder
from .schemas import SnoozeInput
# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api.main")

# Database setup
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/remaindersystem"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Endpoint: Create User
@app.post("/create-user", status_code=201)
def create_user(user: UserCreate):
    db = SessionLocal()
    try:
        new_user = User(username=user.username, email=user.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"status": 201, "message": "User created successfully.", "user_id": new_user.user_id}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="User creation failed.")
    finally:
        db.close()

@app.post("/create-reminder", status_code=201)
def create_reminder(data: ReminderCreate):
    db = SessionLocal()
    try:
        total_time = timedelta(weeks=data.weeks, days=data.days, hours=data.hours, minutes=data.minutes)
        reminder_time = datetime.now()
        scheduled_time = reminder_time + total_time

        new_reminder = Reminder(
            user_id=data.user_id,
            message=data.message,
            reminder_time=reminder_time,
            scheduled_time=scheduled_time,
            is_active=True,
            snooze_duration={
                "weeks": data.weeks,
                "days": data.days,
                "hours": data.hours,
                "minutes": data.minutes
            }
        )

        db.add(new_reminder)
        db.commit()
        db.refresh(new_reminder)

        formatted_duration = f"{data.weeks} weeks, {data.days} days, {data.hours} hours, and {data.minutes} minutes"

        return {
            "status": 201,
            "message": "Reminder created successfully.",
            "data": {
                "Total Wait Time": formatted_duration,
                "Scheduled Time": scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except Exception as e:
        logger.error(f"Error creating reminder: {e}")
        raise HTTPException(status_code=500, detail="Reminder creation failed.")
    finally:
        db.close()


@app.post("/calculate-snooze-time", status_code=200)
def calculate_snooze_time(input_data: SnoozeInput):
    try:
        total_time = timedelta(
            weeks=input_data.weeks,
            days=input_data.days,
            hours=input_data.hours,
            minutes=input_data.minutes
        )

        if total_time == timedelta(0):
            return {
                "status": 200,
                "message": "No time selected. Reminder will not be snoozed anymore.",
                "data": {"status": "REMINDER_DELETED"}
            }

        new_time = datetime.now() + total_time
        formatted_duration = f"{input_data.weeks} weeks, {input_data.days} days, {input_data.hours} hours, and {input_data.minutes} minutes"

        return {
            "status": 200,
            "message": "Snooze time calculated successfully.",
            "data": {
                "Total Wait Time": formatted_duration,
                "New Scheduled Time": new_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }

    except ValueError as ve:
        raise HTTPException(
            status_code=422,
            detail={
                "status": 422,
                "message": "Invalid input values.",
                "data": None
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": 500,
                "message": "Internal Server Error",
                "data": None
            }
        )


@app.post("/update-reminder", status_code=200)
def update_reminder(input_data: SnoozeInput):
    db = SessionLocal()
    reminder = db.query(Reminder).filter_by(reminder_id=input_data.reminder_id).first()
    if not reminder:
        db.close()
        raise HTTPException(status_code=404, detail=f"Reminder not found for reminder_id {input_data.reminder_id}")

    try:
        # Calculate total time to be added (weeks, days, hours, minutes)
        total_time = timedelta(
            weeks=input_data.weeks,
            days=input_data.days,
            hours=input_data.hours,
            minutes=input_data.minutes
        )

        # If no time is provided, mark reminder as inactive (deleted behavior)
        if total_time == timedelta(0):
            reminder.is_active = False
            db.commit()
            return {
                "status": 200,
                "message": "No time selected. Reminder will not be snoozed anymore.",
                "data": {
                    "status": "REMINDER_DELETED",
                    "Total Wait Time": "0 weeks, 0 days, 0 hours, and 0 minutes",
                    "Scheduled Time": reminder.scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
                }
            }

        # Update the reminder with the new scheduled time
        reminder.scheduled_time += total_time
        reminder.snooze_duration = {
            "weeks": input_data.weeks,
            "days": input_data.days,
            "hours": input_data.hours,
            "minutes": input_data.minutes
        }

        db.commit()

        formatted_duration = f"{input_data.weeks} weeks, {input_data.days} days, {input_data.hours} hours, and {input_data.minutes} minutes"

        return {
            "status": 200,
            "message": "Reminder snoozed and updated in the database successfully.",
            "data": {
                "Total Wait Time": formatted_duration,
                "Scheduled Time": reminder.scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }

    except Exception as e:
        logger.error(f"Error updating reminder: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again later.")
    
    finally:
        db.close()
