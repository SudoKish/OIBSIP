def detect_intent(command):

    command = command.lower().strip()

    # -----------------------------
    # GREETING
    # -----------------------------

    if (
        command == "hello"
        or command == "hi"
        or command == "hey"
        or "hey there" in command
    ):
        return "GREETING"

    # -----------------------------
    # TIME
    # -----------------------------

    if (
        "what time" in command
        or "current time" in command
        or "tell me the time" in command
    ):
        return "GET_TIME"

    # -----------------------------
    # DATE
    # -----------------------------

    if (
        "today's date" in command
        or "todays date" in command
        or "what is the date" in command
        or "current date" in command
    ):
        return "GET_DATE"

    # -----------------------------
    # WEATHER
    # -----------------------------

    if (
        "weather" in command
        or "temperature" in command
        or "forecast" in command
    ):
        return "WEATHER"

    # -----------------------------
    # EXIT
    # -----------------------------

    if (
        command == "exit"
        or command == "quit"
        or command == "stop"
        or command == "goodbye"
        or command == "good bye"
    ):
        return "EXIT"

    # -----------------------------
    # REMINDER
    # -----------------------------

    if (
        "remind me" in command
        or "set a reminder" in command
        or "set reminder" in command
    ):
        return "SET_REMINDER"

    # -----------------------------
    # EMAIL
    # -----------------------------

    if (
        "send an email" in command
        or "send email" in command
        or "send a mail" in command
        or "send mail" in command
    ):
        return "SEND_EMAIL"

    # -----------------------------
    # GENERAL KNOWLEDGE / Q&A
    # -----------------------------

    if (
        command.startswith("what ")
        or command.startswith("who ")
        or command.startswith("where ")
        or command.startswith("when ")
        or command.startswith("why ")
        or command.startswith("how ")
        or command.startswith("tell me about ")
        or command.startswith("explain ")
    ):
        return "QUESTION"

    # -----------------------------
    # WEB SEARCH
    # -----------------------------

    if (
        "please search" in command
        or "search for" in command
        or command.startswith("search ")
        or "look up" in command
        or "can you search" in command
    ):
        return "WEB_SEARCH"

    # -----------------------------
    # UNKNOWN
    # -----------------------------

    return "UNKNOWN"


if __name__ == "__main__":

    test_commands = [

        "Hello",
        "Hey there",

        "What time is it?",
        "Can you tell me the current time?",

        "What is today's date?",

        "Please search Python decorators",
        "Look up machine learning",

        "Goodbye",

        "Remind me in 10 seconds",
        "Set a reminder for 1 minute",
        "Can you set a reminder for 5 minutes?",

        "What's the weather in Pune?",
        "Tell me the weather in Mumbai",
        "What is the temperature in Delhi?",

        "Send an email",
        "Send an email to someone",
        "Can you send a mail",
        "Please send an email",

        "What is Python?",
        "Who invented Python?",
        "How does Python work?",
        "Tell me about artificial intelligence",
        "Why is Python popular?"
    ]

    for command in test_commands:

        print(
            f"{command} -> {detect_intent(command)}"
        )