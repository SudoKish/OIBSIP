import re


def normalize_email(text):

    text = text.lower().strip()

    # Convert common spoken email phrases
    replacements = {
        " at the rate ": "@",
        " at rate ": "@",
        " at ": "@",
        " dot ": ".",
        " period ": ".",
        " underscore ": "_",
        " dash ": "-",
        " hyphen ": "-"
    }

    for spoken, symbol in replacements.items():
        text = text.replace(spoken, symbol)

    # Remove spaces around email symbols
    text = text.replace(" @", "@")
    text = text.replace("@ ", "@")
    text = text.replace(" .", ".")
    text = text.replace(". ", ".")

    return text


def extract_email_details(command):

    command = normalize_email(command)

    # Find email address
    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        command
    )

    if not email_match:
        return None, None

    receiver = email_match.group(0)

    # Find message after "saying"
    message_match = re.search(
        r'\bsaying\s+(.+)',
        command
    )

    if message_match:

        message = message_match.group(1).strip()

    else:

        message = ""

    return receiver, message


if __name__ == "__main__":

    test_commands = [

        "Send an email to test@gmail.com saying hello",

        "Send an email to Kishan at the rate gmail.com saying hello",

        "Send a mail to Kishan at gmail dot com saying I will reach late",

        "Kishan at the rate gmail dot com"

    ]

    for command in test_commands:

        receiver, message = extract_email_details(
            command
        )

        print("\nCommand:", command)
        print("Receiver:", receiver)
        print("Message:", message)