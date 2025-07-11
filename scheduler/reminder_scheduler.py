import time
from datetime import datetime
from database.db_manager import get_reminders_at_time

def send_reminder(user_id, message):
    print(f"🔔 Reminder for {user_id}: {message}")

def start_scheduler():
    print("🕒 Reminder scheduler started...")
    while True:
        now = datetime.now().strftime("%H:%M")
        reminders = get_reminders_at_time(now)
        for user_id, message in reminders:
            send_reminder(user_id, message)
        time.sleep(60)
