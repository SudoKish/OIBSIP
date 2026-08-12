import re


def extract_duration(command):

    command = command.lower()

    # Find number + time unit
    match = re.search(
        r"(\d+)\s*(second|seconds|minute|minutes|hour|hours)",
        command
    )

    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    if "second" in unit:
        seconds = value

    elif "minute" in unit:
        seconds = value * 60

    elif "hour" in unit:
        seconds = value * 60 * 60

    else:
        return None

    return seconds

if __name__ == "__main__":

    test_commands = [
        "Remind me in 10 seconds",
        "Set a reminder for 2 minutes",
        "Remind me in 1 hour",
        "Can you remind me after 30 seconds?"
    ]

    for command in test_commands:
        duration = extract_duration(command)
        print(command, "->", duration, "seconds")