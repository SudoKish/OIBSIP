import threading
from queue import Queue


reminder_queue = Queue()


def reminder_alert():

    reminder_queue.put(
        "Your reminder is complete."
    )


def set_reminder(seconds):

    timer = threading.Timer(
        seconds,
        reminder_alert
    )

    timer.daemon = True
    timer.start()


def get_pending_reminders():

    reminders = []

    while not reminder_queue.empty():

        reminders.append(
            reminder_queue.get()
        )

    return reminders