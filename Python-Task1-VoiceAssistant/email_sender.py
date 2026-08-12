import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


def send_email(receiver, subject, message):

    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:

        return "Email credentials are not configured."

    try:

        email = EmailMessage()

        email["From"] = EMAIL_ADDRESS
        email["To"] = receiver
        email["Subject"] = subject

        email.set_content(message)

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_APP_PASSWORD
            )

            smtp.send_message(email)

        return "Email sent successfully."

    except smtplib.SMTPAuthenticationError:

        return "Email authentication failed. Please check your app password."

    except smtplib.SMTPException as e:

        print("SMTP error:", e)

        return "There was a problem sending the email."

    except Exception as e:

        print("Email error:", e)

        return "Something went wrong while sending the email."


if __name__ == "__main__":

    receiver = input(
        "Enter receiver email: "
    )

    subject = input(
        "Enter subject: "
    )

    message = input(
        "Enter message: "
    )

    result = send_email(
        receiver,
        subject,
        message
    )

    print(result)