from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import send_reminder_notifications
from datetime import datetime, time
import pytz

def start():
    try:
        # Set the timezone for the United Arab Emirates
        timezone = pytz.timezone('Asia/Dubai')

        # Create a BackgroundScheduler with the specified timezone
        scheduler = BackgroundScheduler(timezone=timezone)
        
        # Set the time of day when the job should run
        scheduled_time = time(17, 13)  #  12:01 AM in 24-hour format

        # Set the current date and time for the next run
        next_run_time = datetime.now(timezone).replace(hour=scheduled_time.hour, minute=scheduled_time.minute, second=0, microsecond=0)

        # Add the job to the scheduler
        scheduler.add_job(send_reminder_notifications, trigger="daily", next_run_time=next_run_time, id="send_reminder_001", replace_existing=True)
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


