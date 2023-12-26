from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import send_reminder_notifications
import pytz

def start():
    try:
        # Set the timezone for the United Arab Emirates
        timezone = pytz.timezone('Asia/Dubai')

        # Create a BackgroundScheduler with the specified timezone
        scheduler = BackgroundScheduler(timezone=timezone)

        # Schedule the job to run daily at 12:00 AM
        scheduler.add_job(
            send_reminder_notifications,
            trigger="cron",
            hour=16,
            minute=40,
            second=0,
            id="send_reminder_001",
            replace_existing=True,
        )

        # Start the scheduler
        scheduler.start()

        # Use a with statement to ensure proper resource cleanup
        with scheduler:
            # Add an informative comment
            print("Scheduler started successfully. Press Ctrl+C to stop.")

            # Keep the application running
            while True:
                pass

    except Exception as e:
        # Handle exceptions and print a warning message
        print(f"An error occurred: {e}")
