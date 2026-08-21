from plyer import notification


def show_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Python Chat Application",
            timeout=5
        )
    except Exception as error:
        print(f"Notification error: {error}")