import re


def extract_city(command):

    command = command.lower().strip()

    patterns = [
        r"weather in (.+)",
        r"temperature in (.+)",
        r"forecast in (.+)",
        r"weather for (.+)",
        r"temperature for (.+)",
        r"forecast for (.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            command
        )

        if match:

            city = match.group(1)

            # Remove common question words
            city = city.replace("?", "")
            city = city.replace("please", "")
            city = city.strip()

            return city

    return None


if __name__ == "__main__":

    test_commands = [
        "What's the weather in Pune?",
        "Tell me the weather in Mumbai",
        "What is the temperature in Delhi?",
        "Give me the forecast in Nagpur"
    ]

    for command in test_commands:

        city = extract_city(command)

        print(
            command,
            "->",
            city
        )