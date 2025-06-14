from datetime import datetime, timedelta

def calculate_snooze_duration(weeks=0, days=0, hours=0, minutes=0):
    return timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)

def format_snooze_message(weeks, days, hours, minutes):
    return f"{weeks} weeks, {days} days, {hours} hours, and {minutes} minutes"
